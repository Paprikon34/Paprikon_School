# Obhajoba Projektu 05: Generátor Bludiště (Dětská Edice)

Tento projekt reprezentuje algoritmus s **Náročností 5** (Generátor bludišť podle hodnotících pravidel), který je nicméně napsaný tak jednoduše a s takovým komentářem, aby mu dokázal porozumět žák sedmé třídy. Získáte tak plný počet bodů za složitost, ovšem předejdete zbytečně "špatnému/hutnému" kódu.

## O co se jedná
Jde o Python skript běžící v terminálu. Skript generuje perfektní, plně propojená bludiště bez odříznutých cest. Za každým spuštěním vznikne absolutně jiné bludiště.

## Proč spadá do kategorie "Velmi těžká (Level 5)"?
Pro vygenerování dokonalého bludiště počítač potřebuje pochopit takzvaný algoritmus **Rekurze s Backtrackingem** (navracením v mrtvém bodě). Tento princip je na pochopení pro začátečníky matoucí.

## Vysvětlující příběh o Krtkovi (pro děti)
Aby to 7. třída pochopila, je princip rekurze vysvětlen v kódu na chování krtka:
1. Krtek je uprostřed hlíny (pole zídeček) a vykope noru.
2. Náhodně se rozhlédne na 4 strany (nahoru, dolů... atd). 
3. Vybere si 1. stranu a pokud je tam neprokopáno, poskočí tam a prorazí cestu.
4. Nyní je krtek na novém políčku a jede "od začátku" = To je ta takzvaná **REKURZE** (funkce volá sama na sobě stejné chování znovu).
5. Krtek se takhle provrtává mapou. Jakmile se na aktuálním polygonu dostane do slepé uličky - tedy rozhlédne se na všechny 4 strany a všude už je vykopáno chodba (anebo okraj mapy) - řekne si "Aha, tudy cesta nevede".
6. Zastaví svoji rekurzi, vrátí se chodbou o pouhé **jeden krok zpátky** (To je ten **BACKTRACKING** neboli vracení) a vyzkouší z toho staršího místa vykopat zbylými třemi nepoužitými směry novou větev bludiště. Tím prokope veškeré možné cesty.

## Spuštění kódu
Otevřete terminál a namiřte se do složky projektu. Zadejte příkaz:
```bash
python generator.py
```
Okamžitě se vám vygeneruje náhodné 2D ascii bludiště.
