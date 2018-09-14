def wort_zu_schluessel(wort):
    # Sortiere mittlere Buchstaben des Worts
    mittlere_buchstaben = ''.join(sorted(list(wort[1:-1])))
    return wort[0].lower() + mittlere_buchstaben + wort[-1].lower()