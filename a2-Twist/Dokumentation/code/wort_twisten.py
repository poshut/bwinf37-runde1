def wort_twisten(wort):
    if len(wort) <= 2:
        return wort
    mittlere_buchstaben = list(wort[1:-1])
    shuffle(mittlere_buchstaben)
    return wort[0] + ''.join(mittlere_buchstaben) + wort[-1]
