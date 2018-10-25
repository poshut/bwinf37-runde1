def anordnen(rechtecke, breite, laenge):
    matrix = [ [LEER for _ in range(breite)] for _ in range(laenge) ]
    loesung = []
    for r in rechtecke:
        platziert = eins_platzieren(r_breite(r), r_laenge(r), matrix)
        if platziert is not None:
            loesung.append(platziert)
        else:
            return None

    rechteck_ganz_weit_rechts = max(loesung, key=lambda r: r_x(r) + r_breite(r))
    maximal_benoetigte_breite = r_x(rechteck_ganz_weit_rechts) + r_breite(rechteck_ganz_weit_rechts)
    
    return (loesung, laenge, maximal_benoetigte_breite)