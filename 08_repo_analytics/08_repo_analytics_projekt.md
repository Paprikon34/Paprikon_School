# Repo Analytics

## Popis a cíl projektu
Automatizovaný systém pro sledování metrik a statistik celého repozitáře. Cílem je poskytovat přehled o vývoji projektů, počtu řádků kódu a distribuci technologií.

## Funkcionalita programu
- Skenování adresářové struktury a detekce projektů.
- Počítání souborů podle přípon (.py, .cpp, .md).
- Analýza celkového počtu řádků kódu a dokumentace (odděleně).
- Generování a aktualizace datového souboru `repo_stats.json`.
- Automatizované spouštění pomocí GitHub Actions.

## Technická část
- **Jazyk**: Python 3.12
- **Knihovny**: `os`, `json`, `datetime` (standardní knihovny)
- **Logika**: Rekurzivní procházení adresářů se selektivním filtrováním systémových složek.
