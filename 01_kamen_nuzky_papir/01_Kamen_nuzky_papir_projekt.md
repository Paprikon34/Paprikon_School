# Kámen, nůžky, papír

Tento dokument slouží jako podrobný průvodce kódem a strukturou projektu „Kámen, nůžky, papír“ s grafickým rozhraním v Pythonu.

## Popis a cíl projektu
Cílem bylo vytvořit moderní verzi klasické hry s využitím knihovny **Pygame**. Program je navržen tak, aby byl vizuálně atraktivní, intuitivně ovladatelný a technicky správně strukturovaný podle standardů studentské práce.

## Funkcionalita programu
Program je klasická hra "kámen, nůžky, papír" s grafickým rozhraním. Hráč volí kliknutím na interaktivní tlačítka s hover efekty. Podporuje Dark/Light mode, neomezené FPS a ukládání herní statistiky. Aplikace také bezpečně obsluhuje načítání grafických aktivních prvků a generuje náhradní grafiku v případě chybějících souborů.

## Technická část

### Architektura programu
Program využívá **objektově orientované programování (OOP)**. Celá hra je zapouzdřena ve třídě `Game`, což zajišťuje přehlednost a snadnou správu stavu hry (skóre, herní volby).

### Použité technologie:
- **Python 3.14+**: Nejnovější verze interpretu.
- **Pygame-ce**: Komunitní edice knihovny Pygame pro vykreslování grafiky a zpracování událostí.
- **Modul `random`**: Pro generování náhodných tahů počítače.
- **Modul `os`**: Pro bezpečnou práci s cestami k souborům (ikony v `assets`).

---

### Rozbor klíčových částí kódu

#### Inicializace a nastavení (`__init__`)
V této části nastavujeme okno, fonty a základní proměnné.
```python
def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((800, 600))
    # Definice tlačítek pomocí seznamu slovníků pro snadnou iteraci při vykreslování
    self.buttons = [
        {"id": "rock", "rect": pygame.Rect(100, 420, 180, 140)},
        {"id": "paper", "rect": pygame.Rect(310, 420, 180, 140)},
        {"id": "scissors", "rect": pygame.Rect(520, 420, 180, 140)}
    ]
```
*Proč toto řešení?* Použití `pygame.Rect` nám později umožňuje velmi jednoduše detekovat kolizi myši s tlačítkem.

#### Herní logika (`play`)
Tato funkce je srdcem hry. Spustí se pokaždé, když hráč klikne na tlačítko.
```python
def play(self, player_choice: str):
    self.last_player_choice = player_choice
    self.last_computer_choice = random.choice(CHOICES)
    
    # Logika vyhodnocení vítěze
    if self.last_player_choice == self.last_computer_choice:
        self.result_text = "Je to remíza!"
    elif (self.last_player_choice == "rock" and self.last_computer_choice == "scissors") or \
         (self.last_player_choice == "paper" and self.last_computer_choice == "rock") or \
         (self.last_player_choice == "scissors" and self.last_computer_choice == "paper"):
        self.result_text = "Vyhrál jsi!"
        self.player_score += 1
    else:
        self.result_text = "Počítač vyhrál!"
        self.computer_score += 1
```
*Vysvětlení:* Počítač si náhodně vybere z listu `["rock", "paper", "scissors"]`. Následně porovnáme volby pomocí podmínek, které pokrývají všechny tři možnosti výhry hráče. V ostatních případech (kromě remízy) vyhrává počítač.

#### Vykreslovací smyčka (`draw`)
Zde vytváříme grafické rozhraní. Aplikujeme zde tzv. **double buffering** (funkce `pygame.display.flip()`), který zabraňuje blikání obrazu.
- **Zpracování barev**: Používáme moderní hexadecimální převody do RGB (např. tmavé pozadí `(20, 24, 35)`).
- **Hover efekt**: 
```python
is_hovered = btn["rect"].collidepoint(mouse_pos) and not self.in_settings
color = theme["highlight"] if is_hovered else theme["card_bg"]
```
*Vysvětlení:* Pokud se souřadnice myši nacházejí uvnitř obdélníku tlačítka (a současně nejsme v menu nastavení), tlačítko se vybarví světlejší barvou z aktuálního motivu (`highlight`), což dává uživateli zpětnou vazbu.

#### Tématické přepínání (Dark/Light mode)
Hra nyní podporuje dva vizuální režimy:
- **Dark Mode (výchozí)**: Optimalizováno pro šetření zraku, využívá tmavě modré a šedé odstíny.
- **Light Mode**: Klasický světlý vzhled s vysokým kontrastem.

#### Menu nastavení
Nové rozhraní přístupné přes ikonu ozubeného kolečka v pravém horním rohu. Menu obsahuje:
- **Změna motivu**: Přepínání barev za běhu.
- **Neomezené FPS**: Možnost vypnout limit 60 FPS pro maximální výkon s ukazatelem aktuální snímkové frekvence v levém dolním rohu.
- **Reset skóre**: Vynuluje statistiky.
- **Ukončení hry**: Bezpečné zavření aplikace.

#### Zpracování chyb a pádů

---

### Uživatelská příručka
1. **Spuštění**: Spusťte skript `main.py` ve složce projektu.
2. **Průběh**: Uvidíte tři velká tlačítka s ikonami. Kliknutím levým tlačítkem myši provedete svůj tah.
3. **Cíl**: Získejte co nejvyšší skóre. Skóre se ukládá po dobu běhu programu.
4. **Ukončení**: Zavřete okno křížkem v horním rohu.
5. **V případě chyby**: Pokud aplikace spadne, zkontrolujte soubor `crash_report.txt` v hlavním adresáři projektu.

---

### Správa aktiv a cest
Obrázky jsou uloženy v podsložce `assets`. Aby program fungoval správně i po přesunu do jiné složky, používáme **dynamické určování absolutní cesty**:

```python
# Získání absolutní cesty k adresáři, kde se nachází tento skript
base_dir = os.path.dirname(os.path.abspath(__file__))
# Dynamické sestavení cesty k obrázku
path = os.path.join(base_dir, "assets", f"{choice}.png")
```

Pokud by soubor přesto chyběl (např. smazání uživatelem), kód obsahuje **fallback mechanismus**:
```python
    def load_asset(self, filename, size):
        path = get_asset_path(filename)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.smoothscale(img, size)
            except Exception:
                pass
        return self.create_fallback_surface(size)
        
    def create_fallback_surface(self, size):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surf, (150, 150, 150), (size[0]//2, size[1]//2), size[0]//2 - 5)
        return surf
```
Toto řešení zajišťuje maximální stabilitu aplikace a přenositelnost. Nově přidané globální ošetření chyb doplňuje tento mechanismus o ochranu proti pádům způsobeným jinými faktory (např. chybějící systémové fonty nebo ovladače).
