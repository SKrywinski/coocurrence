#%%
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize
import os
from collections import Counter 
import time
import pandas as pd
import sys
from scipy import sparse
import numpy as np


#%%
#if __name__ == "__main__":
#    wiki_pfad = sys.argv[1]
#else:

#%%
counter = 0

with open(r'D:\informatik_programme\word_embedding\coocurrence\stoppwörter.txt', 'r') as s:
    e = s.readlines()
stopwords = [x.strip() for x in e]

#stopp_wörter = stopwords
satzzeichen = [".", ",", "!", ";", "?", "(", ")", r"'", 
               r"`", ":", r"„", r"''", "%", r"“", "-", 
               "_", r"``", "–", ">", "<", "†", "/"]
#bei neuen Daten wegnehmen
weitere_stopp_wörter = ["doc", "ab", "id=", "url=", "https", "title=",
                        "/doc", "*", "seit", "sowie", "org", "de", "id", "url", "title", "curid", "wikipedia",
                        "für", "über", "wiki"]

stop_words2 = stopwords + satzzeichen + weitere_stopp_wörter

wiki_pfad = r"D:\informatik_programme\word_embedding\text2"

#%%

"""
    1. Häufigsten Wörter erstellen
"""

start_time = time.time()

def get_top_n_words(corpus, n=None):
    """
    List the top n words in a vocabulary according to occurrence in a text corpus.
    
    get_top_n_words(["I love Python", "Python is a language programming", "Hello world", "I love the world"]) -> 
    [('python', 2),
     ('world', 2),
     ('love', 2),
     ('hello', 1),
     ('is', 1),
     ('programming', 1),
     ('the', 1),
     ('language', 1)]
    """
    vec = CountVectorizer(stop_words = stop_words2).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

contents = [open(str(os.path.join(root, datei)), "r", encoding="utf-8").read().lower() for root, dirs, files in os.walk(wiki_pfad, topdown=True) for datei in files]
#print(get_top_n_words(contents, 100))
#zeit = time.time() - start_time
#print("\n")
#print(zeit)

#%%

"""
    2. DataFrame aus tf-dif Werten erstellen
"""

anzahl_der_häufigsten_wörter = 100

häufigsten_wörter_tupelliste = get_top_n_words(contents, anzahl_der_häufigsten_wörter)
#h = [('für', 852030), ('über', 328594), ('de', 265901), ('org', 190248), ('id', 190245), ('wikipedia', 190139), ('wiki', 189759), ('url', 189698), ('title', 189616), ('curid', 189512)]
h2 = {}

for element in häufigsten_wörter_tupelliste:
    key = element[0]
    value = element[1]
    h2[key] = value
print(h2)


#austauschen mit artikel-namen
titel2 = []
counter = 0
"""
for wort in contents:
    counter +=1
    titel2.append("art " + str(counter))
"""

for root, dirs, files in os.walk(wiki_pfad, topdown=True):
    for datei in files:
        d = str(os.path.join(root, datei))
        with open(d, "r", encoding="utf-8") as datei:
            titel2.append(datei.name[:-4])

#%%
my_vectorizer = TfidfVectorizer(sublinear_tf=True, vocabulary=list(h2)) #list(set(häufigsten_wörter_wörterbuch)))
tfidf_matrix = my_vectorizer.fit_transform(contents)
feature_names = my_vectorizer.get_feature_names()

dense = tfidf_matrix.todense()
denselist = dense.tolist()

#%%


df = pd.DataFrame(denselist, columns=h2, index=titel2)
df.to_csv(r'D:\informatik_programme\word_embedding\coocurrence\artikel_top100.csv')

df = df.T
#s = pd.Series(df.loc['stadt'])
#s2 = s[s > 0].sort_values(ascending=False)
#print(s2)
#%%

"""
    3. Nachbarn suchen mit Testwort "Stadt" in contents (sind die ersten 100 Files)
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

metadic = {}
#start_time = time.time()
counter = 0
for wort in h2.keys():
    if wort == "stadt":
        for artikel in contents:
            sätze = sent_tokenize(artikel)
            for satz in sätze:
                wörter = word_tokenize(satz)
                
                dic_liste = nachbarn_suchen10000(2, wörter, wort, h2)
                
                if wort in metadic.keys():
                    temp = dic_liste.get(wort)
                    existing_value = metadic.get(wort)
                    metadic[wort] = temp + existing_value
                else:
                    temp = dic_liste.get(wort)
                    metadic[wort] = temp
                    
                counter += 1


#%%

alle_nachbarn = metadic["stadt"]

metadic = dict(metadic)
#print(metadic)
matrix = pd.DataFrame(metadic)
#matrix = matrix.T
matrix2 = matrix.sort_values(by=["stadt"], ascending = False)
matrix.to_csv(r'D:\informatik_programme\word_embedding\coocurrence\matrix_stadt.csv')
matrix2.to_csv(r'D:\informatik_programme\word_embedding\coocurrence\matrix_stadt_sortiert.csv')      
