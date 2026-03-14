import pygame
import random
import os
import sys
import traceback
import tkinter as tk
from tkinter import messagebox

# Configuration
WIDTH, HEIGHT = 800, 600
FPS = 60

# Theme Definitions
THEMES = {
    "dark": {
        "background": (20, 24, 35),
        "card": (30, 35, 48),
        "text": (240, 240, 240),
        "text_dim": (160, 160, 170),
        "accent": (74, 144, 226),
        "success": (46, 204, 113),
        "danger": (231, 76, 60)
    },
    "light": {
        "background": (240, 240, 240),
        "card": (210, 215, 230),
        "text": (20, 24, 35),
        "text_dim": (80, 80, 90),
        "accent": (50, 120, 200),
        "success": (39, 174, 96),
        "danger": (192, 57, 43)
    }
}

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rock Paper Scissors Ultra")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Segoe UI", 64, bold=True)
        self.font_medium = pygame.font.SysFont("Segoe UI", 32)
        self.font_small = pygame.font.SysFont("Segoe UI", 24)
        
        # Theme and State
        self.current_theme = "dark"
        self.colors = THEMES[self.current_theme]
        self.state = "playing" # playing, settings
        self.unlimited_fps = False
        self.current_fps = FPS
        
        # Load Assets
        self.assets = {}
        self.load_images()
        
        self.player_score = 0
        self.computer_score = 0
        self.last_player_choice = None
        self.last_computer_choice = None
        self.result_text = "Vyber si!"
        self.result_color = self.colors["text"]
        
        # Choices
        self.choices = ["rock", "paper", "scissors"]
        
        # Button Setup
        button_y = 420
        self.buttons = [
            {"id": "rock", "rect": pygame.Rect(100, button_y, 180, 140)},
            {"id": "paper", "rect": pygame.Rect(310, button_y, 180, 140)},
            {"id": "scissors", "rect": pygame.Rect(520, button_y, 180, 140)}
        ]
        
        # Settings Button (Top Right)
        self.settings_btn = pygame.Rect(WIDTH - 70, 15, 50, 50)
        
        # Settings Menu Buttons
        self.menu_buttons = [
            {"id": "theme", "rect": pygame.Rect(WIDTH//2 - 140, 160, 280, 50), "label": "ZMĚNIT MOTIV"},
            {"id": "fps", "rect": pygame.Rect(WIDTH//2 - 140, 230, 280, 50), "label": "NEOMEZENÉ FPS: VYP"},
            {"id": "reset", "rect": pygame.Rect(WIDTH//2 - 140, 300, 280, 50), "label": "RESETOVAT SKÓRE"},
            {"id": "exit", "rect": pygame.Rect(WIDTH//2 - 140, 370, 280, 50), "label": "UKONČIT HRU"},
            {"id": "back", "rect": pygame.Rect(WIDTH//2 - 140, 450, 280, 50), "label": "ZPĚT"}
        ]
        
    def load_images(self):
        """Načte obrázky ze složky assets."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        asset_names = ["rock", "paper", "scissors", "settings", "reset", "exit", "theme"]
        for asset in asset_names:
            path = os.path.join(base_dir, "assets", f"{asset}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                # Změna velikosti podle typu assetu
                if asset in ["rock", "paper", "scissors"]:
                    self.assets[asset] = pygame.transform.smoothscale(img, (100, 100))
                else:
                    self.assets[asset] = pygame.transform.smoothscale(img, (30, 30))
            else:
                # Fallback
                surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(surf, self.colors["accent"], (50, 50), 40)
                self.assets[asset] = surf

    def play(self, player_choice):
        """
        Zpracuje tah hráče, vybere náhodný tah počítače a určí vítěze kola.
        Také aktualizuje celkové skóre a text výsledku.
        """
        self.last_player_choice = player_choice
        self.last_computer_choice = random.choice(self.choices)
        
        # Logika pro určení výsledku (Remíza / Výhra / Prohra)
        if self.last_player_choice == self.last_computer_choice:
            self.result_text = "Je to remíza!"
            self.result_color = self.colors["text_dim"]
        elif (self.last_player_choice == "rock" and self.last_computer_choice == "scissors") or \
             (self.last_player_choice == "paper" and self.last_computer_choice == "rock") or \
             (self.last_player_choice == "scissors" and self.last_computer_choice == "paper"):
            self.result_text = "Vyhrál jsi!"
            self.result_color = self.colors["success"]
            self.player_score += 1
        else:
            self.result_text = "Počítač vyhrál!"
            self.result_color = self.colors["danger"]
            self.computer_score += 1

    def draw_rounded_rect(self, surface, color, rect, radius=15):
        """Pomocná funkce pro vykreslení obdélníku se zaoblenými rohy."""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def draw(self):
        """Vykreslí rozhraní na obrazovku."""
        self.screen.fill(self.colors["background"])
        
        if self.state == "playing":
            self.draw_game()
        elif self.state == "settings":
            self.draw_settings()
            
        if self.unlimited_fps:
            fps_text = self.font_small.render(f"FPS: {int(self.clock.get_fps())}", True, self.colors["text_dim"])
            self.screen.blit(fps_text, (10, HEIGHT - 35))
            
        pygame.display.flip()

    def draw_game(self):
        """Vykreslí samotnou hru."""
        # Vykreslení horního panelu
        score_bg = pygame.Rect(0, 0, WIDTH, 80)
        pygame.draw.rect(self.screen, self.colors["card"], score_bg)
        
        player_score_text = self.font_medium.render(f"HRÁČ: {self.player_score}", True, self.colors["text"])
        computer_score_text = self.font_medium.render(f"POČÍTAČ: {self.computer_score}", True, self.colors["text"])
        self.screen.blit(player_score_text, (50, 20))
        self.screen.blit(computer_score_text, (WIDTH - computer_score_text.get_width() - 100, 20))

        # Nastavení tlačítko
        mouse_pos = pygame.mouse.get_pos()
        is_settings_hovered = self.settings_btn.collidepoint(mouse_pos)
        s_color = (self.colors["accent"][0]+20, self.colors["accent"][1]+20, self.colors["accent"][2]+20) if is_settings_hovered else self.colors["card"]
        self.draw_rounded_rect(self.screen, s_color, self.settings_btn, 10)
        self.screen.blit(self.assets["settings"], (self.settings_btn.centerx - 15, self.settings_btn.centery - 15))

        # Hlavní aréna
        if self.last_player_choice:
            player_tag = self.font_small.render("TY", True, self.colors["text_dim"])
            self.screen.blit(player_tag, (200 - player_tag.get_width()//2, 130))
            self.screen.blit(self.assets[self.last_player_choice], (150, 160))
            
            vs_text = self.font_medium.render("VS", True, self.colors["text"])
            self.screen.blit(vs_text, (WIDTH//2 - vs_text.get_width()//2, 200))
            
            computer_tag = self.font_small.render("POČÍTAČ", True, self.colors["text_dim"])
            self.screen.blit(computer_tag, (600 - computer_tag.get_width()//2, 130))
            self.screen.blit(self.assets[self.last_computer_choice], (550, 160))
            
            res_surf = self.font_large.render(self.result_text, True, self.result_color)
            self.screen.blit(res_surf, (WIDTH//2 - res_surf.get_width()//2, 300))
        else:
            welcome = self.font_large.render("Jdeme na to?", True, self.colors["text"])
            self.screen.blit(welcome, (WIDTH//2 - welcome.get_width()//2, 200))

        for btn in self.buttons:
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            color = (self.colors["accent"][0]+20, self.colors["accent"][1]+20, self.colors["accent"][2]+20) if is_hovered else self.colors["card"]
            
            self.draw_rounded_rect(self.screen, color, btn["rect"])
            if is_hovered:
                pygame.draw.rect(self.screen, self.colors["accent"], btn["rect"], 3, border_radius=15)
            
            img = self.assets[btn["id"]]
            self.screen.blit(img, (btn["rect"].centerx - 50, btn["rect"].centery - 55))
            
            labels = {"rock": "KÁMEN", "paper": "PAPÍR", "scissors": "NŮŽKY"}
            label = self.font_small.render(labels[btn["id"]], True, self.colors["text"])
            self.screen.blit(label, (btn["rect"].centerx - label.get_width()//2, btn["rect"].bottom - 30))

    def draw_settings(self):
        """Vykreslí menu nastavení."""
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Menu box
        menu_rect = pygame.Rect(WIDTH//4, 100, WIDTH//2, 450)
        self.draw_rounded_rect(self.screen, self.colors["card"], menu_rect)
        pygame.draw.rect(self.screen, self.colors["accent"], menu_rect, 2, border_radius=15)
        
        title = self.font_medium.render("NASTAVENÍ", True, self.colors["text"])
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 130))
        
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.menu_buttons:
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            color = self.colors["accent"] if is_hovered else self.colors["background"]
            text_color = self.colors["background"] if is_hovered else self.colors["text"]
            
            self.draw_rounded_rect(self.screen, color, btn["rect"], 10)
            
            # Icon
            if btn["id"] in self.assets:
                self.screen.blit(self.assets[btn["id"]], (btn["rect"].left + 15, btn["rect"].centery - 15))
            
            label_text = btn["label"]
            if btn["id"] == "fps":
                label_text = "NEOMEZENÉ FPS: ZAP" if self.unlimited_fps else "NEOMEZENÉ FPS: VYP"
                
            label = self.font_small.render(label_text, True, text_color)
            self.screen.blit(label, (btn["rect"].centerx - label.get_width()//2 + 15, btn["rect"].centery - label.get_height()//2))

    def run(self):
        """Hlavní herní smyčka."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Levé tlačítko
                        if self.state == "playing":
                            # Kliknutí na nastavení
                            if self.settings_btn.collidepoint(event.pos):
                                self.state = "settings"
                                continue
                                
                            # Kliknutí na herní tlačítka
                            for btn in self.buttons:
                                if btn["rect"].collidepoint(event.pos):
                                    self.play(btn["id"])
                        
                        elif self.state == "settings":
                            for btn in self.menu_buttons:
                                if btn["rect"].collidepoint(event.pos):
                                    if btn["id"] == "theme":
                                        self.current_theme = "light" if self.current_theme == "dark" else "dark"
                                        self.colors = THEMES[self.current_theme]
                                        # Update result color to match theme
                                        self.result_color = self.colors["text"]
                                    elif btn["id"] == "fps":
                                        self.unlimited_fps = not self.unlimited_fps
                                        self.current_fps = 0 if self.unlimited_fps else FPS
                                    elif btn["id"] == "reset":
                                        self.player_score = 0
                                        self.computer_score = 0
                                        self.last_player_choice = None
                                        self.last_computer_choice = None
                                        self.result_text = "Skóre resetováno!"
                                        self.state = "playing"
                                    elif btn["id"] == "exit":
                                        running = False
                                    elif btn["id"] == "back":
                                        self.state = "playing"
            
            self.draw()
            self.clock.tick(self.current_fps)
            
        pygame.quit()
        sys.exit()

def show_error_popup(error_message):
    """Zobrazí uživateli vyskakovací okno s popisem chyby."""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Kritická chyba", 
                           f"Aplikace narazila na problém a musí být ukončena.\n\n"
                           f"Detaily byly uloženy do souboru 'crash_report.txt'.\n\n"
                           f"Chyba:\n{error_message.splitlines()[-1]}")
        root.destroy()
    except:
        # Fallback pokud tkinter selže
        print(f"Kritická chyba: {error_message}", file=sys.stderr)

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception:
        # Získání celého tracebacku
        error_info = traceback.format_exc()
        
        # Zápis do logovacího souboru
        try:
            with open("crash_report.txt", "w", encoding="utf-8") as f:
                f.write("======= ROCK PAPER SCISSORS CRASH REPORT =======\n")
                f.write(f"Exception details:\n")
                f.write("-" * 40 + "\n")
                f.write(error_info)
        except:
            pass # Pokud selže i zápis do souboru, nic víc dělat nemůžeme
        
        # Zobrazení popupu
        show_error_popup(error_info)
        sys.exit(1)
