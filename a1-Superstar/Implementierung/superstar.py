#!/usr/bin/python3
import sys

def eingabe_lesen(dateiname):
    with open(dateiname) as f:
        mitglieder = f.readline().strip().split(' ')
        verbindungen = []
        for line in f.readlines():
            if line.strip() != "":
                verbindung = line.strip().split(' ')
                verbindungen.append(verbindung)
    return mitglieder, verbindungen

verbindungen_zwischenspeicher = {}
euro = 0

# Folgt X Y?
def folgt(x, y, verbindungen):

    # Aufruf aus Zwischenspeicher beantworten, falls möglich
    if verbindungen_zwischenspeicher.get((x,y)) is not None:
        return verbindungen_zwischenspeicher.get((x,y))

    # Anfrage stellen
    ergebnis = [x,y] in verbindungen

    # Anfrage und Ergebnis zwischenspeichern
    verbindungen_zwischenspeicher[(x,y)] = ergebnis

    # Anzahl der Anfragen erhöhen
    global euro
    euro += 1

    # Anfrage und Ergebnis ausgeben
    if ergebnis:
        print("Folgt", x, y + "? \tJa!")
    else:
        print("Folgt", x, y + "? \tNein!")

    return ergebnis


def superstar_bestimmen(mitglieder, verbindungen):
    # Ermittlungsphase
    moegliche_superstars: list = mitglieder.copy()

    # Wiederholen, bis es nurnoch einen möglichen Superstar gibt
    while len(moegliche_superstars) > 1:

        mitglied1 = moegliche_superstars.pop()
        mitglied2 = moegliche_superstars.pop()

        # Eines der beiden Mitglieder ausschließen
        if folgt(mitglied1, mitglied2, verbindungen):
            moegliche_superstars.append(mitglied2)
        else:
            moegliche_superstars.append(mitglied1)

    # Validierungsphase

    vermuteter_superstar = moegliche_superstars[0]

    # Für jedes Mitglied fragen, ob es dem vermuteten Superstar folgt oder andersherum
    for mitglied in mitglieder:
        if mitglied != vermuteter_superstar:
            if not folgt(mitglied, vermuteter_superstar, verbindungen):
                return None
            if folgt(vermuteter_superstar, mitglied, verbindungen):
                return None

    return vermuteter_superstar

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Benutzung:", sys.argv[0], "<Eingabedatei>")
        exit(1)
    mitglieder, verbindungen = eingabe_lesen(sys.argv[1])
    superstar = superstar_bestimmen(mitglieder, verbindungen)
    if superstar is not None:
        print("Superstar:", superstar)
    else:
        print("Kein Superstar")
    print(len(mitglieder), "Mitglieder")
    print(euro, "gestellte Anfragen")