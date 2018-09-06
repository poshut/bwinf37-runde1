from itertools import combinations
from graphviz import Graph
from uuid import uuid4

# widerstaende = list(map(float, [
#     1000, 5600, 180, 6800, 8200, 820, 2700, 150, 100, 1800, 220, 1500, 330, 390, 680, 120, 3900, 3300, 4700, 560, 470, 1200, 270, 2200]))

widerstaende = [100.0, 100.0, 100.0, 100.0]

"""
Ein zusammengebauter Widerstand wird als Tupel repräsentiert.
Das erste Feld ist der Typ: "einer", "reihe" oder "parallel"
Falls der Widerstandstyp "einer" ist, so ist das zweite Feld die Ohmzahl.
Falls der Widerstandstyp "reihe" ist, so sind das zweite und dritte Feld die in Reihe geschaltenen Widerstände.
Falls der Widerstandstyp "parallel" ist, so sind das zweite und dritte Feld die parallel geschaltenen Widerstände.
"""


def berechne(widerstand):
    """
    Den Widerstandswert eines Widerstandes zurueckgeben
    @param widerstand: Der Widerstand, fuer den der Widerstandswert berechnet werden soll
    """
    if widerstand[0] == "einer":
        return widerstand[1]
    elif widerstand[0] == "reihe":
        return berechne(widerstand[1]) + berechne(widerstand[2])
    elif widerstand[0] == "parallel":
        return 1 / (1 / berechne(widerstand[1]) + 1 / berechne(widerstand[2]))
    print("error")
    exit(1)



def widerstand_zusammenbauen(ohm, wie_viele, widerstaende):
    """
    Einen Widerstand mit einem speziellem Wert zusammenbauen
    @param ohm: Wie viel Ohm der Widerstand am besten haben sollte
    @param wie_viele: Aus wie vielen Elementarwiderstaenden der Widerstand bestehen soll
    @param widerstaende: Liste von zu verbauenden Elementarwiderstaenden
    """
    if wie_viele == 1:
        return ("einer", min(widerstaende, key=lambda x: abs(x-ohm)))

    moeglichkeiten = []

    # Falls noch vier Widerstaende uebrig sind, muessen wir zwei Extrafaelle betrachten
    if wie_viele == 4:
        combs = list(combinations(widerstaende, 2))
        for combination in combs:
            widerstaende.remove(combination[0])
            widerstaende.remove(combination[1])

            # Fall 1: Die Gruppen werden in Reihe geschalten
            uebrig = ohm - 1 / (1 / combination[0] + 1 / combination[1])
            moeglichkeiten.append(("reihe", ("parallel", ("einer", combination[0]), (
                "einer", combination[1])), widerstand_zusammenbauen(uebrig, 2, widerstaende)))

            # Fall 2: Die Gruppen werden parallel geschalten
            uebrig = 1 / (1 / ohm - (1 / combination[0] + 1 / combination[1]))
            moeglichkeiten.append(("parallel", ("parallel", ("einer", combination[0]), (
                "einer", combination[1])), widerstand_zusammenbauen(uebrig, 2, widerstaende)))

            widerstaende.append(combination[0])
            widerstaende.append(combination[1])

    # Fuer jeden Widerstand zweri Moeglichkeiten erstellen: In Reihe und parallel
    for i in widerstaende.copy():
        widerstaende.remove(i)

        # Man kann den neuen Widerstand und den Rest in Reihe schalten
        rest_reihe = ohm - i
        moeglichkeiten.append(("reihe", ("einer", i), widerstand_zusammenbauen(
            (rest_reihe), wie_viele-1, widerstaende)))

        # Mann kann den neuen Widerstand und den Rest parallel schalten

        # Wenn Ohm = i, oder Ohm = 0, dann kann es zu Fehlern fuehren. In diesem Fall betrachten wir den Rest als sehr gross
        if ohm != i and ohm != 0:
            rest_parallel = 1 / ((1 / ohm) - (1 / i))
        else:
            rest_parallel = 1e100
        moeglichkeiten.append(("parallel", ("einer", i), widerstand_zusammenbauen(
            (rest_parallel), wie_viele-1, widerstaende)))

        widerstaende.append(i)

    # Die Moeglichkeit mit der hoechsten Genauigkeit finden
    return min(moeglichkeiten, key=lambda x: abs(berechne(x)-ohm))


# Den Graphen mit der Bibliothek "graphviz" zeichnen
# Jeder Knoten bekommt eine zufällige ID.
# Alles wird zwischen einen Anfangs- und Endwiderstand gezeichnet.
# Die Funktion wird rekursiv aufgerufen.
def draw(widerstand, graph, knoten_davor, knoten_danach):
    if widerstand[0] == "einer":
        uid = str(uuid4())
        graph.node(uid, label="%.2f Ohm" % widerstand[1])
        graph.edge(knoten_davor, uid)
        graph.edge(uid, knoten_danach)
    elif widerstand[0] == "reihe":
        uid = str(uuid4())
        graph.node(uid, label='', height='0', shape='none')
        draw(widerstand[1], graph, knoten_davor, uid)
        draw(widerstand[2], graph, uid, knoten_danach)
    elif widerstand[0] == "parallel":
        draw(widerstand[1], graph, knoten_davor, knoten_danach)
        draw(widerstand[2], graph, knoten_davor, knoten_danach)


for i in range(1, 5):
    resultat = widerstand_zusammenbauen(25, i, widerstaende)
    print(resultat)
    print(berechne(resultat))
    dot = Graph(name="%s Widerstände - %.2f Ohm" %
                (i, berechne(resultat)), node_attr={'shape': 'box'}, format='png')

    dot.node('-', label='-')
    dot.node('+', label='+')
    print(resultat)
    draw(resultat, dot, '-', '+')
    dot.render()
