import sys
from itertools import combinations
from uuid import uuid4

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


def draw(widerstand, graph, knoten_davor, knoten_danach):
    """
    Den Graphen mit der Bibliothek "graphviz" zeichnen
    Jeder Knoten bekommt eine zufällige ID.
    Alles wird zwischen einen Anfangs- und Endwiderstand gezeichnet.
    Die Funktion wird rekursiv aufgerufen.
    """
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


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Benutzung:", sys.argv[0],
              "<Widerstandsliste> <Widerstandswert>")
        exit(1)

    widerstandswert = int(sys.argv[2])
    with open(sys.argv[1]) as f:
        widerstaende = list(map(lambda x: float(int(x[:-1])), f.readlines()))

    # Versuche, graphviz zu importieren
    try:
        graphviz = __import__("graphviz")
    except ImportError as e:
        print(e)
        print("Fehler beim Versuch, Graphviz zu importieren. Es werden keine Zeichnungen ausgegeben.")
        graphviz = None

    for anzahl in range(1, 5):
        resultat = widerstand_zusammenbauen(
            widerstandswert, anzahl, widerstaende)
        print(anzahl, "Widerstände:", berechne(resultat), "Ohm")
        print(resultat)

        if graphviz is not None:
            name = "%s Widerstände - %.2f Ohm" % (anzahl, berechne(resultat))
            graph = graphviz.Graph(name=name, node_attr={
                                   'shape': 'box'}, format='png')

            graph.node('-', label='-')
            graph.node('+', label='+')
            draw(resultat, graph, '-', '+')
            graph.render()
            print("Zeichnung nach \"%s.gv.png\" ausgegeben" % name)

        print()
