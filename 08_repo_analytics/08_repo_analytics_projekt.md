# Repo Analytics

## 📋 Popis a cíl projektu
Automatizovaný systém pro sledování metrik, statistik a plnění administrativních podmínek celého repozitáře. Cílem je poskytovat přehled o vývoji projektů, počtu řádků kódu, distribuci technologií a monitorovat dodržování pravidel výuky (příprava na hodnocení AI).

## 🚀 Hlavní funkcionalita
Program je rozdělen do několika modulů, které automaticky skenují repozitář a generují výstupy:

1. **Skenování adresářové struktury**:
   - Detekce jednotlivých projektů (číselné složky) a jejich individuálních statistik.
   - Sledování celkového počtu složek a fyzické velikosti repozitáře v KB.
   - Počítání souborů podle klíčových přípon (`.py`, `.cpp`, `.md`, `.h`, `.json`, `.txt`, `.yml`, `.yaml`, `.csv`).
   - Analýza řádků rozdělených na kód, dokumentaci a datové/konfigurační soubory.
   - Identifikace 5 největších souborů v celém repozitáři podle počtu řádků.

2. **Git integrace a analýza historie**:
   - Analýza historie commitů z `git log`.
   - Zjištění celkového počtu commitů a počtu aktivních vývojových dnů.
   - Získání informací o posledním commitu (autor, zpráva, datum).

3. **Týdenní Hodnocení & Disciplína (Grading Dashboard)**:
   - Vyhodnocování tří administrativních podmínek pro získání bonusu **60 bodů**:
     - **Podmínka 1**: Minimálně 3 commity za aktuální týden (filtruje automatické commity bota, počítá pouze reálnou práci studenta).
     - **Podmínka 2 (Pravidlo 12 hodin)**: Kontrola, zda alespoň 3 commity dělí časový rozestup minimálně 12 hodin.
     - **Podmínka 3**: Ověření přítomnosti hlavního `README.md` v kořenu a `[nazev]_projekt.md` ve všech aktivních projektech.
   - Výpočet odhadovaného bonusu za disciplínu (+20 bodů za každé splněné pravidlo).

4. **Automatické generování výstupů**:
   - Uložení strukturovaných dat do `repo_stats.json`.
   - Generování přehledného Markdown reportu `repo_report.md` včetně Mermaid.js koláčového grafu distribuce řádků.
   - Automatická aktualizace tabulky statistik v hlavním souboru `README.md`.

## 🛠 Technická specifikace
- **Jazyk**: Python 3.12+
- **Použité moduly**:
  - `os` a `sys`: Práce se soubory, systémem a kódováním výstupu.
  - `json`: Serializace a ukládání statistik.
  - `subprocess`: Spouštění Git příkazů pro analýzu logů.
  - `datetime` a `timedelta`: Manipulace s časovými razítky a výpočet 12hodinových intervalů.

## 📂 Adresářová struktura
* `update_stats.py`: Hlavní analytický skript.
* `repo_stats.json`: Uložená data v JSON formátu (generováno automaticky).
* `repo_report.md`: Kompletní přehledový report pro vývojáře (generováno automaticky).
* `08_repo_analytics_projekt.md`: Tato technická dokumentace.

## ▶️ Spuštění programu
Pro ruční aktualizaci statistik a reportů spusťte v kořenovém adresáři repozitáře příkaz:
```bash
python 08_repo_analytics/update_stats.py
```
Program lze také spouštět automaticky pomocí GitHub Actions (např. při každém pushi nebo pravidelně jednou týdně).

