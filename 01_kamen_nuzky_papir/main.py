import os
import pygame
import git

# Nastavení projektu
projekt_nazev = "Kámen, nůžky, papír"
projekt_cel = "Implementace hry Kámen, nůžky, papír pomocí Pygame"

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
okno_velikost = (800, 600)

# Vytvoření okna
okno = pygame.display.set_mode(okno_velikost)

# Nastavení titulku okna
pygame.display.set_caption(projekt_nazev)

# Funkce pro načítání assetů
def načit_asset(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    asset_path = os.path.join(base_dir, 'assets', path)
    return pygame.image.load(asset_path)

# Funkce pro načítání dokumentace
def načit_dokumentace():
    with open('README.md', 'r') as soubor:
        dokumentace = soubor.read()
    return dokumentace

# Funkce pro načítání požadavků
def načit_pozadavky():
    with open('pozadavky.md', 'r') as soubor:
        pozadavky = soubor.read()
    return pozadavky

# Funkce pro načítání projektové dokumentace
def načit_projekt_dokumentace():
    with open('01_Kamen_nuzky_papir_projekt.md', 'r') as soubor:
        projekt_dokumentace = soubor.read()
    return projekt_dokumentace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():
    with open('pozadavky_ke_studentskym_pracim.md', 'r') as soubor:
        req_studentske_prace = soubor.read()
    return req_studentske_prace

# Funkce pro načítání požadavků ke studentským pracím
def načit_req_studentske_prace():