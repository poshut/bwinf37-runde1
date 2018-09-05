def superstar_bestimmen(mitglieder, verbindungen):
    # Ermittlungsphase
    moegliche_superstars: list = mitglieder.copy()

    # Wiederholen, bis es nurnoch einen moeglichen Superstar gibt
    while len(moegliche_superstars) > 1:

        mitglied1 = moegliche_superstars.pop()
        mitglied2 = moegliche_superstars.pop()

        # Eines der beiden Mitglieder ausschliessen
        if folgt(mitglied1, mitglied2, verbindungen):
            moegliche_superstars.append(mitglied2)
        else:
            moegliche_superstars.append(mitglied1)

    # Validierungsphase

    vermuteter_superstar = moegliche_superstars[0]

    # Fuer jedes Mitglied fragen, ob es dem vermuteten Superstar folgt oder andersherum
    for mitglied in mitglieder:
        if mitglied != vermuteter_superstar:
            if not folgt(mitglied, vermuteter_superstar, verbindungen):
                return None
            if folgt(vermuteter_superstar, mitglied, verbindungen):
                return None

    return vermuteter_superstar