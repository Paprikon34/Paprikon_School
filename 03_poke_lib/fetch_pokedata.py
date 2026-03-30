import requests
import json
import time
import os
import concurrent.futures
import threading

"""
fetch_pokedata.py
-----------------
A multithreaded web scraper for fetching comprehensive Pokemon data from PokeAPI.
This script populates 'pokemon.json' with enriched data including:
- Base stats, height, weight, and abilities.
- Dynamically calculated weaknesses based on type combinations.
- Evolution chains and alternative forms (Megas, regional variants).
- Pokedex entries (flavor text) from across different game versions.
- Encounter locations and capture rates.

Architecture:
Uses 'concurrent.futures.ThreadPoolExecutor' to fetch data for multiple species 
simultaneously, significantly reducing processing time from hours to minutes.
"""

# Constants
# Constants for API and output
POKEAPI_BASE = "https://pokeapi.co/api/v2"  # Base URL for the PokeAPI
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(script_dir, "pokemon.json")  # Path to the output file where data will be saved
MAX_WORKERS = 10                            # Number of parallel threads for fetching data

# Generation to Region mapping
REGION_MAP = {
    "generation-i": "Kanto",
    "generation-ii": "Johto",
    "generation-iii": "Hoenn",
    "generation-iv": "Sinnoh",
    "generation-v": "Unova",
    "generation-vi": "Kalos",
    "generation-vii": "Alola",
    "generation-viii": "Galar",
    "generation-ix": "Paldea"
}

TYPE_CHART = {}
EVO_CACHE = {}
# Threading locks to ensure data integrity when multiple threads write to shared resources
CACHE_LOCK = threading.Lock() # Protects EVO_CACHE from concurrent writes
DATA_LOCK = threading.Lock()  # Protects the final pokemon_data dictionary
PRINT_LOCK = threading.Lock() # Ensures console output from different threads doesn't overlap

def safe_print(msg):
    """
    Thread-safe print function.
    In a multithreaded environment, standard 'print' can sometimes result in 
    interleaved output if two threads print at the exact same millisecond. 
    This lock-based wrapper prevents that.
    """
    with PRINT_LOCK:
        print(msg)

def get_json(url):
    """
    Utility function to fetch and parse JSON from a URL with basic retry logic
    and rate limit handling (429 status code).
    """
    retries = 3
    while retries > 0:
        try:
            # Set a 10s timeout to avoid hanging on slow network responses
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # 429 means we are hitting the API too fast (rate limited)
                # Wait 1 second before retrying to respect the server's limits
                time.sleep(1)
                retries -= 1
                continue
            else:
                safe_print(f"Error fetching {url}: {response.status_code}")
                return None
        except Exception as e:
            safe_print(f"Exception fetching {url}: {e}")
            retries -= 1
    return None

def build_type_chart():
    """
    Fetches all Pokemon types and their damage relations to build a local
    chart. This is used later to calculate weaknesses for dual-type Pokemon.
    """
    safe_print("Building type chart...")
    types_list = get_json(f"{POKEAPI_BASE}/type")
    if not types_list:
        return
    
    for entry in types_list['results']:
        name = entry['name']
        if name in ['unknown', 'shadow']:
            continue
            
        type_data = get_json(entry['url'])
        if not type_data:
            continue
            
        damage_relations = type_data['damage_relations']
        
        rel = {
            "double": [x['name'] for x in damage_relations['double_damage_from']],
            "half": [x['name'] for x in damage_relations['half_damage_from']],
            "zero": [x['name'] for x in damage_relations['no_damage_from']]
        }
        TYPE_CHART[name] = rel
    safe_print("Type chart built.")

def calculate_weaknesses(def_types):
    """
    Calculates combined type effectiveness for a list of defensive types.
    Multiplies base 1.0 effectiveness by 2.0 (weak), 0.5 (resist), or 0.0 (immune).
    """
    all_types = list(TYPE_CHART.keys())
    multipliers = {t: 1.0 for t in all_types}
    
    for dt in def_types:
        if dt not in TYPE_CHART:
            continue
        rels = TYPE_CHART[dt]
        
        for t in rels['double']:
            if t in multipliers: multipliers[t] *= 2.0
        for t in rels['half']:
            if t in multipliers: multipliers[t] *= 0.5
        for t in rels['zero']:
            if t in multipliers: multipliers[t] *= 0.0
            
    weaknesses = []
    for t, mult in multipliers.items():
        # A weakness is defined as having a multiplier of 2.0 or 4.0 (for dual types)
        if mult >= 2.0:
            weaknesses.append(f"{t} ({mult}x)")
    
    return weaknesses

def get_gender_ratio(gender_rate):
    if gender_rate == -1:
        return "Genderless"
    female_chance = (gender_rate / 8.0) * 100
    male_chance = 100 - female_chance
    return f"Male: {male_chance:.1f}%, Female: {female_chance:.1f}%"

def get_evolution_chain(chain_url):
    """
    Retrieves the evolution chain from the given URL. 
    Uses global EVO_CACHE to avoid fetching the same chain for different Pokemon 
    in the same family.
    """
    with CACHE_LOCK:
        if chain_url in EVO_CACHE:
            return EVO_CACHE[chain_url]

    data = get_json(chain_url)
    if not data:
        return []
    
    chain = data['chain']
    evo_list = []
    
    def traverse(node):
        """Recursive helper to flatten the evolution tree into a list."""
        evo_list.append(node['species']['name'])
        for child in node['evolves_to']:
            traverse(child)
            
    traverse(chain)
    
    with CACHE_LOCK:
        EVO_CACHE[chain_url] = evo_list
        
    return evo_list

def process_pokemon(entry, total, idx, current_data):
    """
    The core worker function. Processes a single Pokemon species, 
    including all its varieties (Mega, Alolan forms, etc.).
    Returns a list of dictionaries, one for each variety found.
    """
    name = entry['name']
    
    # Force update mode: fetch data even if it might already exist.
    # We can skip already fetched entries by checking current_data.get(name) 
    # if we want to implement resuming a partially finished run.
    needs_update = True 
    
    if not needs_update:
        return None

    url = entry['url']
    
    # Fetch species level details (description, generation, egg groups)
    species_details = get_json(url)
    if not species_details:
        return None
        
    dex_id = species_details['id']
    gen_name = species_details['generation']['name']
    region = REGION_MAP.get(gen_name, "Unknown")
    gender = get_gender_ratio(species_details['gender_rate'])

    # Evolution data
    evo_chain_url = species_details['evolution_chain']['url'] if species_details['evolution_chain'] else None
    evolution = []
    if evo_chain_url:
        evolution = get_evolution_chain(evo_chain_url)
        
    # Pokedex Flavor Text: extract English entries
    description = "No description available."
    entries_list = []
    seen_texts = set()
    for entry in species_details.get('flavor_text_entries', []):
        if entry['language']['name'] == 'en':
            text = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
            version = entry['version']['name'].replace('-', ' ').title()
            
            # Keep the first suitable entry as primary description
            if description == "No description available.":
                description = text
            
            # Store all version-specific texts for the "Entries" tab in the GUI
            entries_list.append({"version": version, "text": text})

    egg_groups = [g['name'] for g in species_details.get('egg_groups', [])]
    capture_rate = species_details.get('capture_rate')
    hatch_counter = species_details.get('hatch_counter')
    base_happiness = species_details.get('base_happiness')

    variety_results = []
    
    # Iterate through all varieties (Standard, Mega, G-Max, Regional Forms)
    for var in species_details['varieties']:
        v_name = var['pokemon']['name']
        v_url = var['pokemon']['url']
        
        # --- Variety Specific Details ---
        # Fetch specific details for this variety (stats, types, abilities, sprites)
        pokemon_details = get_json(v_url)
        if not pokemon_details:
            continue

        # Extract basic info
        types = [t['type']['name'] for t in pokemon_details['types']]
        abilities = [{"name": ab['ability']['name'], "is_hidden": ab['is_hidden']} for ab in pokemon_details['abilities']]
        
        # Enrichment: calculate double/half damage based on type relation table
        weaknesses = calculate_weaknesses(types)
        
        # --- Stats & Physical Attributes ---
        # Extract base stats (HP, Attack, etc.)
        stats = {s['stat']['name']: s['base_stat'] for s in pokemon_details['stats']}
        # Convert API units (dm, hg) to standard units (m, kg)
        height = pokemon_details['height'] / 10.0
        weight = pokemon_details['weight'] / 10.0
        
        # --- Media (Sprites) ---
        # Prefer high-quality official artwork sprites
        sprite = pokemon_details['sprites'].get('other', {}).get('official-artwork', {}).get('front_default')
        if not sprite:
            sprite = pokemon_details['sprites'].get('front_default')

        shiny_sprite = pokemon_details['sprites'].get('other', {}).get('official-artwork', {}).get('front_shiny')
        if not shiny_sprite:
            shiny_sprite = pokemon_details['sprites'].get('front_shiny')

        base_experience = pokemon_details.get('base_experience')

        # --- Learning Moves ---
        # Move list processing: split into level-up and other methods (TM, Tutor)
        moves = []
        raw_moves = pokemon_details.get('moves', [])
        level_moves = []
        other_moves = []
        for m in raw_moves:
            m_name = m['move']['name']
            is_level = False
            level = 0
            for vgd in m['version_group_details']:
                if vgd['move_learn_method']['name'] == 'level-up':
                    is_level = True
                    level = vgd['level_learned_at']
                    break
            if is_level:
                level_moves.append({"name": m_name, "level": level})
            else:
                other_moves.append({"name": m_name, "level": 0})
        level_moves.sort(key=lambda x: x['level'])
        moves = level_moves + other_moves
        
        # Encounter locations (limit to 10 for performance/clarity)
        enc_url = pokemon_details.get('location_area_encounters')
        locations = []
        if enc_url:
            enc_data = get_json(enc_url)
            if enc_data:
                seen_locs = set()
                for enc in enc_data:
                    loc_name = enc['location_area']['name'].split('-area')[0].replace('-', ' ')
                    if loc_name not in seen_locs:
                        seen_locs.add(loc_name)
                        locations.append(loc_name)
                    if len(locations) >= 10: break

        # Compile variety data
        variety_results.append({
            "name": v_name,
            "data": {
                "id": dex_id,
                "region": region,
                "types": types,
                "evolution": evolution,
                "forms": [v['pokemon']['name'] for v in species_details['varieties']],
                "gender": gender,
                "abilities": abilities,
                "weaknesses": weaknesses,
                "stats": stats,
                "height": height,
                "weight": weight,
                "sprite": sprite,
                "shiny_sprite": shiny_sprite,
                "description": description,
                "pokedex_entries": entries_list,
                "egg_groups": egg_groups,
                "capture_rate": capture_rate,
                "base_experience": base_experience,
                "hatch_counter": hatch_counter,
                "base_happiness": base_happiness,
                "moves": moves,
                "locations": locations
            }
        })
    
    return variety_results

def main():
    """Main execution block."""
    # Ensure type chart is ready for calculating weaknesses
    if not TYPE_CHART:
        build_type_chart()

    safe_print("Fetching Pokemon species list...")
    # Get all species from PokeAPI
    species_list_resp = get_json(f"{POKEAPI_BASE}/pokemon-species?limit=2000")
    if not species_list_resp:
        return

    pokemon_data = {}
    
    # Load existing data if file exists to allow resuming or incremental updates
    if os.path.exists(OUTPUT_FILE):
        safe_print(f"Found existing {OUTPUT_FILE}, loading...")
        try:
            with open(OUTPUT_FILE, 'r') as f:
                pokemon_data = json.load(f)
            safe_print(f"Loaded {len(pokemon_data)} existing entries.")
        except Exception as e:
            safe_print(f"Error loading existing file: {e}")

    # Each species entry points to one or more "varieties" 
    # (e.g. Charizard has Charizard-Mega-X, Charizard-Mega-Y, etc.)
    results = species_list_resp['results']
    total = len(results)
    safe_print(f"Total species to process: {total} with {MAX_WORKERS} workers")

    completed = 0
    
    # Use ThreadPoolExecutor for concurrent web requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit tasks to the pool
        future_to_entry = {executor.submit(process_pokemon, entry, total, i, pokemon_data): entry for i, entry in enumerate(results)}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_entry):
            entry = future_to_entry[future]
            try:
                res_list = future.result()
                if res_list:
                    # Thread-safe dictionary update
                    with DATA_LOCK:
                        for result in res_list:
                            pokemon_data[result['name']] = result['data']
                        completed += 1
                        
                        # Console progress logging
                        if completed % 10 == 0:
                            safe_print(f"Progress: {completed}/{total} species processed")
                        
                        # Intermediate save every 50 species to prevent data loss 
                        # This allows the GUI to be usable even if the fetch script is killed.
                        if completed % 50 == 0:
                            with open(OUTPUT_FILE, 'w') as f:
                                json.dump(pokemon_data, f, indent=2)
            except Exception as exc:
                safe_print(f"Entry {entry['name']} generated an exception: {exc}")

    # Final persistent save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(pokemon_data, f, indent=2)
        
    safe_print("Done!")

if __name__ == "__main__":
    main()
