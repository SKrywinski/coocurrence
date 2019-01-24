import pywikibot as pw
from pywikibot import pagegenerators
import wikipediaapi as wi
import time

import csv
import re

wp = wi.Wikipedia("de")

# commented for developing-purposes
categories = ["Kategorie:Biologischer Prozess",
              # "Kategorie:Fantasy-Fernsehserie",
              # "Kategorie:Romantik (Literatur)",
              # "Kategorie:Informationssendung (Fernsehen)",
              # "Kategorie:See in Bayern",
              # "Kategorie:Viertausender",
              # "Kategorie:Kreditgeschäft",
              # "Kategorie:Planung und Organisation",
              # "Kategorie:Xbox-Spiel",
              # "Kategorie:Internet"
              ]


site = pw.Site()

# regex to be found (only calculated once)
# TODO: "^"-literal
pat = re.compile("^Literatur$|^Einzelnachweis$|^Weblinks$|^Siehe auch$|^Weiterführende Literatur$", re.MULTILINE)
# pat = re.compile("^Literatur$")

def processed(text, pat=pat):
    bevor = len(text)
    match = pat.search(text)
    if match != None:
        ind = match.start()
        text = text[:ind]
        print("{} gefunden".format(ind))
    diff = bevor - len(text)
    print(diff, len(text))
    return text

articles_list = []
headers = ["Kategorie", "Titel", "Zusammenfassung", "Text"]

fb = open(r'backup3.csv', 'w')
wb = csv.DictWriter(fb, headers)
wb.writeheader()

for category in categories:
    article_line = {}
    cat = pw.Category(site, category)
    for article in cat.articles():
        start = time.time()
        page_wi = wp.page(article.title())
        summary = page_wi.summary
        # text = page_wi.text.replace(page_wi.summary, "")
        text = page_wi.text
        text = processed(text)
        article_line = {
            "Kategorie": cat.title(),
            "Titel": page_wi.title,
            "Zusammenfassung": summary,
            "Text": text}
        articles_list.append(article_line)
        # print("{} seconds per article".format(time.time() - start))
        wb.writerow(article_line)

fb.close()

with open(r'total3.csv', 'w') as f:
    w = csv.DictWriter(f, headers)
    w.writeheader()
    w.writerows(articles_list)


# TODO: in DF, zum Sortieren, Länge verlgeichen (Summary -- Text)

# TODO: Mindestlänge der Texte

# TODO: Texte: (50 .. -->100) .. 2000 Wörter (Token) in Textlänge

# TODO: nicht-lateinische Zeichen/Wörter/Sprachen - Schriftsysteme?

# TODO: Überschneidungen bei den Daten (Kategorien)

# TODO:


# TODO: Kategorie-Länge zum entdecken ausreichend reichhaltiger Kategorien

# TODO: könnte man zu lange Texte in Junks einteilen? --> Anzahl der Texte pro Label würde ja dem Klassifizieren nicht schaden
## eher nicht, wegen overfitting (?)