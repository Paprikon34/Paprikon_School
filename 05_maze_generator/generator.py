import random
import sys

# Zvětšíme limit rekurze (pro jistotu, kdyby se vygenerovalo obří bludiště)
sys.setrecursionlimit(5000)

# Velikost bludiště (musí to být lichá čísla, např. 31 a 15)
SIRKA = 31
VYSKA = 15

# Definujeme si, jak budou vypadat zdi a cesty (použijeme 2 znaky pro každé, ať vznikne hezký čtverec)
ZED = "██"
CESTA = "  "

def vytvor_prazdne_bludiste():
    """ 
    Vytvoří mapu, která je úplně celá zasypaná hlínou (všude jsou zdi).
    Vrací 2D pole zdí.
    """
    mapa = []
    for y in range(VYSKA):
        radek = []
        for x in range(SIRKA):
            radek.append(ZED)
        mapa.append(radek)
    return mapa

def vykopat_tunel(x, y, mapa):
    """
    Toto je hlavní FUNKCE (krtek). Vykope díru, náhodně se rozhlédne a jde dál.
    """
    # Označíme současné místo jako vykopanou cestu (prázdno)
    mapa[y][x] = CESTA
    
    # 4 směry, kam může krtek kopat (Nahoru, Dolů, Doleva, Doprava)
    # Skáčeme vždy o 2 políčka! To aby nám mezi cestami zůstala vždy jedna tenká zeď.
    # Uspořádání je: (kolik_skok_na_X, kolik_skok_na_Y)
    smery = [
        (0, -2), # Nahoru (y se zmenší o 2)
        (0, 2),  # Dolů (y se zvětší o 2)
        (-2, 0), # Doleva (x se zmenší o 2)
        (2, 0)   # Doprava (x se zvětší o 2)
    ]
    
    # Zamícháme směry! Proto je každé bludiště jiné - krtek má pokaždé jiný plán.
    random.shuffle(smery)
    
    # Krtek to zkouší postupně do všech 4 směrů v náhodném pořadí
    for skok_x, skok_y in smery:
        dalsi_x = x + skok_x
        dalsi_y = y + skok_y
        
        # Zkontrolujeme dvě důležité věci:
        # 1. Nevyjeli jsme z mapy pryč?
        # 2. Je na tom novém místě ještě hlína (zeď)? (Pokud je tam už cesta, nekopeme tam)
        if 0 < dalsi_x < SIRKA - 1 and 0 < dalsi_y < VYSKA - 1:
            if mapa[dalsi_y][dalsi_x] == ZED:
                # Našli jsme místo! 
                # Prokopneme i tu zeď, kterou jsme "přeskočili", čímž se obě místa spojí
                mapa[y + skok_y // 2][x + skok_x // 2] = CESTA
                
                # REKURZE: (Nejsložitější krok - obtížnost 5)
                # Voláme znovu stejnou funkci, aby pokračovala z NOVÉHO místa. 
                # Když krtek v nové chodbě skončí a nemá kam jít (slepá ulička), 
                # program se o krok vrátí z rekurze zpět sem a krtek zkusí další směr.
                vykopat_tunel(dalsi_x, dalsi_y, mapa)

# --- HLAVNÍ ČÁST PROGRAMU ---
if __name__ == "__main__":
    print("Spouštím program pro generování bludiště (Algoritmus: Rekurzivní Krtek)...\n")

    # 1. Připravíme hlínu (zdi)
    nase_bludiste = vytvor_prazdne_bludiste()

    # 2. Vypustíme krtka z levého horního rohu (souřadnice 1, 1 uvnitř hlíny)
    vykopat_tunel(1, 1, nase_bludiste)

    # 3. Z krtkovy nory vyrobíme Vstup a Výstup na krajích mapy, aby to bylo hratelné bludiště
    nase_bludiste[1][0] = CESTA # Vstup je nalevo
    nase_bludiste[VYSKA-2][SIRKA-1] = CESTA # Výstup je napravo dole

    # 4. Vytiskneme hezky na obrazovku řádek po řádku
    for radek in nase_bludiste:
        # Převedeme pole značek do jednoho stringu pro celý řádek
        print("".join(radek))

    print("\nÚspěšně vygenerováno! Zvládneš ho v hlavě vyřešit?")
