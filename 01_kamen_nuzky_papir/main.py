import os
import pygame
import pygame.image

# Funkce pro načítání obrázku pomocí script-relative path
def load_image(image_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, 'assets', image_path)
    return pygame.image.load(image_path)

# Funkce pro načítání assetů pomocí script-relative path
def load_assets():
    rock_image = load_image('rock.png')
    paper_image = load_image('paper.png')
    scissors_image = load_image('scissors.png')
    return rock_image, paper_image, scissors_image

# Funkce pro inicializaci projektu
def init_project():
    # Vytvoření prázdné dokumentace a hlavních souborů
    with open('dokumentace.md', 'w') as f:
        f.write('')

    with open('main.py', 'w') as f:
        f.write('')

    # Přidání požadavků ke studentským pracím
    with open('požadavky.md', 'w') as f:
        f.write('')

    # Přidání projektových souborů
    with open('01_kamen_nuzky_papir/README.md', 'w') as f:
        f.write('')

    with open('01_kamen_nuzky_papir/main.py', 'w') as f:
        f.write('')

    with open('01_kamen_nuzky_papir/assets/rock.png', 'w') as f:
        f.write('')

    with open('01_kamen_nuzky_papir/assets/paper.png', 'w') as f:
        f.write('')

    with open('01_kamen_nuzky_papir/assets/scissors.png', 'w') as f:
        f.write('')

    # Přidání README s přehledem projektů a principy repozitáře
    with open('README.md', 'w') as f:
        f.write('')

    # Aktualizace 01_Kamen_nuzky_papir_projekt.md
    with open('01_Kamen_nuzky_papir_projekt.md', 'w') as f:
        f.write('')

# Inicializace projektu
init_project()

# Načtení assetů
rock_image, paper_image, scissors_image = load_assets()

# Uložení assetů do souborů
rock_image.save('01_kamen_nuzky_papir/assets/rock.png')
paper_image.save('01_kamen_nuzky_papir/assets/paper.png')
scissors_image.save('01_kamen_nuzky_papir/assets/scissors.png')


Poznámka: Tento kód pouze generuje prázdné soubory a neposkytuje žádné funkční kód pro hru "Kámen, nůžky, papír". Pro implementaci samotné hry budete muset přidat další kód.