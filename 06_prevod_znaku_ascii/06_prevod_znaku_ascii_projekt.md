# Převod znaků na ASCII (ASCII Converter)

Tento dokument popisuje projekt **Převod znaků na ASCII**, jednoduchý konzolový nástroj v C++, který převádí:
- zadaný znak → jeho číselnou hodnotu (ASCII / kód znaku)
- zadané celé číslo → odpovídající znak

## 📋 Popis a cíl projektu
Cílem projektu je procvičit práci se vstupem/výstupem v konzoli, základní validaci vstupu a převody typů (cast) v jazyce C++.

Program je určen pro začátečníky jako demonstrace toho, jak v C++ reprezentují znaky čísla (kódy znaků).

## 🚀 Hlavní funkcionalita
1. **Znak → číslo**
   - Program si vyžádá právě jeden znak.
   - Pokud uživatel zadá více znaků, program jej vyzve k opravě.
   - Následně vypíše číselnou hodnotu znaku.

2. **Číslo → znak**
   - Program si vyžádá celé číslo (např. `65` pro `A`).
   - Vypíše znak odpovídající zadanému číslu.

3. **Opakování běhu**
   - Program se po dokončení zeptá, zda chce uživatel pokračovat (`y/Y`).

## 🛠 Technická specifikace
| Technologie / prvek | Využití v projektu |
| :--- | :--- |
| **C++** | Implementace konzolového programu. |
| **<iostream>** | `cin`, `cout`, `endl` (vstup/výstup). |
| **<string>** | Bezpečné načtení vstupu pro kontrolu, že uživatel zadal právě jeden znak. |
| **Typové převody (cast)** | Převod `char → int` a `int → char`. |

## ▶️ Spuštění (doporučení)
- Otevřete soubor `ascii_converter.cpp` ve VS Code.
- Spusťte build úlohu **C/C++: g++.exe build active file**.
- Poté spusťte vygenerovaný `.exe` soubor ve stejné složce.

Poznámka: Některé číselné hodnoty (typicky pod 33) reprezentují řídicí znaky a nemusí se zobrazit „jako písmeno“.

## 📂 Adresářová struktura
- `ascii_converter.cpp` — zdrojový kód programu.
- `06_prevod_znaku_ascii_projekt.md` — tato dokumentace.
