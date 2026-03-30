# --- IMPORTY / LIBRARIES ---
import os      # Práce se soubory a cestami / File and path management
import random  # Náhodný výběr pro počítač / Random choice for the PC
import pygame  # Hlavní knihovna pro tvorbu her / Main game library
import sys     # Systémové funkce (např. ukončení programu) / System functions
from typing import Optional, List, Dict, Any, Union, cast # Typové anotace / Type hints



# Skryje zprávu o verzi Pygame v konzoli / Hides the Pygame version message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# --- CONSTANTS AND CONFIGURATION ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Color palettes for light/dark modes
THEMES = {
    "dark": {
        "bg": (20, 24, 35),
        "card_bg": (35, 40, 55),
        "accent": (14, 164, 233),
        "text": (240, 240, 240),
        "highlight": (45, 50, 70),
        "shadow": (10, 12, 18)
    },
    "light": {
        "bg": (240, 245, 250),
        "card_bg": (255, 255, 255),
        "accent": (14, 164, 233),
        "text": (30, 40, 50),
        "highlight": (225, 235, 245),
        "shadow": (210, 215, 225)
    }
}

# Definice herních tahů / Possible moves
CHOICES = ["rock", "paper", "scissors"]

def get_asset_path(filename: str) -> str:
    """
    Vypočítá absolutní cestu k obrázku. To je důležité, aby hra 
    našla obrázky bez ohledu na to, odkud ji spustíš.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__)) # Cesta ke složce s tímto skriptem
    return os.path.join(base_dir, 'assets', filename)      # Spojení cesty se složkou 'assets'

class Game:
    """
    Hlavní třída hry, která spravuje stav, vykreslování a události.
    Main game class that manages state, rendering, and events.
    """
    def __init__(self):
        """ Inicializace všeho potřebného při spuštění. """
        pygame.init() # Zapne všechny moduly Pygame
        
        # Vytvoření okna / Create window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Kámen, nůžky, papír")
        
        # Hodiny pro hlídání rychlosti hry (FPS) / Game clock
        self.clock = pygame.time.Clock()
        self.running = True # Pokud je True, hra běží. Pokud False, hra se zavře.
        
        # --- STAV HRY / GAME STATE ---
        self.current_theme = "dark" # Aktuální barevný motiv
        self.fps_cap = 60           # Limit snímků za sekundu
        self.in_settings = False    # Je otevřené menu nastavení?
        
        self.player_score: int = 0       # Body hráče
        self.computer_score: int = 0     # Body počítače
        self.last_player_choice: Optional[str] = None   # Poslední tah hráče
        self.last_computer_choice: Optional[str] = None # Poslední tah počítače
        self.result_text: str = "Vyber si svůj tah!" # Text uprostřed obrazovky

        
        # Načtení písem (fontů) / Load fonts
        try:
            # Zkusíme standardní Arial
            self.title_font = pygame.font.SysFont("arial", 42, bold=True)
            self.text_font = pygame.font.SysFont("arial", 24)
            self.score_font = pygame.font.SysFont("arial", 32, bold=True)
        except Exception:
            # Pokud není Arial, použijeme výchozí tah Pygame
            self.title_font = pygame.font.Font(None, 48)
            self.text_font = pygame.font.Font(None, 24)
            self.score_font = pygame.font.Font(None, 36)
            
        self.assets = {} # Tady budou uložené všechny obrázky
        self.load_all_assets()
        
        # --- UI LAYOUT ---
        self.buttons: List[Dict[str, Any]] = [
            {"id": "rock", "rect": pygame.Rect(100, 420, 180, 140)},
            {"id": "paper", "rect": pygame.Rect(310, 420, 180, 140)},
            {"id": "scissors", "rect": pygame.Rect(520, 420, 180, 140)}
        ]

        
        self.settings_btn_rect = pygame.Rect(WINDOW_WIDTH - 65, 25, 40, 40)
        
        # Settings Menu Layout
        btn_w, btn_h = 240, 60
        start_y = 170
        gap = 75
        cx = WINDOW_WIDTH // 2 - btn_w // 2
        
        self.settings_buttons: List[Dict[str, Any]] = [
            {"id": "theme", "rect": pygame.Rect(cx, start_y, btn_w, btn_h), "label": "Přepnout motiv"},
            {"id": "fps", "rect": pygame.Rect(cx, start_y + gap, btn_w, btn_h), "label": "Neomezené FPS: Vyp"},
            {"id": "reset", "rect": pygame.Rect(cx, start_y + gap*2, btn_w, btn_h), "label": "Reset skóre"},
            {"id": "exit", "rect": pygame.Rect(cx, start_y + gap*3, btn_w, btn_h), "label": "Ukončit hru"}
        ]

        
    def load_all_assets(self):
        """
        Načte všechny obrázky pro hru (tahy a ikony).
        Loads all gameplay images (moves and icons).
        """
        for choice in CHOICES:
            self.assets[choice] = self.load_asset(f"{choice}.png", (100, 100))
        
        # Ikony pro nastavení a UI / UI and Settings icons
        self.assets['settings'] = self.load_asset("settings.png", (24, 24))
        self.assets['theme'] = self.load_asset("theme.png", (28, 28))
        self.assets['reset'] = self.load_asset("reset.png", (28, 28))
        self.assets['exit'] = self.load_asset("exit.png", (28, 28))
                
    def load_asset(self, filename, size):
        """
        Pokusí se načíst obrázek. Pokud neexistuje, vytvoří náhradní povrch.
        Attempts to load an image. If it fails, returns a fallback surface.
        """
        path = get_asset_path(filename)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.smoothscale(img, size)
            except Exception:
                pass
        return self.create_fallback_surface(size)
                
    def create_fallback_surface(self, size):
        """Placeholder for missing graphics."""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surf, (150, 150, 150), (size[0]//2, size[1]//2), size[0]//2 - 5)
        return surf

    def play(self, player_choice: str):
        """ Tato funkce se spustí, když klikneš na Kámen, Nůžky nebo Papír. """
        self.last_player_choice = player_choice # Uložíme tvou volbu
        self.last_computer_choice = random.choice(CHOICES) # PC si náhodně vylosuje svůj tah
        
        # Logika vyhodnocení / Win logic
        if self.last_player_choice == self.last_computer_choice:
            self.result_text = "Je to remíza!" # Stejné tahy
            
        elif (self.last_player_choice == "rock" and self.last_computer_choice == "scissors") or \
             (self.last_player_choice == "paper" and self.last_computer_choice == "rock") or \
             (self.last_player_choice == "scissors" and self.last_computer_choice == "paper"):
            # Kombinace, kdy hráč vyhrává
            self.result_text = "Vyhrál jsi!"
            self.player_score += 1 # Přičteme bod hráči
            
        else:
            # Všechny ostatní případy znamenají výhru PC
            self.result_text = "Počítač vyhrál!"
            self.computer_score += 1 # Přičteme bod PC

    def handle_events(self):
        """ Tady hra naslouchá tvým akcím (myš, klávesnice). """
        for event in pygame.event.get():
            # Kliknutí na křížek okna / Window close button
            if event.type == pygame.QUIT:
                self.running = False
            
            # Jakékoliv kliknutí myší / Any mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 1 = Levé tlačítko myši
                    mouse_pos = pygame.mouse.get_pos() # Zjistíme souřadnice kde jsi klikl
                    
                    if not self.in_settings:
                        # Reakce na ikonu nastavení / Open settings
                        if self.settings_btn_rect.collidepoint(mouse_pos):
                            self.in_settings = True
                        else:
                            # Kontrola, jestli jsi klikl na tlačítko Kámen, Nůžky nebo Papír
                            for btn in self.buttons:
                                # Explicitly ensure we have a dict with a Rect
                                if isinstance(btn, dict) and "rect" in btn:
                                    rect = btn["rect"]
                                    if hasattr(rect, "collidepoint") and rect.collidepoint(mouse_pos):
                                        self.play(btn["id"])

                    else:
                        # Pokud jsme v NESTAVENÍ / Handling settings menu
                        if self.settings_btn_rect.collidepoint(mouse_pos):
                            self.in_settings = False # Zavření nastavení křížkem
                            
                        for btn in self.settings_buttons:
                            if btn["rect"].collidepoint(mouse_pos):
                                if btn["id"] == "theme":
                                    # Přepínání Temný/Světlý režim
                                    self.current_theme = "light" if self.current_theme == "dark" else "dark"
                                elif btn["id"] == "fps":
                                    # Zapne nebo vypne limit 60 FPS
                                    self.fps_cap = 0 if self.fps_cap == 60 else 60
                                    stat = "Zap" if self.fps_cap == 0 else "Vyp"
                                    btn["label"] = f"Neomezené FPS: {stat}"
                                elif btn["id"] == "reset":
                                    # Nulování výsledků
                                    self.player_score = 0
                                    self.computer_score = 0
                                    self.last_player_choice = None
                                    self.last_computer_choice = None
                                    self.result_text = "Vyber si svůj tah!"
                                    self.in_settings = False
                                elif btn["id"] == "exit":
                                    # Úplné vypnutí hry
                                    self.running = False

    def draw(self):
        """ Tady se všechno kreslí na obrazovku. Pygame kreslí ve vrstvách. """
        theme = THEMES[self.current_theme]
        self.screen.fill(theme["bg"]) # 1. Vrstva: Pozadí / Background
        
        # --- UI: SCORE BOARD (Tabulka se skóre) ---
        score_bg_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 60, 300, 80)
        pygame.draw.rect(self.screen, theme["card_bg"], score_bg_rect, border_radius=15)
        
        # Vykreslení čísel skóre
        score_text = f"{self.player_score}  :  {self.computer_score}"
        score_surf = self.score_font.render(score_text, True, theme["accent"])
        score_rect = score_surf.get_rect(center=score_bg_rect.center)
        self.screen.blit(score_surf, score_rect)
        
        # Texty "Hráč" a "PC"
        player_lbl = self.text_font.render("Hráč", True, theme["text"])
        self.screen.blit(player_lbl, (score_bg_rect.left + 20, score_bg_rect.centery - 10))
        
        comp_lbl = self.text_font.render("PC", True, theme["text"])
        self.screen.blit(comp_lbl, (score_bg_rect.right - 50, score_bg_rect.centery - 10))
        
        # --- UI: BATTLE AREA (Zobrazení vybraných tahů) ---
        # Pokud už proběhlo kolo, ukážeme co kdo hodil
        if self.last_player_choice is not None and self.last_computer_choice is not None:
            # Narrow types for the type checker
            p_choice = cast(str, self.last_player_choice)
            c_choice = cast(str, self.last_computer_choice)
            
            p_img = self.assets.get(p_choice) # Obrázek tvého tahu
            if p_img:
                self.screen.blit(p_img, (WINDOW_WIDTH // 2 - 160, 200))
            
            vs_surf = self.text_font.render("VS", True, (150, 150, 150))
            self.screen.blit(vs_surf, (WINDOW_WIDTH // 2 - 15, 235))
            
            c_img = self.assets.get(c_choice) # Obrázek PC tahu
            if c_img:
                self.screen.blit(c_img, (WINDOW_WIDTH // 2 + 60, 200))



        
        # --- UI: RESULT MESSAGE (Text s výsledkem) ---
        # Např. "Vyhrál jsi!" nebo "Remíza!"
        res_surf = self.text_font.render(self.result_text, True, theme["text"])
        res_rect = res_surf.get_rect(center=(WINDOW_WIDTH // 2, 350))
        self.screen.blit(res_surf, res_rect)
        
        # --- UI: GAME BUTTONS (Tlačítka pro volbu: Kámen, Nůžky, Papír) ---
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            # Check if rect attribute is available and call collidepoint safely
            rect = btn.get("rect")
            if rect is None: continue
            
            is_hovered = hasattr(rect, "collidepoint") and rect.collidepoint(mouse_pos) and not self.in_settings
            color = theme["highlight"] if is_hovered else theme["card_bg"]
            
            # Shadow (Stín tlačítka)
            if hasattr(rect, "copy"):
                shadow_rect = rect.copy()
                shadow_rect.y += 4
                pygame.draw.rect(self.screen, theme["shadow"], shadow_rect, border_radius=12)
            
            # Main Button (Samotné tlačítko)
            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            if is_hovered:
                pygame.draw.rect(self.screen, theme["accent"], rect, 2, border_radius=12)
            
            # Asset (Obrázek tahu)
            img = self.assets.get(btn["id"])
            if img:
                img_rect = img.get_rect(center=rect.center)
                self.screen.blit(img, img_rect)


            
        # --- UI: SETTINGS ICON (Ikona ozubeného kolečka) ---
        set_hover = self.settings_btn_rect.collidepoint(mouse_pos) and not self.in_settings
        set_color = theme["highlight"] if set_hover else theme["card_bg"]
        pygame.draw.rect(self.screen, set_color, self.settings_btn_rect, border_radius=8)
        
        set_img = self.assets['settings']
        self.screen.blit(set_img, set_img.get_rect(center=self.settings_btn_rect.center))

        # --- SETTINGS OVERLAY (Menu nastavení) ---
        if self.in_settings:
            # Semi-transparent dark overlay (Ztmavení pozadí)
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            # Modal Menu Card (Karta menu)
            menu_w, menu_h = 320, 420
            menu_rect = pygame.Rect(WINDOW_WIDTH//2 - menu_w//2, WINDOW_HEIGHT//2 - menu_h//2, menu_w, menu_h)
            pygame.draw.rect(self.screen, theme["card_bg"], menu_rect, border_radius=20)
            pygame.draw.rect(self.screen, theme["accent"], menu_rect, 2, border_radius=20)
            
            title_surf = self.title_font.render("Nastavení", True, theme["text"])
            self.screen.blit(title_surf, title_surf.get_rect(center=(WINDOW_WIDTH//2, menu_rect.top + 45)))

            # Tlačítka v nastavení / Buttons in settings
            for btn in self.settings_buttons:
                rect = btn.get("rect")
                if rect is None: continue
                
                is_hovered = hasattr(rect, "collidepoint") and rect.collidepoint(mouse_pos)
                b_color = theme["highlight"] if is_hovered else theme["bg"]
                
                pygame.draw.rect(self.screen, b_color, rect, border_radius=10)
                if is_hovered:
                    pygame.draw.rect(self.screen, theme["accent"], rect, 1, border_radius=10)
                
                # Check if icon exists and draw it
                if btn["id"] in self.assets:
                    icon = self.assets[btn["id"]]
                    # Safe access to rect properties
                    if icon and hasattr(rect, "left") and hasattr(rect, "centery"):
                        self.screen.blit(icon, (rect.left + 20, rect.centery - icon.get_height()//2))
                        lbl_x = rect.left + 65
                    else:
                        lbl_x = rect.centerx # Use rect centerx as fallback
                else:
                    lbl_x = rect.centerx

                
                # Text na tlačítku / Button text
                lbl_surf = self.text_font.render(btn["label"], True, theme["text"])
                if btn["id"] in self.assets and self.assets[btn["id"]]:
                    self.screen.blit(lbl_surf, (lbl_x, rect.centery - lbl_surf.get_height()//2))
                else:
                    self.screen.blit(lbl_surf, lbl_surf.get_rect(center=rect.center))



        # --- UI: FPS (Počítadlo snímků za sekundu) ---
        fps_text = f"FPS: {int(self.clock.get_fps())}"
        fps_surf = self.text_font.render(fps_text, True, (150, 150, 150))
        self.screen.blit(fps_surf, (15, WINDOW_HEIGHT - 35))
        
        pygame.display.flip()

    def run(self):
        """ Srdce hry - nekonečný cyklus, který běží dokud hru nevypneš. """
        while self.running:
            self.handle_events() # 1. Zjisti, co uživatel dělá / Get input
            self.draw()          # 2. Nakresli obrázek / Render graphics
            self.clock.tick(self.fps_cap) # 3. Počkej chvilku, ať hra neběží moc rychle / Maintain FPS
        
        pygame.quit() # Úklid Pygame před vypnutím
        sys.exit()    # Úplné zavření procesu Pythonu

# --- START PROGRAMU / SCRIPT START ---
if __name__ == "__main__":
    game = Game() # Vytvoříme objekt naší hry
    game.run()    # Spustíme hlavní smyčku