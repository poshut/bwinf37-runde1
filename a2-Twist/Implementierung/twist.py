#!/usr/bin/python3
import sys
import re
import argparse
from random import shuffle

def wort_twisten(wort):
    if len(wort) <= 2:
        return wort
    mittlere_buchstaben = list(wort[1:-1])
    shuffle(mittlere_buchstaben)
    return wort[0] + ''.join(mittlere_buchstaben) + wort[-1]

def text_twisten(text):
    # Der reguläre Ausdruck zum Finden von Wörtern im Text
    muster = re.compile(r'([a-zA-ZäöüÄÖÜß]+)')
    result = ""
    elemente = re.split(muster, text)
    for element in elemente:
        if re.fullmatch(muster, element):
            result += wort_twisten(element)
        else:
            result += element
    return result

def wort_zu_schluessel(wort):
    # Sortiere mittlere Buchstaben des Worts
    mittlere_buchstaben = ''.join(sorted(list(wort[1:-1])))
    return wort[0].lower() + mittlere_buchstaben + wort[-1].lower()

def woerterbuch_erstellen(woerter_liste):
    woerterbuch = {}
    for wort in woerter_liste:
        if wort != '':
            schluessel = wort_zu_schluessel(wort)
            if schluessel not in woerterbuch:
                woerterbuch[schluessel] = []
            woerterbuch[schluessel].append(wort)
    return woerterbuch


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
            # Mehrere mögliche Wörter gefunden
            else:
                benutztes_wort = moegliche_woerter[0]
                if (element[0].isupper()):
                    benutztes_wort = benutztes_wort[0].upper() + benutztes_wort[1:]
                
                # Warnung ausgeben, falls alle Wörter nicht gleich sind
                if len(set(moegliche_woerter)) != 1:
                    print("Mehrere enttwistete Wörter für", '"' + element + '"', "gefunden: ", moegliche_woerter, ", benutze", '"' + benutztes_wort + '"', "...")
                enttwisteter_text.append(benutztes_wort)
        # Das Element ist kein Wort
        else:
            enttwisteter_text.append(element)
    print()
    return ''.join(enttwisteter_text)

def twist_und_zurueck(text, woerterliste):
    return enttwist_text(text_twisten((text)), woerterliste)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Aufgabe 2: Twist")
    parser.add_argument('aktion', help='Aktion', choices=['twist', 'enttwist', 'beides'])
    parser.add_argument('eingabe', help='Eingabedatei')
    parser.add_argument('-w', '--woerter', help='Wörterliste')
    args = parser.parse_args()

    if args.aktion == 'twist':
        with open(args.eingabe) as f:
            print(text_twisten(f.read()))
    elif args.aktion == 'enttwist':
        if args.woerter is None:
            print("Fehler: Keine Wörterliste angegeben!")
            exit(1)

        with open(args.eingabe) as eingabe:
            with open(args.woerter) as woerter:
                print(enttwist_text(eingabe.read(), woerter.read()))
    elif args.aktion == 'beides':
        if args.woerter is None:
            print("Fehler: Keine Wörterliste angegeben!")
            exit(1)

        with open(args.eingabe) as eingabe:
            with open(args.woerter) as woerter:
                print(twist_und_zurueck(eingabe.read(), woerter.read()))

