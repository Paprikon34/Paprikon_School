# Web Scraper AI (Automatizace)

Tento dokument slouží jako podrobný průvodce kódem a strukturou projektu **Web Scraper AI**, který automatizuje proces analýzy školních úkolů a opravu kódu pomocí umělé inteligence.

## 📋 Popis a cíl projektu
Cílem projektu je vytvořit samostatně fungujícího agenta (**bota**), který monitoruje vzdělávací portál (např. Erudios), identifikuje zpětnou vazbu od učitele, analyzuje ji pomocí LLM (Groq/Llama-3) a následně navrhuje a ukládá opravy kódu.

## 🚀 Hlavní funkcionalita
Program je rozdělen do několika logických modulů, které simulují lidskou práci vývojáře:

1. **Scraping (Oči)**: Pomocí knihoven `requests` a `BeautifulSoup4` prochází webové stránky a hledá klíčové informace (např. hodnocení studenta).
2. **AI Analýza (Mozek)**: Využívá Groq API k rychlé analýze textu. AI identifikuje, kterého souboru se kritika týká, a vygeneruje opravený kód.
3. **Git Automator (Ruce)**: Automaticky verzuje změny pomocí systému Git, odesílá commity a pushuje kód na GitHub se zprávami vygenerovanými pomocí AI.

## 🛠 Technická specifikace

| Technologie | Využití v projektu |
| :--- | :--- |
| **Python 3.14+** | Základní programovací jazyk |
| **BeautifulSoup4** | Parsing HTML struktury webu |
| **Groq API** | Výkonný LLM model (Llama 3.1) pro rychlou odezvu |
| **Subprocess** | Ovládání systémových příkazů (Git) |
| **Dotenv** | Bezpečná správa API klíčů |

---

## 🔍 Rozbor klíčových částí kódu

### 1. Detekce změn a historie
Bot si ukládá již zpracované odkazy do souboru `zpracovane_odkazy.txt`, aby neřešil stejný úkol dvakrát.

```python
def nacti_historii():
    if os.path.exists(HISTORIE_SOUBOR):
        with open(HISTORIE_SOUBOR, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())
    return set()
```

### 2. Komunikace s AI (Groq)
Funkce `ask_groq` odesílá prompt a systémový kontext do cloudu. Teplota je nastavena na **0.2** pro maximální přesnost při generování kódu.

```python
def ask_groq(prompt, system_prompt="Jsi zkušený senior vývojář.", temperature=0.2):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        temperature=temperature,
    )
    return chat_completion.choices[0].message.content.strip()
```

### 3. Automatizace Gitu
Bot provádí `git add`, `git commit` a `git push` automaticky, přičemž respektuje školní pravidla o časových prodlevách.

---

## 📂 Adresářová struktura
Projekt přísně dodržuje pravidlo o čistém kořenovém adresáři. Všechny pomocné soubory jsou uloženy v projektové složce:

*   `bot.py`: Hlavní spustitelný skript.
*   `zpracovane_odkazy.txt`: Databáze historie (generuje se automaticky).
*   `.env`: Konfigurační soubor s API klíči (ignorováno v Gitu).
*   `02_web_scraper_ai_projekt.md`: Tato dokumentace.

---

## ⚠️ Správa chyb
V případě pádu bot vygeneruje podrobný **Crash Report** ve složce `crash_reports`, který obsahuje čas chyby, traceback a popis výjimky pro snadný debugging.
