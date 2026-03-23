import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import random
import pygame
import sys

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

CHOICES = ["rock", "paper", "scissors"]

def get_asset_path(filename: str) -> str:
    """Returns absolute path to asset file"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'assets', filename)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Kámen, nůžky, papír")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # --- GAME STATE ---
        self.current_theme = "dark"
        self.fps_cap = 60
        self.in_settings = False
        
        self.player_score = 0
        self.computer_score = 0
        self.last_player_choice = None
        self.last_computer_choice = None
        self.result_text = "Vyber si svůj tah!"
        
        # Fonts
        try:
            self.title_font = pygame.font.SysFont("arial", 42, bold=True)
            self.text_font = pygame.font.SysFont("arial", 24)
            self.score_font = pygame.font.SysFont("arial", 32, bold=True)
        except Exception:
            self.title_font = pygame.font.Font(None, 48)
            self.text_font = pygame.font.Font(None, 24)
            self.score_font = pygame.font.Font(None, 36)
            
        self.assets = {}
        self.load_all_assets()
        
        # --- UI LAYOUT ---
        self.buttons = [
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
        
        self.settings_buttons = [
            {"id": "theme", "rect": pygame.Rect(cx, start_y, btn_w, btn_h), "label": "Přepnout motiv"},
            {"id": "fps", "rect": pygame.Rect(cx, start_y + gap, btn_w, btn_h), "label": "Neomezené FPS: Vyp"},
            {"id": "reset", "rect": pygame.Rect(cx, start_y + gap*2, btn_w, btn_h), "label": "Reset skóre"},
            {"id": "exit", "rect": pygame.Rect(cx, start_y + gap*3, btn_w, btn_h), "label": "Ukončit hru"}
        ]
        
    def load_all_assets(self):
        """Loads gameplay assets and UI icons safely."""
        for choice in CHOICES:
            self.assets[choice] = self.load_asset(f"{choice}.png", (100, 100))
        
        # Icons
        self.assets['settings'] = self.load_asset("settings.png", (24, 24))
        self.assets['theme'] = self.load_asset("theme.png", (28, 28))
        self.assets['reset'] = self.load_asset("reset.png", (28, 28))
        self.assets['exit'] = self.load_asset("exit.png", (28, 28))
                
    def load_asset(self, filename, size):
        """Loads and scales an image, returning a fallback if not found."""
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
        self.last_player_choice = player_choice
        self.last_computer_choice = random.choice(CHOICES)
        
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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if not self.in_settings:
                        if self.settings_btn_rect.collidepoint(mouse_pos):
                            self.in_settings = True
                        else:
                            for btn in self.buttons:
                                if btn["rect"].collidepoint(mouse_pos):
                                    self.play(btn["id"])
                    else:
                        # Close settings when clicking top-right button again
                        if self.settings_btn_rect.collidepoint(mouse_pos):
                            self.in_settings = False
                            
                        # Handle clicks on setting items
                        for btn in self.settings_buttons:
                            if btn["rect"].collidepoint(mouse_pos):
                                if btn["id"] == "theme":
                                    self.current_theme = "light" if self.current_theme == "dark" else "dark"
                                elif btn["id"] == "fps":
                                    self.fps_cap = 0 if self.fps_cap == 60 else 60
                                    stat = "Zap" if self.fps_cap == 0 else "Vyp"
                                    btn["label"] = f"Neomezené FPS: {stat}"
                                elif btn["id"] == "reset":
                                    self.player_score = 0
                                    self.computer_score = 0
                                    self.last_player_choice = None
                                    self.last_computer_choice = None
                                    self.result_text = "Vyber si svůj tah!"
                                    self.in_settings = False
                                elif btn["id"] == "exit":
                                    self.running = False

    def draw(self):
        theme = THEMES[self.current_theme]
        self.screen.fill(theme["bg"])
        
        # --- UI: SCORE BOARD ---
        score_bg_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 60, 300, 80)
        pygame.draw.rect(self.screen, theme["card_bg"], score_bg_rect, border_radius=15)
        
        score_text = f"{self.player_score}  :  {self.computer_score}"
        score_surf = self.score_font.render(score_text, True, theme["accent"])
        score_rect = score_surf.get_rect(center=score_bg_rect.center)
        self.screen.blit(score_surf, score_rect)
        
        player_lbl = self.text_font.render("Hráč", True, theme["text"])
        self.screen.blit(player_lbl, (score_bg_rect.left + 20, score_bg_rect.centery - 10))
        
        comp_lbl = self.text_font.render("PC", True, theme["text"])
        self.screen.blit(comp_lbl, (score_bg_rect.right - 50, score_bg_rect.centery - 10))
        
        # --- UI: BATTLE AREA ---
        if self.last_player_choice and self.last_computer_choice:
            p_img = self.assets[self.last_player_choice]
            self.screen.blit(p_img, (WINDOW_WIDTH // 2 - 160, 200))
            
            vs_surf = self.text_font.render("VS", True, (150, 150, 150))
            self.screen.blit(vs_surf, (WINDOW_WIDTH // 2 - 15, 235))
            
            c_img = self.assets[self.last_computer_choice]
            self.screen.blit(c_img, (WINDOW_WIDTH // 2 + 60, 200))
        
        # --- UI: RESULT MESSAGE ---
        res_surf = self.text_font.render(self.result_text, True, theme["text"])
        res_rect = res_surf.get_rect(center=(WINDOW_WIDTH // 2, 350))
        self.screen.blit(res_surf, res_rect)
        
        # --- UI: GAME BUTTONS ---
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            is_hovered = btn["rect"].collidepoint(mouse_pos) and not self.in_settings
            color = theme["highlight"] if is_hovered else theme["card_bg"]
            
            # Shadow
            shadow_rect = btn["rect"].copy()
            shadow_rect.y += 4
            pygame.draw.rect(self.screen, theme["shadow"], shadow_rect, border_radius=12)
            
            # Main Button
            pygame.draw.rect(self.screen, color, btn["rect"], border_radius=12)
            if is_hovered:
                pygame.draw.rect(self.screen, theme["accent"], btn["rect"], 2, border_radius=12)
            
            # Asset
            img = self.assets[btn["id"]]
            img_rect = img.get_rect(center=btn["rect"].center)
            self.screen.blit(img, img_rect)
            
        # --- UI: SETTINGS ICON ---
        set_hover = self.settings_btn_rect.collidepoint(mouse_pos) and not self.in_settings
        set_color = theme["highlight"] if set_hover else theme["card_bg"]
        pygame.draw.rect(self.screen, set_color, self.settings_btn_rect, border_radius=8)
        
        set_img = self.assets['settings']
        self.screen.blit(set_img, set_img.get_rect(center=self.settings_btn_rect.center))

        # --- SETTINGS OVERLAY ---
        if self.in_settings:
            # Semi-transparent dark overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            # Modal Menu Card
            menu_w, menu_h = 320, 420
            menu_rect = pygame.Rect(WINDOW_WIDTH//2 - menu_w//2, WINDOW_HEIGHT//2 - menu_h//2, menu_w, menu_h)
            pygame.draw.rect(self.screen, theme["card_bg"], menu_rect, border_radius=20)
            pygame.draw.rect(self.screen, theme["accent"], menu_rect, 2, border_radius=20)
            
            title_surf = self.title_font.render("Nastavení", True, theme["text"])
            self.screen.blit(title_surf, title_surf.get_rect(center=(WINDOW_WIDTH//2, menu_rect.top + 45)))

            for btn in self.settings_buttons:
                is_hovered = btn["rect"].collidepoint(mouse_pos)
                b_color = theme["highlight"] if is_hovered else theme["bg"]
                
                pygame.draw.rect(self.screen, b_color, btn["rect"], border_radius=10)
                if is_hovered:
                    pygame.draw.rect(self.screen, theme["accent"], btn["rect"], 1, border_radius=10)
                
                # Check if icon exists and draw it
                if btn["id"] in self.assets:
                    icon = self.assets[btn["id"]]
                    self.screen.blit(icon, (btn["rect"].left + 20, btn["rect"].centery - icon.get_height()//2))
                    lbl_x = btn["rect"].left + 65
                else:
                    lbl_x = btn["rect"].centerx
                
                # Button Text
                lbl_surf = self.text_font.render(btn["label"], True, theme["text"])
                if btn["id"] in self.assets:
                    self.screen.blit(lbl_surf, (lbl_x, btn["rect"].centery - lbl_surf.get_height()//2))
                else:
                    self.screen.blit(lbl_surf, lbl_surf.get_rect(center=btn["rect"].center))

        # --- UI: FPS ---
        fps_text = f"FPS: {int(self.clock.get_fps())}"
        fps_surf = self.text_font.render(fps_text, True, (150, 150, 150))
        self.screen.blit(fps_surf, (15, WINDOW_HEIGHT - 35))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(self.fps_cap)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()