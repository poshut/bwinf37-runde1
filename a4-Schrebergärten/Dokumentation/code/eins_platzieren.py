def eins_platzieren(breite, laenge, matrix):

    platziert = False
    
    # Einen Platz für das Rechteck finden
    for platziertes_x in range(len(matrix[0])):
        for platziertes_y in range(len(matrix)):
            if genuegend_platz(platziertes_x, platziertes_y, breite, laenge, matrix):
                platziert = True
                break
        if platziert:
            break

    if platziert:
        # Die Matrix wiederherstellen
        for x in range(platziertes_x, platziertes_x + breite):
            for y in range(platziertes_y, platziertes_y + laenge):
                matrix[y][x] = VOLL
    else:
        return None
        
    return (laenge, breite, platziertes_x, platziertes_y)