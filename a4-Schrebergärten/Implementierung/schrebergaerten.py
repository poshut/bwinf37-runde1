#!/bin/bash
import math

def r_x(r):
    return r[2]

def r_y(r):
    return r[3]

def r_laenge(r):
    return r[0]

def r_breite(r):
    return r[1]

LEER = 0
VOLL = 1

def genuegend_platz(x, y, breite, laenge, matrix):
    """
    Schaut, ob an der Position (x;y) noch genuegend Platz fuer ein Rechteck der Groesse (breite;laenge) ist
    """

    # Ist das Umgebungsrechteck gross genug?
    if x + breite > len(matrix[0]) or y + laenge > len(matrix):
        return False 

    current_x = x
    while current_x < x + breite:
        if matrix[y][current_x] != LEER or matrix[y + laenge - 1][current_x] != LEER:
            return False
        current_x += 1

    current_y = y
    while current_y < y + laenge:
        if matrix[current_y][x] != LEER or matrix[current_y][x + breite - 1] != LEER:
            return False
        current_y += 1
    
    return True

def eins_platzieren(breite, laenge, matrix):

    platziert = False

    # Einen Platz für das Rechteck finden
    for platziertes_x in range(len(matrix[0])):
        for platziertes_y in range(len(matrix)):
            if genuegend_platz(platziertes_x, platziertes_y, breite, laenge, matrix):
                platziert = True
                break
        if platziert:
            break

    if platziert:
        # Die Matrix wiederherstellen
        for x in range(platziertes_x, platziertes_x + breite):
            for y in range(platziertes_y, platziertes_y + laenge):
                matrix[y][x] = VOLL
    else:
        return None
        
    return (laenge, breite, platziertes_x, platziertes_y)

def anordnen(rechtecke, breite, laenge):
    matrix = [ [LEER for _ in range(breite)] for _ in range(laenge) ]
    loesung = []
    for r in rechtecke:
        platziert = eins_platzieren(r_breite(r), r_laenge(r), matrix)
        if platziert is not None:
            loesung.append(platziert)
        else:
            return None

    rechteck_ganz_weit_rechts = max(loesung, key=lambda r: r_x(r) + r_breite(r))
    maximal_benoetigte_breite = r_x(rechteck_ganz_weit_rechts) + r_breite(rechteck_ganz_weit_rechts)
    
    return (loesung, laenge, maximal_benoetigte_breite)

# Länge mal Breite
# rechtecke = [
#     (25, 15),
#     (30, 15),
#     (25, 20),
#     (25, 15),
# ]

rechtecke = [
    (25,25),
    (25,25),
    (25,25),
    (25,25),
]

sortierte_rechtecke = sorted(rechtecke, key=lambda x: r_laenge(x), reverse=True)

# Breite aller Rechtecke zusammen
breite_gesamt = 0
for r in rechtecke:
    breite_gesamt += r_breite(r)

# Breite, die das breiteste Rechteck hat
hoechste_breite = r_breite(max(rechtecke, key=lambda r: r_breite(r)))


bestes_ergebnis = []

momentane_laenge = r_laenge(sortierte_rechtecke[0])
momentane_breite = breite_gesamt

while momentane_breite >= hoechste_breite:
    ergebnis = anordnen(sortierte_rechtecke, momentane_breite, momentane_laenge)
    if ergebnis is not None:
        #print("Garten %d m x %d m --> %s" % (momentane_laenge, momentane_breite, ergebnis))

        # Alle Anordnungen, die die gleicht Breite haben werden, überspringen
        momentane_breite = ergebnis[2] - 1

        # Ergebnis speichern
        if len(bestes_ergebnis) == 0 or bestes_ergebnis[1] * bestes_ergebnis[2] > ergebnis[1] * ergebnis[2]:
            bestes_ergebnis = ergebnis
    else:
        #print("Garten %d m x %d m --> Kein Ergebnis" % (momentane_laenge, momentane_breite))
        momentane_laenge += 1


min_flaeche = 0
for r in rechtecke:
    min_flaeche += r_laenge(r) * r_breite(r)

beste_flaeche = bestes_ergebnis[1] * bestes_ergebnis[2]

print("%d m x %d m => %d m^2, %d m^2 verschwendet" % (bestes_ergebnis[2], bestes_ergebnis[1], beste_flaeche, beste_flaeche - min_flaeche))
for r in bestes_ergebnis[0]:
    print("Garten %d m x %d m im Punkt (%d, %d)" % (r_laenge(r), r_breite(r), r_x(r), r_y(r)))