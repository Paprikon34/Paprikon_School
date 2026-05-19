# Repo Analytics

## Popis a cíl projektu
Automatizovaný systém pro sledování metrik a statistik celého repozitáře. Cílem je poskytovat přehled o vývoji projektů, počtu řádků kódu a distribuci technologií.

## Funkcionalita programu
- Skenování adresářové struktury a detekce projektů s jejich individuálními statistikami.
- Sledování počtu adresářů v repozitáři.
- Počítání souborů podle přípon (.py, .cpp, .md, .h, .json, .txt, .yml, .yaml, .csv).
- Analýza celkového počtu řádků kódu, dokumentace a datových souborů (globálně i pro jednotlivé projekty).
- Sledování celkové velikosti repozitáře (KB).
- Výpočet průměrného počtu řádků na soubor.
- Identifikace 5 největších souborů v celém repozitáři.
- Generování a aktualizace datového souboru `repo_stats.json`.
- Generování formátovaného reportu `repo_report.md` pro lidsky čitelný přehled.
- Automatizované spouštění pomocí GitHub Actions.

## Technická část
- **Jazyk**: Python 3.12
- **Knihovny**: `os`, `json`, `datetime` (standardní knihovny)
- **Logika**: Rekurzivní procházení adresářů se selektivním filtrováním systémových složek.
