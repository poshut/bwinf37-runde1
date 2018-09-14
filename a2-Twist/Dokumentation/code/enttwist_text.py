import re

def enttwist_text(text: str, woerterbuch_text: str):
    woerterbuch = woerterbuch_erstellen(woerterbuch_text.split("\n"))
    enttwisteter_text = []
    # Der reguläre Ausdruck zum Finden von Wörtern im Text
    muster = re.compile(r'([a-zA-ZäöüÄÖÜß]+)')
    woerter_und_zeichen = re.split(muster, text)
    for element in woerter_und_zeichen:
        # Ist das Element ein Wort?
        if re.fullmatch(muster, element):
            schluessel = wort_zu_schluessel(element)
            moegliche_woerter = woerterbuch.get(schluessel)
            # Keine möglichen Wörter gefunden
            if moegliche_woerter is None:
                print("Kein enttwistetes Wort für", '"' + element + '"', "gefunden...")
                enttwisteter_text.append(element)
            # Ein mögliches Wort gefunden
            elif len(moegliche_woerter) == 1:
                if (element[0].isupper()):
                    moegliche_woerter[0] = moegliche_woerter[0][0].upper() + moegliche_woerter[0][1:]
                enttwisteter_text.append(moegliche_woerter[0])
            # Mehrere mögliche Woerter gefunden
            else:
                benutztes_wort = moegliche_woerter[0]
                print("Mehrere enttwistete Wörter für", '"' + element + '"', "gefunden: ", moegliche_woerter, ", benutze", '"' + benutztes_wort + '"', "...")
                enttwisteter_text.append(benutztes_wort)
        # Das Element ist kein Wort
        else:
            enttwisteter_text.append(element)
    print()
    return ''.join(enttwisteter_text)