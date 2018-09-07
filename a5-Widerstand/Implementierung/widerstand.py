import sys
from itertools import combinations
from uuid import uuid4


def widerstandswert_berechnen(widerstand):
    """
    Den Widerstandswert eines Widerstandes zurueckgeben
    @param widerstand: Der Widerstand, fuer den der Widerstandswert berechnet werden soll
    """
    if widerstand[0] == "einer":
        return widerstand[1]
    elif widerstand[0] == "reihe":
        return widerstandswert_berechnen(widerstand[1]) + widerstandswert_berechnen(widerstand[2])
    elif widerstand[0] == "parallel":
        return 1 / (1 / widerstandswert_berechnen(widerstand[1]) + 1 / widerstandswert_berechnen(widerstand[2]))
    print("error")
    exit(1)


def widerstand_zusammenbauen(ohm, wie_viele, widerstaende):
    """
    Einen Widerstand mit einem speziellem Wert zusammenbauen
    @param ohm: Wie viel Ohm der Widerstand am besten haben sollte
    @param wie_viele: Aus wie vielen Elementarwiderstaenden der Widerstand bestehen soll
    @param widerstaende: Liste von zu verbauenden Elementarwiderstaenden
    """
    assert 1 <= wie_viele <= 4

    if wie_viele == 1:
        return ("einer", min(widerstaende, key=lambda x: abs(x-ohm)))

    moeglichkeiten = []

    # Falls noch vier Widerstaende uebrig sind, muessen wir zwei Extrafaelle betrachten
    if wie_viele == 4:
        combs = list(combinations(widerstaende, 2))
        for combination in combs:
            widerstaende.remove(combination[0])
            widerstaende.remove(combination[1])

            # Fall 1: Die Gruppen werden in Reihe geschalten, R1 ist aber parallel geschalten
            uebrig = ohm - 1 / (1 / combination[0] + 1 / combination[1])
            moeglichkeiten.append(("reihe", ("parallel", ("einer", combination[0]), (
                "einer", combination[1])), widerstand_zusammenbauen(uebrig, 2, widerstaende)))

            # Fall 2: Die Gruppen werden parallel geschalten, R1 ist aber in Reihe geschalten
            try:
                uebrig = 1 / (1 / ohm - 1 / (combination[0] + combination[1]))
            except ZeroDivisionError:
                # Wenn in der ersten Klammer 0 rauskommt, tritt ein Fehler auf.
                # In diesem Fall ist die Ohmzahl durch die beiden Widerstände gedeckt und die anderen
                # Widerstände sollten so hoch wie möglich sein
                uebrig = 1e100

            moeglichkeiten.append(("parallel", ("reihe", ("einer", combination[0]), (
                "einer", combination[1])), widerstand_zusammenbauen(uebrig, 2, widerstaende)))
            

            widerstaende.append(combination[0])
            widerstaende.append(combination[1])

    # Fuer jeden Widerstand zweri Moeglichkeiten erstellen: In Reihe und parallel
    for r1 in set(widerstaende):
        widerstaende.remove(r1)

        # Man kann den neuen Widerstand und den Rest in Reihe schalten
        rest_reihe = ohm - r1
        moeglichkeiten.append(("reihe", ("einer", r1), widerstand_zusammenbauen(
            (rest_reihe), wie_viele-1, widerstaende)))

        # Mann kann den neuen Widerstand und den Rest parallel schalten
        try:
            rest_parallel = 1 / ((1 / ohm) - (1 / r1))
        except ZeroDivisionError:
            # Wenn in der ersten Klammer 0 rauskommt, tritt ein Fehler auf.
            # In diesem Fall ist die Ohmzahl durch r1 gedeckt und die anderen
            # Widerstände sollten so hoch wie möglich sein
            rest_parallel = 1e100

        moeglichkeiten.append(("parallel", ("einer", r1), widerstand_zusammenbauen(
            (rest_parallel), wie_viele-1, widerstaende)))

        widerstaende.append(r1)

    # Die Moeglichkeit mit der hoechsten Genauigkeit finden
    return min(moeglichkeiten, key=lambda x: abs(widerstandswert_berechnen(x)-ohm))


def widerstand_zeichnen(widerstand, graph, knoten_davor, knoten_danach):
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
        widerstand_zeichnen(widerstand[1], graph, knoten_davor, uid)
        widerstand_zeichnen(widerstand[2], graph, uid, knoten_danach)
    elif widerstand[0] == "parallel":
        widerstand_zeichnen(widerstand[1], graph, knoten_davor, knoten_danach)
        widerstand_zeichnen(widerstand[2], graph, knoten_davor, knoten_danach)

def eingabe_lesen(dateiname):
    widerstaende = []
    with open(sys.argv[1]) as f:
        for i in f.read().split('\n'):
            if i != '':
                assert i != "0"
                widerstaende.append(int(i))
    return widerstaende


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Benutzung:", sys.argv[0],
              "<Widerstandsliste> <Widerstandswert>")
        exit(1)

    widerstaende = eingabe_lesen(sys.argv[1])
    widerstandswert = int(sys.argv[2])

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
        print(anzahl, "Widerstände:", widerstandswert_berechnen(resultat), "Ohm")
        print(resultat)

        if graphviz is not None:
            name = "%s Widerstände - %.2f Ohm" % (anzahl, widerstandswert_berechnen(resultat))
            graph = graphviz.Graph(name=name, node_attr={
                                   'shape': 'box'}, format='png')

            graph.node('-', label='-')
            graph.node('+', label='+')
            widerstand_zeichnen(resultat, graph, '-', '+')
            graph.render()
            print("Zeichnung nach \"%s.gv.png\" ausgegeben" % name)

        print()
