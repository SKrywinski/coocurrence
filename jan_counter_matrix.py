#jupyter notebook --notebook-dir="D:\informatik_programme\word_embedding\coocurrence"
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
for tupel in häufigsten_wörter:
    wort = tupel[0]
    häufigkeit = tupel[1]
    häufigsten_wörter_wörterbuch[wort] = häufigkeit
#print(häufigsten_wörter)
#print(häufigsten_wörter_wörterbuch)

"""
def nachbarn_suchen10000(nachbarn, string, zielwort, wörterbuch, k={}):

    nachbarliste = []    
    
    for n, wort in enumerate(string):
        if n - nachbarn <= 0:
            if wort == zielwort:
                nachbarliste.append(string[:n+(nachbarn+1)])        
        elif n + nachbarn > len(string)+1:
            if wort == zielwort:
                nachbarliste.append(string[n-nachbarn:])
        else:
            if wort == zielwort:
                nachbarliste.append(string[n-nachbarn:n+(nachbarn+1)])     
    new_value = []
    for liste in nachbarliste:
        for element in liste:
            if element in wörterbuch.keys():
                new_value.append(element)                
    
    
    
    k[zielwort] = Counter(new_value)
              
    return k


s2 = "jan alexander ist fast so gut wie stefan in python, oder doch nicht jan?"
s3 = word_tokenize(s2)
for word in s3:
    if word in satzzeichen:
        s3.remove(word)
#print(nachbarn_suchen10000(2, s3, "jan", häufigsten_wörter_wörterbuch))


metaliste = []

start_time = time.time()
for datei in alle_sätze_aller_artikel:
    zeit = time.time() - start_time
    if zeit > 10:
        break
    dateiliste = []
    for satz in datei:
        t_satz = word_tokenize(satz)
        for word in t_satz:
            if word in satzzeichen:
                t_satz.remove(word)
            elif word in stopp_wörter:
                t_satz.remove(word)
            elif word in weitere_stopp_wörter:
                t_satz.remove(word)
        dateiliste.append(t_satz)
    metaliste.append(dateiliste)
    
#print(metaliste)

metadic = {}
start_time = time.time()
for wort in häufigsten_wörter_wörterbuch.keys():
    for datei in metaliste:
        zeit = time.time() - start_time
        if zeit > 10:
            break
        for satz in datei:
            dic_liste = nachbarn_suchen10000(2, satz, wort, häufigsten_wörter_wörterbuch)
            
            if wort in metadic.keys():
                temp = dic_liste.get(wort)
                existing_value = metadic.get(wort)
                metadic[wort] = temp + existing_value
            else:
                temp = dic_liste.get(wort)
                metadic[wort] = temp
            
#print(len(metadic))
"""               
#df = pd.DataFrame(metadic, index=häufigsten_wörter_wörterbuch, columns=häufigsten_wörter_wörterbuch)
#df.to_csv("df.csv")

"""
def tf_berechnen(wort, wörterbuch, logarithmus=True):
    if wort in wörterbuch.keys():
        tf = wörterbuch.get(wort)
        if logarithmus == True:
            tf = math.log10(tf)
    else:
        tf = 0
    return tf
"""

def tf_berechnen(wort, pfadstring, logarithmus=True):
    tf = 0
    with open(pfadstring, "r", encoding="utf-8") as datei:
        text = datei.read().lower()
        sätze = sent_tokenize(text)
        for satz in sätze:
            sätze_wörter = word_tokenize(satz)
            for element in sätze_wörter:
                if element == wort:
                    tf +=1
    if logarithmus == True:
        tf = math.log10(tf)
        
    return tf

n = 551238

def idf_wort_in_dokument_anzahl(zielwort):
    #pfad = wiki_pfad
    dokument_anzahl_wortvorkommen = 0
    start_time = time.time()
    
    for datei in alle_sätze_aller_artikel:
        zeit = time.time() - start_time
        if zeit > 6:
            break
        for satz in datei:
            if wort in satz:
                dokument_anzahl_wortvorkommen += 1
                break
                
    """
    #hier noch nach artikeln und nich dokumenten suchen
    for root, dirs, files in os.walk(pfad, topdown=True):
        for datei in files:
            
            zeit = time.time() - start_time
            if zeit > 6:
                break
            d = str(os.path.join(root, datei))
            with open(d, "r", encoding="utf-8") as datei:
                text = datei.read().lower()
                sätze = sent_tokenize(text)
                alle_sätze_aller_artikel.append(sätze)
                for satz in sätze:
                    sätze_wörter = word_tokenize(satz)
    """
    return dokument_anzahl_wortvorkommen

def idf_berechnen(wort, dokument_anzahl, wort_in_dokument_anzahl, logarithmus=True):
    idf = dokument_anzahl / wort_in_dokument_anzahl
    if logarithmus==True:
        idf = math.log10(idf)
    return idf

def tf_idf_berechnen(tf, idf):
    return tf * idf

#print(tf_berechnen("alexander", häufigsten_wörter_wörterbuch))
#print(tf_berechnen("alexander", häufigsten_wörter_wörterbuch, False))
#print(idf_berechnen("alexander", n, idf_wort_in_dokument_anzahl("alexander")))
#print(idf_berechnen("alexander", n, idf_wort_in_dokument_anzahl("alexander"), False))


"""
for root, dirs, files in os.walk(wiki_pfad, topdown=True):
    for datei in files:
        zeit = time.time() - start_time
        #if zeit > 6:
        #    break
        d = str(os.path.join(root, datei))
"""

df_dic = {}

for root, dirs, files in os.walk(wiki_pfad, topdown=True):
    for datei in files:
        tf_idf_dic = {}
        zeit = time.time() - start_time
        if zeit > 10:
            break
        pfad = str(os.path.join(root, datei))

        for wort in häufigsten_wörter_wörterbuch.keys():
            tf_idf_dic[wort] = tf_idf_berechnen(tf_berechnen(wort, pfad), 
                      idf_berechnen(wort, n, idf_wort_in_dokument_anzahl(wort)))
        df_dic[pfad[:-10]] = tf_idf_dic    
    
    
print(df_dic)

"""
df = pd.DataFrame(metadic, index=häufigsten_wörter_wörterbuch, columns=häufigsten_wörter_wörterbuch)
#df.applymap()
df.to_csv("df.csv")

for column in df:
    for row in df.iterrows():
        df.at[row, column] = tf_idf_berechnen(tf_berechnen(column, ))
    df[column]
"""  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
