# Repo Analytics

## Popis a cíl projektu
Automatizovaný systém pro sledování metrik a statistik celého repozitáře. Cílem je poskytovat přehled o vývoji projektů, počtu řádků kódu a distribuci technologií.

## Funkcionalita programu
- Skenování adresářové struktury a detekce projektů s jejich individuálními statistikami.
- Počítání souborů podle přípon (.py, .cpp, .md, .h).
- Analýza celkového počtu řádků kódu a dokumentace (globálně i pro jednotlivé projekty).
- Sledování celkové velikosti repozitáře (KB).
- Výpočet průměrného počtu řádků na soubor.
- Identifikace 5 největších souborů v celém repozitáři.
- Generování a aktualizace rozšířeného datového souboru `repo_stats.json`.
- Automatizované spouštění pomocí GitHub Actions.

## Technická část
- **Jazyk**: Python 3.12
- **Knihovny**: `os`, `json`, `datetime` (standardní knihovny)
- **Logika**: Rekurzivní procházení adresářů se selektivním filtrováním systémových složek.
