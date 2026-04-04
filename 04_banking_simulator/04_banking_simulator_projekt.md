# Banking Simulator

Tento dokument slouží jako popis projektu **Banking Simulator**, jednoduchého konzolového simulátoru bankovního účtu vytvořeného v jazyce C++.

## 📋 Popis a cíl projektu
Cílem tohoto projektu bylo vytvořit interaktivní bankovní aplikaci v příkazové řádce, která demonstruje základy programování v C++, jako je práce s proměnnými, vstupem a výstupem (I/O), podmínkami a cykly.

## 🚀 Hlavní funkcionalita

Aplikace poskytuje jednoduché menu, ve kterém se uživatel může pohybovat a provádět základní operace se svými penězi:

1. **Vklad (Deposit)**: Umožňuje uživateli na počátku vložit libovolnou částku na svůj účet k vytvoření počátečního zůstatku.
2. **Investování (Invest)**: Hráč může riskovat a investovat část svého zůstatku. Může získat zhodnocení mezi 1% až 5%, ale zároveň má 10% šanci, že svou investici zcela ztratí. K tomu je využito generování náhodných čísel `rand()`.
3. **Výběr (Withdraw)**: Výběr specifikované částky s kontrolou dostatečného zůstatku na účtu (ochrana před záporným zůstatkem).
4. **Hlavní menu**: Cyklus, který neustále nabízí provedení další transakce nebo bezpečné ukončení programu.

## 🛠 Technická specifikace

| Technologie | Využití v projektu |
| :--- | :--- |
| **C++** | Programovací jazyk použitý pro celý projekt. |
| **<iostream>** | Standardní knihovna pro obsluhu vstupů (cin) a výstupů (cout). |
| **<string>** | Knihovna pro práci s textovými řetězci (např. uložení jména uživatele). |
| **<stdlib.h> a <time.h>** | Knihovny pro generování a seedování (srand) pseudonáhodných čísel potřebných v investiční logice. |

---

## 📂 Adresářová struktura
V rámci dodržování čistoty kořenového adresáře a modularity jsou všechny související soubory v příslušné složce:

*   `acout_simulator.cpp`: Zdrojový kód aplikace v C++.
*   `acout_simulator.exe`: Zkompilovaný spustitelný soubor pro platformu Windows.
*   `04_banking_simulator_projekt.md`: Tato dokumentace.
