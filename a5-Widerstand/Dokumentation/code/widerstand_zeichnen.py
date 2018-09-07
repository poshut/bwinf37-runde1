try:
    graphviz = __import__("graphviz")
except ImportError as e:
    print(e)
    print("Fehler beim Versuch, Graphviz zu importieren.
        Es werden keine Zeichnungen ausgegeben.")
    graphviz = None

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


if graphviz is not None:
    name = "%s %s - %.2f Ohm" % (anzahl, w, widerstandswert_berechnen(resultat))
    graph = graphviz.Graph(name=name, node_attr={
                            'shape': 'box'}, format='png')

    graph.node('-', label='-')
    graph.node('+', label='+')
    widerstand_zeichnen(resultat, graph, '-', '+')
    graph.render()
    print("Zeichnung nach \"%s.gv.png\" ausgegeben" % name)