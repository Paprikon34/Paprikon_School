import json

def verify_pokemon_data():
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, "..", "pokemon.json")
        with open(data_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading pokemon.json: {e}")
        return

    print(f"Total entries: {len(data)}")

    missing_fields = []
    
    # Check specifically for Charizard weakness to Rock (4x)
    # Charizard is Fire/Flying.
    # Rock is Super Effective vs Fire (2x) and Super Effective vs Flying (2x) -> 4x.
    
    charizard = data.get('charizard')
    if charizard:
        weaknesses = charizard.get('weaknesses', [])
        # Format is "type (multiplierx)"
        # e.g. "rock (4.0x)"
        rock_weak = next((w for w in weaknesses if w.startswith('rock')), None)
        if rock_weak:
            print(f"Charizard weakness verified: {rock_weak}")
            if "4.0x" not in rock_weak:
                print("WARNING: Charizard rock weakness might be incorrect multiplier!")
        else:
            print("WARNING: Charizard missing rock weakness!")
            
    # Check Scizor (Bug/Steel) -> 4x Fire
    scizor = data.get('scizor')
    if scizor:
        weaknesses = scizor.get('weaknesses', [])
        fire_weak = next((w for w in weaknesses if w.startswith('fire')), None)
        if fire_weak:
            print(f"Scizor weakness verified: {fire_weak}")
            if "4.0x" not in fire_weak:
                print("WARNING: Scizor fire weakness might be incorrect multiplier!")
        else:
             print("WARNING: Scizor missing fire weakness!")

    entries_with_new_fields = 0

    for name, details in data.items():
        has_new = True
        if 'gender' not in details: has_new = False
        if 'abilities' not in details: has_new = False
        if 'weaknesses' not in details: has_new = False
        
        if has_new:
            entries_with_new_fields += 1
        else:
            missing_fields.append(name)

    print(f"Entries with new fields: {entries_with_new_fields}/{len(data)}")
    
    if len(missing_fields) > 0 and len(missing_fields) < 20:
        print(f"Missing new fields for: {missing_fields}")
    elif len(missing_fields) >= 20:
        print(f"Missing new fields for {len(missing_fields)} Pokemon (fetching might be in progress).")

if __name__ == "__main__":
    verify_pokemon_data()
