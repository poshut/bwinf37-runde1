def genuegend_platz(x, y, breite, laenge, matrix):
    """
    Schaut, ob an der Position (x;y) noch genuegend Platz fuer ein Rechteck der Groesse (breite;laenge) ist
    """

    # Ist das Umgebungsrechteck gross genug?
    if x + breite > len(matrix[0]) or y + laenge > len(matrix):
        return False 

    current_x = x
    while current_x < x + breite:
        if matrix[y][current_x] != LEER or matrix[y + laenge - 1][current_x] != LEER:
            return False
        current_x += 1

    current_y = y
    while current_y < y + laenge:
        if matrix[current_y][x] != LEER or matrix[current_y][x + breite - 1] != LEER:
            return False
        current_y += 1
    
    return True