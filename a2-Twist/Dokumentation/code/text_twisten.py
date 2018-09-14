import re

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