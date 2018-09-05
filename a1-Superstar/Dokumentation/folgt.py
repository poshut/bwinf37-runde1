verbindungen_zwischenspeicher = {}
euro = 0

# Folgt X Y?
def folgt(x, y, verbindungen):

    # Aufruf aus Zwischenspeicher beantworten, falls moeglich
    if verbindungen_zwischenspeicher.get((x,y)) is not None:
        return verbindungen_zwischenspeicher.get((x,y))

    # Anfrage stellen
    ergebnis = [x,y] in verbindungen

    # Anfrage und Ergebnis zwischenspeichern
    verbindungen_zwischenspeicher[(x,y)] = ergebnis

    # Anzahl der Anfragen erhoehen
    global euro
    euro += 1

    # Anfrage und Ergebnis ausgeben
    if ergebnis:
        print("Folgt", x, y + "? \tJa!")
    else:
        print("Folgt", x, y + "? \tNein!")

    return ergebnis