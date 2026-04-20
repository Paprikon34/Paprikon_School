# 🏰 Projekt 07: Library Management System

## 📋 Popis projektu
Pokročilý systém pro správu knihovny postavený na principech **objektově orientovaného programování (OOP)** v jazyce C++. Cílem projektu je vytvořit robustní aplikaci pro evidenci knih, čtenářů a výpůjček.

## 🛠 Technické cíle
- **OOP Architektura**: Využití tříd (`Book`, `User`, `Library`).
- **Správa dat**: Ukládání a načítání dat z externího souboru (JSON nebo CSV).
- **Relace**: Propojení knih s konkrétními uživateli.
- **Logika**: Kontrola dostupnosti knih, termíny vrácení a vyhledávání.

## 📂 Plánovaná struktura
- `main.cpp`: Vstupní bod programu.
- `Library.h / .cpp`: Jádro logiky systému.
- `Book.h / .cpp`: Definice objektu knihy.
- `User.h / .cpp`: Správa uživatelských profilů.
- `data/`: Složka pro datové soubory.

## 📊 Stav vývoje
- [ ] Návrh tříd a relací
- [ ] Implementace základní logiky (přidávání/odebírání knih)
- [ ] Persistence dat (ukládání do souboru)
- [ ] Uživatelské menu a vyhledávání
- [ ] Systém výpůjček
