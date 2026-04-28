# 🏰 Projekt 07: Library Management System

## 📋 Popis projektu
Pokročilý systém pro správu knihovny postavený na principech **objektově orientovaného programování (OOP)** v jazyce C++. Cílem projektu je vytvořit robustní aplikaci pro evidenci knih, čtenářů a výpůjček s podporou persistence dat ve formátu JSON.

## 🛠 Technické pilíře
- **OOP Architektura**: Dekompozice systému na třídy `Book`, `User` a `LibraryManager`.
- **JSON Modernizace**: Využití knihovny `nlohmann/json` pro špičkovou práci s daty.
- **Robustnost**: Statické i dynamické metody pro validaci a transformaci dat.
- **Relace**: Provázání knih s uživateli pomocí unikátních identifikátorů.

## 📂 Aktuální struktura
- `Book.h / .cpp`: Kompletní implementace objektu knihy včetně serializace.
- `json.hpp`: Header-only knihovna pro JSON operace.
- `data/library.json`: Hlavní databáze knih a uživatelů.
- `popular_manga_and_novels.json`: Rozšířený datový dataset pro testování (200+ položek).

## 📊 Stav vývoje
- [x] **Návrh tříd a relací**: Definována struktura Book a User v JSON.
- [x] **Základní komponenty**: Implementována třída `Book` s kompletní logikou.
- [x] **Persistence dat**: Plná podpora JSON (Save/Load).
- [/] **Library Manager**: Jádro systému (ve vývoji).
- [ ] **Uživatelské rozhraní**: Interaktivní konzolové menu.
- [ ] **Systém výpůjček**: Pokročilá logika pro správu čtenářů a termínů.

## 🚀 Aktuální cíle (Sprint)
1. **Implementace LibraryManager**: Dokončení hlavní logiky pro správu kolekce knih a uživatelů.
2. **Vyhledávací algoritmy**: Filtrování podle žánru a dostupnosti.
3. **Zabezpečení JSON**: Ošetření stavu, kdy je soubor databáze poškozen nebo prázdný.

## 💾 Datový model (Snippet)
```json
{
  "books": [
    {
      "id": 1,
      "title": "Harry Potter",
      "author": "J.K. Rowling",
      "is_available": true,
      "borrower": "None"
    }
  ],
  "users": [
    {
      "id": 101,
      "name": "patrik_dev",
      "borrowed_count": 1
    }
  ]
}
```
