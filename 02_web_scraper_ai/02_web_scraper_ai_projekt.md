# Web Scraper AI (Automatizace)

## Popis a cíl projektu
Projekt slouží k automatizovanému získávání informací z veřejně dostupných webových stránek (např. z portálu erudios.com) a jejich následnému zpracování pomocí lokálního jazykového modelu (Ollama). Cílem je vytvořit samostatného agenta, který dokáže analyzovat texty na stránce, sumarizovat je a navrhovat řešení zadaných úkolů bez nutnosti manuálního přihlašování.

## Funkcionalita programu
Program se skládá z několika hlavních částí:
1. **Web Scraper (Oči):** Pomocí knihovny `requests` a `BeautifulSoup4` stáhne a rozebere HTML strukturu cílové webové stránky a extrahuje relevantní textová data (zadání).
2. **AI Engine (Mozek):** Získaná data jsou přes místní API odeslána do lokálně běžícího LLM (Ollama). Model zpracuje zadání a vygeneruje odpovídající řešení (např. kód v Pythonu).
3. **Git Automator (Ruce):** Zpracované řešení je následně automaticky verzováno pomocí knihovny `GitPython` nebo přes systémové příkazy. Systém obsahuje časovač, který uměle zdržuje odesílání commitů (např. o 12 hodin), aby simuloval reálný průběh práce dle formálních požadavků.

**Použité technologie:** Python, `requests`, `beautifulsoup4`, lokální instance `Ollama`, Git.
