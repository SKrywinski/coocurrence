from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize
import os
from collections import Counter 
import time
import pandas as pd
import math


wiki_pfad = r"D:\informatik_programme\word_embedding\wikipedia_kookurrenz\text2"
counter = 0


with open('stopwords.txt', 'r') as s:
    e = s.readlines()
stopwords = [x.strip() for x in e]

stopp_wörter = stopwords
satzzeichen = [".", ",", "!", ";", "?", "(", ")", r"'", 
               r"`", ":", r"„", r"''", "%", r"“", "-", 
               "_", r"``", "–", ">", "<", "†", "/"]
weitere_stopp_wörter = ["doc", "ab", "id=", "url=", "https", "title=",
                        "/doc", "*", "seit", "sowie"]

counter_wörterbuch = dict()
wort_von_wiki_counter = 0
start_time = time.time()
s = '<doc id="'
alle_sätze_aller_artikel = []
"""
for root, dirs, files in os.walk(wiki_pfad, topdown=True):
    for datei in files:
        zeit = time.time() - start_time
        if zeit > 60:
            break
        d = str(os.path.join(root, datei))
        with open(d, "r", encoding="utf-8") as datei:
            
            text = datei.read().lower()
            sätze = sent_tokenize(text)
            alle_sätze_aller_artikel.append(sätze)
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
         
#print("Anzahl der Wörter: " + str(wort_von_wiki_counter))
#print(len(counter_wörterbuch))
#print(dateicounter)


sorted(counter_wörterbuch.values())
häufigsten_wörter = Counter(counter_wörterbuch).most_common(10)
häufigsten_wörter_wörterbuch = {}
vocab = []
for tupel in häufigsten_wörter:
    wort = tupel[0]
    vocab.append(wort)
    häufigkeit = tupel[1]
    häufigsten_wörter_wörterbuch[wort] = häufigkeit
    
print(häufigsten_wörter_wörterbuch)
"""

#stopp_wörter = ...
#sublinear beudeutet log10 + 1, wie im Text
#vectorizer = TfidfVectorizer(sublinear_tf=True, vocabulary
                             #stop_words=stopp_wörter)

#häufigsten10Wörter = häufigste_wörter_wörterbuch.most_common(10)
#liste
                             

counter = 1
meta_inhalt = []

vocab2 = []
for word in häufigsten_wörter_wörterbuch.keys():
    vocab2.append(word)

"""
for root, dir .... 
	if counter >= 10:
		break


	inhalt = [open(file, encoding="utf-8").read().lower() for file in files]

	ODER
"""
#inhalt = [open(str(os.path.join(root, datei)), encoding="utf-8").read().lower() counter+=1 ]
wiki_pfad2 = r"D:\informatik_programme\word_embedding\wikipedia_kookurrenz\text2\AA\wiki_55"
#inhalt = open(wiki_pfad2, encoding="utf-8").read().lower()
#inhalt = word_tokenize(inhalt)
inhalt = ["ert den Zustand der Atmosphäre an einem bestimmten Ort und zu einem bestimmten Zeitpunkt. Kennzeichnend sind die meteorologischen Elemente Strahlung, Luftdruck, Lufttemperatur, Luftfeuchtigkeit und Wind, sowie die daraus ableitbaren Elemente Bewölkung, Niederschlag, Sichtweite etc. Das Wetter ist das augenblickliche Bild eines Vorganges (Wettergeschehen), das sich hauptsächlich in der Troposphäre abspielt. Es kann sich – im Gegensatz zur Wetterlage und Witterung – mehrmals täglich ändern. Ueshiba Morihei (jap. ; * 14. Dezember 1883 in Nishinotani, Nishimuro-gun (heute Tanabe), Präfektur Wakayama; † 26. April 1969 in Iwama) war der Begründer der modernen japanischen Kampfkunst Aikidō."]
inhalt2 = []
for wort in inhalt:
    a = word_tokenize(wort)
    inhalt2 += a
    
print(inhalt2)
    

    
häufigsten_wörter2 = Counter(inhalt2).most_common(10)
häufigsten_wörter_wörterbuch2 = {}
for tupel in häufigsten_wörter2:
    wort = tupel[0]
    vocab.append(wort)
    häufigkeit = tupel[1]
    häufigsten_wörter_wörterbuch2[wort] = häufigkeit
    
print(häufigsten_wörter_wörterbuch2)

vocab2 = []
for word in häufigsten_wörter_wörterbuch2.keys():
    vocab2.append(word)
print(vocab2)
"""
for root, dirs, files in os.walk(wiki_pfad, topdown=True):
    for datei in files:
        if counter >= 10:
            inhalt.append(open(str(os.path.join(root, datei)), encoding="utf-8").read().lower())
            counter += 1
"""

inhalt3 = ""

for wort in inhalt2:
    inhalt3.join(wort)



#stopp_wörter = ...
#sublinear beudeutet log10 + 1, wie im Text
vectorizer = TfidfVectorizer(vocabulary=vocab2) #stop_words=stopp_wörter)
#sublinear_tf=True, 

tfidf_matrix = vectorizer.fit_transform(inhalt)
feature_names = vectorizer.get_feature_names()
dense = tfidf_matrix.todense()
denselist = dense.tolist()

df = pd.DataFrame(denselist, columns=feature_names, index=vocab2)
df.to_csv("a.csv")
print(df)






