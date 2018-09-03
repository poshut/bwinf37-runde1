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

def ist_superstar(mitglied, mitglieder, verbindungen):
    pass


verbindungen_cache = {}
euro = 0

def folgt(x, y, verbindungen):
    """
    Folgt x y?
    """
    if verbindungen_cache.get((x,y)) is not None:
        return verbindungen_cache.get((x,y))
    ergebnis = [x,y] in verbindungen
    verbindungen_cache[(x,y)] = ergebnis

    global euro
    euro += 1

    print("Folgt", x, y + "?", ergebnis)

    return ergebnis


def superstar_bestimmen(mitglieder, verbindungen):
    mögliche_superstars: list = mitglieder.copy()

    while len(mögliche_superstars) > 1:
        mögliche_superstars_neu = []
        for _ in range(len(mögliche_superstars) // 2):
            mitglied1 = mögliche_superstars.pop()
            mitglied2 = mögliche_superstars.pop()
            if folgt(mitglied1, mitglied2, verbindungen):
                mögliche_superstars_neu.append(mitglied2)
            else:
                mögliche_superstars_neu.append(mitglied1)
        mögliche_superstars += mögliche_superstars_neu

    vermuteter_superstar = mögliche_superstars[0]
    for mitglied in mitglieder:
        if mitglied != vermuteter_superstar:
            if not folgt(mitglied, vermuteter_superstar, verbindungen):
                return False
            if folgt(vermuteter_superstar, mitglied, verbindungen):
                return False

    return vermuteter_superstar

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Benutzung:", sys.argv[0], "<Eingabedatei>")
        exit(1)
    mitglieder, verbindungen = eingabe_lesen(sys.argv[1])
    superstar = superstar_bestimmen(mitglieder, verbindungen)
    if superstar != False:
        print("Superstar:", superstar)
    else:
        print("Kein Superstar")
    print(len(mitglieder), "Mitglieder")
    print(euro, "gestellte Anfragen")