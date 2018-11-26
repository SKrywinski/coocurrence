from nltk.tokenize import sent_tokenize, word_tokenize
import os
from stop_words import get_stop_words
from collections import Counter 
import time

"""
        jupyter notebook --notebook-dir="D:\informatik_programme\word_embedding\coocurrence"
"""
wiki_pfad = r"D:\informatik_programme\word_embedding\wikipedia_kookurrenz\text"
counter = 0

stopp_wörter = get_stop_words('de') #type = Liste
satzzeichen = [".", ",", "!", ";", "?", "(", ")", r"'", 
               r"`", ":", r"„", r"''", "%", r"“", "-", 
               "_", r"``", "–", ">", "<", "†", "/"]
weitere_stopp_wörter = ["doc", "ab", "id=", "url=", "https", "title=",
                        "/doc", "*", "seit", "sowie"]

counter_wörterbuch = dict()
wort_von_wiki_counter = 0
start_time = time.time()

"""
    for-Schleife, die die Häufigkeit aller Wörter zählt außer den Satzzeichen
"""
for root, dirs, files in os.walk(wiki_pfad, topdown=True):
    for datei in files:
        zeit = time.time() - start_time
        if zeit > 60:
            break
        d = str(os.path.join(root, datei))
        with open(d, "r", encoding="utf-8") as artikel:
            text = artikel.read().lower()
            sätze = sent_tokenize(text)
            
            for satz in sätze:
                sätze_wörter = word_tokenize(satz)
                
                for wort in sätze_wörter:
                    if wort in stopp_wörter:
                        wort_von_wiki_counter += 1 
                        pass
                    elif wort in weitere_stopp_wörter:
                        wort_von_wiki_counter += 1 
                        pass
                    elif wort in satzzeichen:
                        pass
                    else:
                        wort_von_wiki_counter += 1
                        if wort not in counter_wörterbuch:
                            counter_wörterbuch[wort] = 1
                        else:
                            counter_wörterbuch[wort] += 1
            
            counter += 1        

#print(counter_wörterbuch)
print("\n")
print("Anzahl der Wörter: " + str(wort_von_wiki_counter))
print("\n")

"""
    ???
"""

sorted(counter_wörterbuch.values())
häufigsten_wörter = Counter(counter_wörterbuch).most_common(10)
print(häufigsten_wörter)



