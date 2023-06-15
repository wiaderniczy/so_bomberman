# Bomberman - DynaBlaster

## Opis projektu

W ramach projektu należało stworzyć aplikację wykorzystującą wielowątkowość oraz sekcje krytyczne (w naszym przypadku semafory). Utworzona gra opiera się na klasycznej wersji dwuosobowego Bombermana. Zadaniem każdego z graczy jest wyeliminowanie przeciwnika poprzez eksplozję bomby.

## Grafika

![Grafika ilustrująca koncept działania programu](concept_graphic.png)

## Wątki

- player1_thread - reprezentuje pierwszego gracza
- player2_thread - reprezentuje drugiego gracza
- board_thread - reprezentuje plansze do gry

## Sekcje krytyczne

- semafor - służacy do synchronizacji dostępu do planszy