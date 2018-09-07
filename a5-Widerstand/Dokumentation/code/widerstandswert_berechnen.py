def widerstandswert_berechnen(widerstand):
    """
    Den Widerstandswert eines Widerstandes zurueckgeben
    @param widerstand: Der Widerstand, fuer den der Widerstandswert berechnet werden soll
    """
    if widerstand[0] == "einer":
        return widerstand[1]
    elif widerstand[0] == "reihe":
        return widerstandswert_berechnen(widerstand[1]) +
            widerstandswert_berechnen(widerstand[2])
    elif widerstand[0] == "parallel":
        return 1 / (1 / widerstandswert_berechnen(widerstand[1]) + 
            1 / widerstandswert_berechnen(widerstand[2]))
    print("error")
    exit(1)