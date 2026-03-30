# Poke_lib (Pokedex Ultra)

Tento dokument slouží jako podrobný průvodce kódem a strukturou projektu **Poke_lib**, který se zaměřuje na sběr, zpracování a vizualizaci dat o Pokémonech pomocí oficiálního rozhraní PokéAPI.

## 📋 Popis a cíl projektu
Cílem projektu bylo vytvořit komplexní knihovnu a prohlížeč (Pokédex), který dokáže v reálném čase stahovat data z webu, ukládat je do strukturovaného formátu JSON a následně je prezentovat uživateli jak v grafickém rozhraní (Python), tak v rychlém konzolovém prostředí (C++).

## 🚀 Hlavní funkcionalita
Projekt se skládá ze tří klíčových částí:

1.  **Data Fetcher (`fetch_pokedata.py`)**: 
    -   Využívá multithreading (`concurrent.futures`) pro extrémně rychlé stahování dat o více než 1000 Pokémonech.
    -   Automaticky počítá slabosti (weaknesses) na základě typových kombinací.
    -   Zpracovává různé variety Pokémonů (Mega evoluce, regionální formy).
    -   Ukládá data do redundantního JSON souboru s průběžným ukládáním.

2.  **GUI Pokedex (`pokedex_gui.py`)**:
    -   Postaven na frameworku **PyQt6**.
    -   Nabízí pokročilé filtrování podle jména, ID, regionu a typů.
    -   Asynchronní načítání obrázků (neblokující UI).
    -   Detailní statistiky, evoluční linie, seznamy útoků a historie záznamů z různých her.

3.  **C++ Loader (`main.cpp`)**:
    -   Využívá knihovnu `nlohmann/json` pro ultra-rychlé parsování dat.
    -   Poskytuje jednoduché konzolové rozhraní pro vyhledávání Pokémonů bez nutnosti grafického prostředí.

## 🛠 Technická specifikace a instalace

### 🔌 Instalace závislostí
Před prvním spuštěním je nutné nainstalovat potřebné knihovny:
```bash
pip install -r requirements.txt
```

| Technologie | Využití v projektu |
| :--- | :--- |
| **Python 3.12+** | Skriptování, stahování dat a GUI |
| **PyQt6** | Moderní grafické rozhraní |
| **Requests** | Komunikace s PokéAPI |
| **C++ / GCC** | Rychlé konzolové zpracování dat |
| **nlohmann/json** | Standardní formát pro výměnu dat |

---

## 🔍 Rozbor klíčových částí kódu

### 1. Paralelní zpracování dat (Multithreading)
Pro zrychlení stahování dat o tisících objektů používáme `ThreadPoolExecutor`.

```python
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Odeslání úkolů (fetchování každého Pokémona zvlášť)
    future_to_entry = {executor.submit(process_pokemon, entry, ...): entry for entry in results}
```
*Vysvětlení:* Díky tomuto přístupu se program neblokuje čekáním na odpověď ze serveru u jednoho Pokémona, ale zpracovává jich až 10 současně.

### 2. Typová tabulka a slabosti
Program obsahuje algoritmus pro výpočet efektivity útoků.

```python
def calculate_weaknesses(def_types):
    multipliers = {t: 1.0 for t in all_types}
    for dt in def_types:
        rels = TYPE_CHART[dt]
        for t in rels['double']: multipliers[t] *= 2.0
        for t in rels['half']: multipliers[t] *= 0.5
        # ...
```
*Proč toto řešení?* PokéAPI neposkytuje slabosti přímo pro konkrétní Pokémony. Tato logika umožňuje dynamicky zjistit, na které útoky je Pokémon náchylný i u unikátních typových kombinací.

### 3. Asynchronní GUI
V Pokédexu používáme `QThread` pro stahování obrázků, aby aplikace „nezamrzala“ při načítání galerie.

---

## 📂 Adresářová struktura (Profesionální uspořádání)
Projekt je organizován do logických celků pro snadnou údržbu:

*   **Hlavní skripty (Root)**:
    *   `fetch_pokedata.py`: Skript pro generování a aktualizaci databáze.
    *   `pokedex_gui.py`: Hlavní aplikace s grafickým rozhraním PyQt6.
    *   `pokemon.json`: Centralizovaná databáze Pokémonů.
    *   `run_app.bat`: Rychlý spouštěč aplikace.
*   **`bin/`**: Obsahuje zkompilované binární soubory a pomocné spouštěče.
*   **`cpp/`**: Zdrojové kódy v C++ a nezbytné knihovny (`json.hpp`).
*   **`tests/`**: Verifikační skripty pro kontrolu integrity databáze.
*   `03_poke_lib_projekt.md`: Tato technická dokumentace.

---

## 📖 Uživatelská příručka
1.  **Příprava**: Spusťte `fetch_pokedata.py` pro vygenerování aktuálního souboru `pokemon.json`.
2.  **Spuštění GUI**: Použijte `run_app.bat` nebo přímo `pokedex_gui.py`.
3.  **Konzolové vyhledávání (C++)**: Přejděte do `bin/` a spusťte `pokedex.exe` (nebo zkompilujte `cpp/main.cpp`).
4.  **Verifikace**: Pro kontrolu správnosti dat spusťte skripty ve složce `tests/`.
