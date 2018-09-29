#!/bin/bash
import math

def laenge(r):
    return r[0]

def breite(r):
    return r[1]


def anordnen(sortiert, max_laenge):
    ergebnis = []
    current_row_height = breite(sortiert[0])
    current_x = 0
    current_y = 0

    for r in sortiert:
        if current_x + laenge(r) > max_laenge:
            if current_x == 0:
                return None, None, None, None
            current_x = 0
            current_y += current_row_height
            current_row_height = breite(r)

        ergebnis.append((current_x, current_y, r))
        current_x += laenge(r)

    return ergebnis, max_laenge, current_y + current_row_height, max_laenge * (current_y + current_row_height)


# Länge mal Breite
# rechtecke = [
#     (25, 15),
#     (30, 15),
#     (25, 20),
#     (25, 15),
# ]

rechtecke = [
    (50,25),
    (50,25),
    (25,25),
    (25,25),
]
sortiert = sorted(rechtecke, key=lambda x: breite(x), reverse=True)
min_laenge = min(rechtecke, key=lambda x: x[0])[0]
max_laenge = 0
for r in rechtecke:
    max_laenge += laenge(r)

min_flaeche = math.inf

for i in range(min_laenge, max_laenge + 1):
    resultat, laeng, hoeh, flaeche = anordnen(sortiert, i)
    if resultat is not None and min_flaeche > flaeche:
        min_resultat = resultat
        min_flaeche = flaeche
        min_laenge = laeng
        min_hoehe = hoeh

gesamtflaeche = 0
for r in rechtecke:
    gesamtflaeche += r[0] * r[1]

print("%d m x %d m => %d m^2, %d m^2 verschwendet" % (min_laenge, min_hoehe, min_flaeche, min_flaeche - gesamtflaeche))
for erg in min_resultat:
    print("Garten %d m x %d m im Punkt (%d, %d)" % (erg[2][0], erg[2][1], erg[0], erg[1]))