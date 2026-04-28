# Centrální evidence vývojových projektů (Paprikon School)

Vítejte v mém profesionálním repozitáři, který slouží k systematickému vývoji a evidenci softwarových řešení. Tento projekt je postaven na principech **čistého kódu (Clean Code)**, **modulární architektury** a přísném dodržování **projektové hygieny**.

## 🛠 Hlavní technologické pilíře

| Pilíř | Popis |
| :--- | :--- |
| **Robustní implementace** | Důraz na stabilitu, ošetření chybových stavů a přenositelnost kódu. |
| **Škálovatelná struktura** | Každý projekt je izolován ve vlastní modulární složce. Kořenový adresář (root) zůstává čistý a neobsahuje žádné dočasné ani nesouvisející soubory. |
| **Vyspělá dokumentace** | Souběžná tvorba technické a uživatelské dokumentace pro zajištění vysoké kvality výstupu. |
| **AI Integrace** | Průběžné vylepšování projektů pomocí analytických schopností LLM modelů (Groq, Llama 3.1). |

---

## 🚀 Rychlý start

Pro spuštění většiny projektů v tomto repozitáři je nutné mít nainstalován **Python 3.12+** a **C++ kompilátor (GCC)**. 

1. **Klonování repozitáře**:
   ```bash
   git clone https://github.com/Paprikon34/Paprikon_School.git
   ```
2. **Instalace Python závislostí**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Spuštění projektu**: Přejděte do složky konkrétního projektu (např. `01_kamen_nuzky_papir`) a spusťte hlavní skript (např. `python main.py`).

---

## 📊 Přehled realizovaných projektů

Níže naleznete tabulku s aktuálně vyvíjenými a dokončenými projekty. Každý projekt obsahuje podrobný technický popis struktury v příslušném `_projekt.md` souboru uvnitř své složky.

| ID | Název projektu | Datum zápisu | Klíčové technologie | Náročnost | Stav |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | **[Kámen, nůžky, papír](./01_kamen_nuzky_papir)** | 04.03.2026 | Python, Pygame-ce, OOP | ⭐⭐⭐⭐ | ✅ Hotovo |
| **02** | **[Web Scraper AI](./02_web_scraper_ai)** | 16.03.2026 | Python, Groq API, Scraping | ⭐⭐⭐⭐ | 🚧 Dočasně pozastaven |
| **03** | **[Poke_lib (Pokedex)](./03_poke_lib)** | 30.03.2026 | Python, PyQt6, C++, MultiAPI | ⭐⭐⭐⭐⭐ | ✅ Hotovo |
| **04** | **[Banking Simulator](./04_banking_simulator)** | 04.04.2026 | C++, Console, RNG | ⭐⭐⭐ | ✅ Hotovo |
| **05** | **[Maze Generator](./05_maze_generator)** | 13.04.2026 | Python, Algoritmy, Rekurze | ⭐⭐⭐⭐⭐ | ✅ Hotovo |
| **06** | **[Převod znaků na ASCII](./06_prevod_znaku_ascii)** | 19.04.2026 | C++, Console, ASCII | ⭐⭐ | ✅ Hotovo |
| **07** | **[Library Management System](./07_library_management_system)** | 20.04.2026 | C++, OOP, File I/O | ⭐⭐⭐⭐ | 🚧 Ve vývoji |

---

## 📂 Správa adresářové struktury (**Pravidlo 1**)

V souladu s profesionálními standardy je tento repozitář udržován v maximální čistotě:
*   **Žádné povalující se soubory v kořenu**: Veškeré `.txt`, `.md` (kromě `README.md` a `gitignore`) a pomocné skripty patří výhradně do složek svých projektů.
*   **Automatické čištění**: Interní nástroje (např. automatický bot v projektu 02) jsou konfigurovány tak, aby ukládaly výsledky své práce výhradně do svých přidělených adresářů.

---

## 🛠 Standardy a postupy

Při vývoji jsou striktně dodržovány následující principy:
*   **Clean Code**: Přehledný kód s jasným pojmenováním proměnných a funkcí.
*   **Bilingvní komentování**: Klíčové části kódu jsou komentovány v českém i anglickém jazyce pro maximální srozumitelnost.
*   **Verzování (Git)**: Pravidelné commity s jasným popisem změn, respektující pravidlo 12hodinových rozestupů.
*   **JSON Persistence**: Většina projektů využívá JSON pro ukládání stavu, což zajišťuje přenositelnost a snadnou editaci dat.

## 📈 Statistiky repozitáře

| Metrika | Hodnota |
| :--- | :--- |
| **Počet projektů** | 7 |
| **Hlavní jazyky** | Python, C++ |
| **Stav dokumentace** | 100% (Up to code) |
| **Průměrná náročnost** | ⭐⭐⭐⭐ (Pokročilý) |

---
*Tento repozitář je udržován v souladu s moderními standardy vývoje softwaru a metodikou průběžného verzování.*
