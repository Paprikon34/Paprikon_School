import sys
import requests
from bs4 import BeautifulSoup
import time
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Načtení skrytého API klíče
load_dotenv()

# ================= KONFIGURACE =================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

URL_HLAVNI_STRANKA = "https://erudios.com/"
URL_HODNOCENI = "https://erudios.com/student_hodnoceni"
STUDENT_JMENO = "Paprikon34"

# Nastavení Groq klienta
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant" 

HISTORIE_SOUBOR = os.path.join(SCRIPT_DIR, "zpracovane_odkazy.txt")
CEKACI_DOBA_HODIN = 0
# ===============================================

"""
Tento skript (bot) automaticky kontroluje web Erudios pro nové úkoly, 
analyzuje je pomocí AI (Groq/Llama) a automaticky opravuje kód.

This script (bot) automatically checks the Erudios website for new tasks,
analyzes them using AI (Groq/Llama), and automatically fixes the code.
"""


def ask_groq(prompt, system_prompt="Jsi zkušený senior vývojář.", temperature=0.2):
    """
    Odešle dotaz na Groq API.
    Sends a query to the Groq API.
    
    Args:
        prompt: Text dotazu / The query text.
        system_prompt: Role pro AI / The role for the AI.
        temperature: Míra kreativity (0 = přesné, 1 = kreativní) / Creativity level.
    """
    print("🧠 Cloudový Mozek (Groq) přemýšlí...")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL_NAME,
            temperature=temperature,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Připojení na Groq se nezdařilo: {e}")
        return None

def nacti_historii():
    """
    Načte seznam již zpracovaných odkazů ze souboru.
    Loads the list of already processed links from a file.
    """
    if os.path.exists(HISTORIE_SOUBOR):
        with open(HISTORIE_SOUBOR, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())
    return set()

def uloz_do_historie(link):
    """
    Uloží zpracovaný odkaz do historie, aby se neopakoval.
    Saves the processed link to history to avoid duplication.
    """
    with open(HISTORIE_SOUBOR, "a", encoding="utf-8") as f:
        f.write(link + "\n")

def najdi_kritiku(url):
    """
    Prohledá web a najde odkazy, které se týkají studenta.
    Scans the web and finds links related to the student.
    """
    print(f"🌐 Hledám nové hodnocení/kritiku pro '{STUDENT_JMENO}' na adrese {url} ...")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Nelze navázat spojení s Erudios: {e}")
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')
    nalezene_odkazy = []
    
    # Prohledá všechny <a href="...">, jestli v nich nebo jejich textu není jméno "Paprikon34"
    for a_tag in soup.find_all('a', href=True):
        if STUDENT_JMENO.lower() in a_tag.text.lower() or STUDENT_JMENO.lower() in a_tag['href'].lower():
            link = a_tag['href']
            if link.startswith('/'):
                link = "https://erudios.com" + link
            nalezene_odkazy.append(link)
            
    return set(nalezene_odkazy)

def stahni_text(url):
    """
    Stáhne a vyčistí text (zadání) z konkrétní URL.
    Downloads and cleans the text (assignment) from a specific URL.
    """
    print(f"📖 Stahuji zadání z odkazu: {url} ...")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Nelze stáhnout {url}: {e}")
        return ""
        
    soup = BeautifulSoup(response.text, 'html.parser')
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.extract()
    return soup.get_text(separator='\n', strip=True)

def proved_git_commit(commit_zprava, pockat_hodin=0):
    """
    Automatizuje proces odeslání změn na GitHub.
    Automates the process of pushing changes to GitHub.
    
    Args:
        commit_zprava: Zpráva pro commit / Commit message.
        pockat_hodin: Čas, po který má bot čekat před odesláním / Delay in hours.
    """
    if pockat_hodin > 0:
        print(f"⏳ Čekám {pockat_hodin} hodin dle školních pravidel...")
        time.sleep(pockat_hodin * 3600)

    print(f"🔨 Provádím GIT akce s commit zprávou: '{commit_zprava}'")
    try:
        # Přesun o složku výš do kořene gitu přes konkrétní absolutní cestu
        subprocess.run(["git", "add", "."], check=True, cwd=REPO_ROOT)
        subprocess.run(["git", "commit", "-m", commit_zprava], check=True, cwd=REPO_ROOT)
        subprocess.run(["git", "push"], check=True, cwd=REPO_ROOT)
        print("✅ Úspěch: Kód odeslán na GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git neměl co poslat nebo došlo k chybě: {e}")

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"--- 🤖 Erudios Auto-Bot (Verze: GROQ) spuštěn (Cíl: {STUDENT_JMENO}) ---")
    
    if not GROQ_API_KEY:
        print("❌ Chybí API klíč v souboru .env!")
        return

    historie = nacti_historii()
    vsechny_odkazy = najdi_kritiku(URL_HLAVNI_STRANKA)
    nove_odkazy = vsechny_odkazy - historie
    
    if not nove_odkazy:
        print("🛏️ Žádné nové úkoly. Bot jde spát.")
        return
        
    for link in nove_odkazy:
        print(f"\n[!NALEZEN URGENTNÍ ÚKOL!] {link}")
        text_zadani = stahni_text(link)
        
        if len(text_zadani) < 20: continue
            
        print("🧠 Probouzím Llama-3-70B model na Groq...")
        
        # Analyzujeme o jaký projekt/soubor jde
        system_pro_analyzu = "Jsi bystrý IT manažer. Ze slovního hodnocení učitele zjisti, do kterého Python projektu (názvy složek začínají většinou 01_ atd.) kritika míří."
        prompt_analyza = f"Kritika z webu zní takto:\n{text_zadani[:1500]}\n\nOdpověz JEN stručným odhadem názvu souboru, který učitel chce opravit (např. 01_kamen_nuzky_papir/main.py). Pokud nevíš, napiš 'nerozpoznano.py'."
        
        odhad_souboru = ask_groq(prompt_analyza, system_pro_analyzu)
        if odhad_souboru is None:
            odhad_souboru = "nerozpoznano.py"
        else:
            odhad_souboru = odhad_souboru.strip()
            
        print(f"🔎 AI si myslí, že potřebujeme upravit hru/soubor: {odhad_souboru}")
        
        stavajici_kod = ""
        cesta_k_souboru = os.path.join(REPO_ROOT, odhad_souboru)
        if "nerozpoznano" not in odhad_souboru and os.path.exists(cesta_k_souboru):
            try:
                with open(cesta_k_souboru, "r", encoding="utf-8") as f:
                    stavajici_kod = f.read()
                print(f"📖 Původní kód úspěšně načten z {odhad_souboru}.")
            except Exception as e:
                print(f"⚠️ Nelze přečíst původní soubor: {e}")

        # Samotný kód
        if stavajici_kod:
            prompt_kod = f"Toto je současný kód v souboru {odhad_souboru}:\n```python\n{stavajici_kod}\n```\n\nToto je kritika/zadání od učitele:\n\n{text_zadani[:2000]}\n\nUprav současný kód tak, aby vyřešil problémy zmíněné v kritice. ZACHOVEJ zbytek kódu nedotčený. Napiš mi VÝHRADNĚ kompletní funkční kód v Pythonu (celý upravený soubor). Bez žádného dodatečného vysvětlování, vygeneruj čistý kód."
        else:
            prompt_kod = f"Toto je IT zadání od učitele:\n\n{text_zadani[:2000]}\n\nNapiš mi pouze kompletní funkční kód v Pythonu, který problém vyřeší. Bez žádného vysvětlování, vygeneruj čístý kód připravený k uložení."
        
        opraveny_kod = ask_groq(prompt_kod, system_prompt="Jsi senior Python inženýr.")
        
        if opraveny_kod is None:
            print("❌ AI nevrátila žádný kód.")
            continue
            
        # Očistíme od Markdown syntaxe z Groqu
        if opraveny_kod.startswith("```python"):
            opraveny_kod = opraveny_kod.replace("```python\n", "").replace("```", "")
        # Někdy vrátí jen ``` bez python
        if opraveny_kod.startswith("```"):
            opraveny_kod = opraveny_kod.replace("```\n", "").replace("```", "")
        
        if opraveny_kod:
            # Uložení kódu
            # Určení cesty pro uložení / Determining the save path
            if "nerozpoznano" not in odhad_souboru:
                adresar = os.path.dirname(odhad_souboru) # Např. 01_kamen_nuzky_papir
                soubor = os.path.basename(odhad_souboru) # Např. main.py
                # Uložíme jako "edited_main.py" vedle originálu
                cesta = os.path.join(REPO_ROOT, adresar, f"edited_{soubor}")
            else:
                # Pokud nevíme kam, uložíme do kořene
                cesta = os.path.join(REPO_ROOT, "novy_kod_z_hodnoceni.py")
                
            try:
                os.makedirs(os.path.dirname(cesta), exist_ok=True)
                with open(cesta, "w", encoding="utf-8") as f:
                    f.write(opraveny_kod)
                print(f"💾 Nový kód uložen do: {cesta}")
                
                # Commit zpráva
                prompt_commit = f"Tohle se změnilo v kódu:\n{opraveny_kod[:500]}\nNapíšeš mi jednovětou git commit zprávu česky v trpném rodě a minulém čase? POUZE zprávu bez uvozovek."
                commit_zprava = ask_groq(prompt_commit, "Git expert.").strip("\"'")
                
                # Zpožděný commit
                proved_git_commit(commit_zprava, pockat_hodin=CEKACI_DOBA_HODIN)
                uloz_do_historie(link)
                
            except Exception as e:
                print(f"❌ Nelze zapsat: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        crash_dir = os.path.join(SCRIPT_DIR, "crash_reports")
        os.makedirs(crash_dir, exist_ok=True)
        crash_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        crash_file = os.path.join(crash_dir, f"crash_report_{crash_time}.txt")
        
        print(f"\n[!!! FATAL ERROR !!!] Aplikace spadla! Vytvářím crash report: {crash_file}")
        try:
            with open(crash_file, "w", encoding="utf-8") as f:
                f.write(f"=== CRASH REPORT ===\n")
                f.write(f"Čas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Chyba: {str(e)}\n\n")
                f.write("=== TRACEBACK ===\n")
                f.write(traceback.format_exc())
            print("Crash report úspěšně vytvořen.")
        except Exception as file_err:
            print(f"Chyba při zapisování crash reportu: {file_err}")
            print(traceback.format_exc())
        sys.exit(1)
