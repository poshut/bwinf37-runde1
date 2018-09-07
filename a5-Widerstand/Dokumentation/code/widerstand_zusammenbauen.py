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