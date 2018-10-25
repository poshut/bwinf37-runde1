if __name__ == "__main__":
    # Länge mal Breite
    rechtecke = [
        # Rechtecke hier einfügen, z.B.
        #(100, 100),
        #(100, 100),
        #(100, 100),
        #(100, 100),
     ]

    # Keine Rechtecke vorhanden
    if len(rechtecke) == 0:
        print("0 m x 0 m => 0 m^2, 0 m^2 verschwendet")
        exit()

    gesamtflaeche = 0
    for r in rechtecke:
        gesamtflaeche += r_laenge(r) * r_breite(r)
    
    faktor = r_laenge(rechtecke[0])
    for r in rechtecke:
        faktor = gcd(faktor, r_laenge(r))
        faktor = gcd(faktor, r_breite(r))
    

    rechtecke = list(map(lambda r: (r[0] // faktor, r[1] // faktor), rechtecke))
    sortierte_rechtecke = sorted(rechtecke, key=lambda x: r_laenge(x), reverse=True)

    # Breite aller Rechtecke zusammen
    gesamtbreite = 0
    for r in rechtecke:
        gesamtbreite += r_breite(r)
    # Breite, die das breiteste Rechteck hat
    maximalbreite = r_breite(max(rechtecke, key=lambda r: r_breite(r)))


    maximallaenge = r_laenge(sortierte_rechtecke[0])



    bestes_ergebnis = []

    momentane_laenge = maximallaenge
    momentane_breite = gesamtbreite

    while momentane_breite >= maximalbreite:
        ergebnis = anordnen(sortierte_rechtecke, momentane_breite, momentane_laenge)
        if ergebnis is not None:
            # Alle Anordnungen, die die gleicht Breite haben werden, überspringen
            momentane_breite = ergebnis[2] - 1

            # Ergebnis speichern
            if len(bestes_ergebnis) == 0 or bestes_ergebnis[1] * bestes_ergebnis[2] > 
                        ergebnis[1] * ergebnis[2]:
                bestes_ergebnis = ergebnis
        else:
            momentane_laenge += 1


    # Alles wieder um Faktor vergrößern
    bestes_ergebnis = (
        list(map(lambda r: tuple(map(lambda g: g*faktor, r)), bestes_ergebnis[0])),
        faktor * bestes_ergebnis[1],
        faktor * bestes_ergebnis[2]
    )


    loesungsflaeche = bestes_ergebnis[1] * bestes_ergebnis[2]

    print("%d m x %d m => %d m^2, %d m^2 verschwendet" % 
                (bestes_ergebnis[2], bestes_ergebnis[1], loesungsflaeche, 
                (loesungsflaeche - gesamtflaeche)))
    for r in bestes_ergebnis[0]:
        print("Garten %d m x %d m im Punkt (%d, %d)" % 
                (r_laenge(r), r_breite(r), r_x(r), r_y(r)))