#!/usr/bin/python3
import math

def r_x(r):
    return r[2]

def r_y(r):
    return r[3]

def r_laenge(r):
    return r[0]

def r_breite(r):
    return r[1]

def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a

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


if __name__ == "__main__":
    # Länge mal Breite
    rechtecke = [
        (700, 299),
        (500, 900),
        (350, 200),
        (600, 800),
        (50, 100),
        (500, 600)
    ]

    # Keine Rechtecke vorhanden
    if len(rechtecke) == 0:
        print("0 m x 0 m => 0 m^2, 0 m^2 verschwendet")
        exit()

    gesamtflaeche = 0
    for r in rechtecke:
        gesamtflaeche += r_laenge(r) * r_breite(r)
    
    faktor = r_laenge(rechtecke[0])
    for r in rechtecke:
        faktor = gcd(faktor, r_laenge(r))
        faktor = gcd(faktor, r_breite(r))
    
    # Alle Rechtecke entsprechend des Faktors verkleinern
    if faktor != 1:
        rechtecke = list(map(lambda r: (r[0] // faktor, r[1] // faktor), rechtecke))
    sortierte_rechtecke = sorted(rechtecke, key=lambda x: r_laenge(x), reverse=True)

    # Breite aller Rechtecke zusammen
    gesamtbreite = 0
    for r in rechtecke:
        gesamtbreite += r_breite(r)

    # Breite, die das breiteste Rechteck hat
    maximalbreite = r_breite(max(rechtecke, key=lambda r: r_breite(r)))


    maximallaenge = r_laenge(sortierte_rechtecke[0])


    bestes_ergebnis = []

    momentane_laenge = maximallaenge
    momentane_breite = gesamtbreite

    while momentane_breite >= maximalbreite:
        ergebnis = anordnen(sortierte_rechtecke, momentane_breite, momentane_laenge)
        if ergebnis is not None:
            # Alle Anordnungen, die die gleicht Breite haben werden, überspringen
            momentane_breite = ergebnis[2] - 1

            # Ergebnis speichern
            if len(bestes_ergebnis) == 0 or bestes_ergebnis[1] * bestes_ergebnis[2] > ergebnis[1] * ergebnis[2]:
                bestes_ergebnis = ergebnis
        else:
            momentane_laenge += 1


    # Alles wieder um Faktor vergrößern
    bestes_ergebnis = (
        list(map(lambda r: tuple(map(lambda g: g*faktor, r)), bestes_ergebnis[0])),
        faktor * bestes_ergebnis[1],
        faktor * bestes_ergebnis[2]
    )


    loesungsflaeche = bestes_ergebnis[1] * bestes_ergebnis[2]

    print("%d m x %d m => %d m^2, %d m^2 verschwendet" % (bestes_ergebnis[2], bestes_ergebnis[1], loesungsflaeche, (loesungsflaeche - gesamtflaeche)))
    for r in bestes_ergebnis[0]:
        print("Garten %d m x %d m im Punkt (%d, %d)" % (r_laenge(r), r_breite(r), r_x(r), r_y(r)))