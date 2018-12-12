# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize, word_tokenize
import os
from collections import Counter 
import time
import pandas as pd
import sys
import numpy as np
from scipy.sparse import csr_matrix
import pickle
import ast


def stoppwoerter_liste_erstellen(stopp_wörter_pfad):
    """
        Stoppwörterliste bauen und durch Satzzeichen und weitere Stoppwörter erweitern
    """
    with open(stopp_wörter_pfad, 'r', encoding="utf-8") as s:
        e = s.readlines()
    stoppwörterliste = [x.strip() for x in e]
    satzzeichen = [".", ",", "!", ";", "?", "(", ")", r"'", 
                   r"`", ":", r"„", r"''", "%", r"“", "-", 
                   "_", r"``", "–", ">", "<", "†", "/"]
    weitere_stopp_wörter = ["doc", "ab", "id=", "url=", "https", "title=",
                            "/doc", "*", "seit", "sowie", "org", "de", "id", "url", "title", "curid", "wikipedia",
                            "für", "über", "wiki"]
    stoppwörter = stoppwörterliste + satzzeichen + weitere_stopp_wörter
    
    return stoppwörter

def woerter_in_text_zaehler(korpus, stopps, laenge=None):
    """
        Gibt die Worthäufigkeit eines Korpus zurück und ignoriert dabei Stoppwörter
        korpus = Liste mit Texten als Strings
        stopps = Liste mit Wörter oder Zeichen als Strings
        laenge = optional kann die Worthäufigkeitsliste gekürzt werden
        
        vectorizer                  --> Wörterverzeichnis aller Wörter des Korpus
        bag_of_words                --> Sparse-Matrix aus dem Wörterverzeichnis erstellen mithilfe des Bag-of-Words-Modell
        woerter_summe               --> Summe der Spalten der Sparse-Matrix erhalten
        wort_haeufigkeit            --> Tupelliste erstellen, wobei ein Tupel aus dem Wort und seiner Anzahl besteht
        wort_haeufigkeit_sortiert   --> Tupelliste wird nach größter Häufigkeit (x[1]) sortiert
    """
    vectorizer = CountVectorizer(stop_words = stopps).fit(korpus) 
    bag_of_words = vectorizer.transform(korpus)
    woerter_summe = bag_of_words.sum(axis=0)
    wort_haeufigkeit = [(wort, woerter_summe[0, index]) for wort, index in vectorizer.vocabulary_.items()]
    wort_haeufigkeit_sortiert = sorted(wort_haeufigkeit, key = lambda x: x[1], reverse=True)
    return wort_haeufigkeit_sortiert[:laenge]


def zwischenspeicherung_der_texte(text_dateien, stoppwoerter, contents, speicherpfad, haeufigste_dic, artikel_name_counter, pickle_speicherung=False):
    """
        Hilfsfunktion für die Zwischenspeicherung von Texten, die entweder als txt- oder pickle-Datei zusammengefasst werden
        text_dateien            = Liste von Texten als Strings
        contents                = Liste der Pfade der erstellten Dateien 
        speicherpfad            = Pfad, wo die Dateien gespeicher werden sollen
        haeufigste_dic          = Counter-Dictionary mit den häufigsten Wörtern
        artikel_name_counter    = durchlaufender Counter für die Benennung der neuen txt- oder pickle-Dateien
        pickle_speicherung      = optional können die zusammengefassten Texte als pickle-Dateien gespeichert werden
    """

    artikel_datei_name = "\wiki_artikel" + str(artikel_name_counter)
    contents.append(artikel_datei_name)
    text_datei_pfad = speicherpfad + artikel_datei_name
        
    if pickle_speicherung == True:
        text_datei_pfad = text_datei_pfad + "pickle"
        pickling_on = open(text_datei_pfad, "wb")
        pickle.dump(text_dateien, pickling_on)
        pickling_on.close()
    else:
        text_datei_pfad = text_datei_pfad + ".txt"
        with open(text_datei_pfad, "w", encoding="utf-8") as korpusartikel:
            korpusartikel.write(str(text_dateien))
                    
    temp_tupelliste = woerter_in_text_zaehler(text_dateien, stoppwoerter)
    temp_dic = dict(temp_tupelliste)
    if not haeufigste_dic:
        haeufigste_dic = Counter(temp_dic)
    else:
        haeufigste_dic = haeufigste_dic + Counter(temp_dic)

    return contents, haeufigste_dic


def korpus_zusammenfassen_und_haeufigste_woerter_berechnen(korpuspfad, stoppwoerter, anzahl_haeufigste_woerter, speicherpfad, 
                                                           max_speicher_artikel=1000, pickle_speicherung=False):
    """
        Berechnet die häufigsten Wörter eines Korpus und fasst 1000 Artikel in einer txt-Datei oder wahlweise einer pickle-Datei zusammen
        korpuspfad          = Pfad zum Korpus
        speicherpfad        = Pfad, wo die Dateien gespeicher werden sollen
        pickle_speicherung  = optional können die zusammengefassten Texte als pickle-Dateien gespeichert werden
    """
       
    text_dateien = []
    contents = []
    artikel_counter = 0
    artikel_name_counter = 0
    haeufigste_dic = {}

    for root, dirs, files in os.walk(korpuspfad, topdown=True):
        for datei in files:
            if artikel_counter >= max_speicher_artikel:
                artikel_name_counter += 1
                contents, haeufigste_dic = zwischenspeicherung_der_texte(text_dateien,
                                                                         stoppwoerter,
                                                                     contents, 
                                                                     speicherpfad, 
                                                                     haeufigste_dic, 
                                                                     artikel_name_counter,
                                                                     pickle_speicherung)
                artikel_counter = 0
                text_dateien = []
            try:
                datei_pfad = str(os.path.join(root, datei))
                with open(datei_pfad, "r", encoding="utf-8", errors='ignore') as artikel:
                    artikel_text = artikel.read().lower()
                    text_dateien.append(artikel_text)
                    artikel_counter += 1
            except FileNotFoundError:
                print("Die Datei wurde nicht gefunden oder konnte nicht geöffnet werden")
                pass
    
    
    haeufigste_dic = Counter(haeufigste_dic)
    haeufigste_dic = haeufigste_dic.most_common(anzahl_haeufigste_woerter)
    haeufigste_dic = dict(haeufigste_dic)

    return contents, haeufigste_dic


def dict_to_list(dictionary):
    return list(dictionary.keys())
    
def nachbarn_aller_woerter(text, size=2):
    """
        Von jedem Wort eines Strings werden die n-nächsten Nachbarn in einer Liste gespeichert,
        wobei n hier durch den Parameter "size" repräsentiert wird
    """
    tokens = word_tokenize(text)
    nachbarn = []
    letzte_worte = []
    for tok in tokens:
        letzte_worte.append(tok)
        if len(letzte_worte) == size:
            nachbarn.append(' '.join(letzte_worte))
            letzte_worte.pop(0)
    return nachbarn

def vokabular_erstellen(haeufigste_list):
    vocab = {}
    for n, wort in enumerate(haeufigste_list):
        vocab[wort] = n
    return vocab

def kookurrenz_matrix(text, stoppwoerter, nachbarn_anzahl, häufigkeits_liste, vectorizer=TfidfVectorizer, gleiches_wort_null=False):
    
    """
        Erstellt eine Term-Term-Matrix aus einem Text
    """
    vocab = vokabular_erstellen(häufigkeits_liste)
    nachbarn = nachbarn_aller_woerter(text, size=nachbarn_anzahl)
    c_vectorizer = vectorizer(stop_words=stoppwoerter, vocabulary=vocab)
    term_document_matrix = c_vectorizer.fit_transform(nachbarn)
    term_term_matrix = (term_document_matrix.T * term_document_matrix)
    
    if gleiches_wort_null:
        term_term_matrix.setdiag(0)
    
    
    ###
    # EVTL. AENDERN!!
    ###
    dense_term_term_matrix = term_term_matrix.todense()    

    return dense_term_term_matrix
    #return term_term_matrix

def aus_contents_matrizen_erstellen(kookurrenzmatrix, haeufigste_list, stoppwoerter, contents, speicherpfad, 
                                    leerung_dateien_im_zwischenspeicher=10, halbestunde=1800, stunde=3600, 
                                    vectorizer=TfidfVectorizer, zwischenspeichern=True, pickle_speichern=False, 
                                    gleiches_wort_null=True):
    """
        speicherpfad = pfad, wo zwischenergebnisse gespeichert werden sollen
    """
    dateien_counter = 0 #Counter wichtig, damit RAM nicht "Überläuft" --> nach jeder 30sten Datei wird dieser wieder auf 0 gesetzt
    temp_wiki_artikel_liste = [] #Speichert bis zu 10 der Pickle-Dateien als String, welche wiederum etwa 1000 Artikel beinhalten (also nach 10000 Artikel wird die Liste geleert)
    zwischenspeicher_counter = 1 #Wichtig für die Zählung der zwischengespeicherten Dateien 
    anzahl_der_dateien_counter = 0 #Zählt, wieviele pickle-Dateien schon verarbeitet wurden
    bereits_verarbeitete_dateien = []
    
    zwischenmatrix_zeit = time.time() #Wird nach einer halben Stunde zurückgesetzt --> somit können Zwischenergebnisse gespeichert werden
    verarbeitete_dateien_zeit = time.time()

    
    
    for pfad in contents:
        
        halbestunde_zwischenergebnis = time.time() - zwischenmatrix_zeit
        stunde_zwischenergebnis = time.time() - verarbeitete_dateien_zeit
        
        if stunde_zwischenergebnis >= stunde and zwischenspeichern == True:
            verarbeitete_dateien_txt = r"\zwischenergebnisse\verarbeitete_dateien.txt"
            verarbeitete_dateien_pfad = speicherpfad + verarbeitete_dateien_txt
            
            with open(verarbeitete_dateien_pfad, "w", encoding="utf-8") as verarbeitet:
                try:
                    for element in bereits_verarbeitete_dateien:
                        verarbeitet.write("%s\n" % element)
                except:
                    pass
            #Der Zwischenergebnis-Timer für die bereits verarbeiteten Dateien wird zurückgesetzt
            stunde_zwischenergebnis = time.time()
        
        if halbestunde_zwischenergebnis >= halbestunde and zwischenspeichern == True:
            str_zwischen = str(zwischenspeicher_counter)
            
            if pickle_speichern == True:
                pickle_matrix_pfad = speicherpfad + str_zwischen + ".pkl"
                kookurrenzmatrix.to_pickle(pickle_matrix_pfad)
            else:
                txt_matrix_pfad = speicherpfad + str_zwischen + ".txt"
                kookurrenzmatrix.to_pickle(txt_matrix_pfad)
            
            #Der Zwischenergebnis-Timer für die Matrixspeicherung wird zurückgesetzt
            halbestunde_zwischenergebnis = time.time()
            zwischenspeicher_counter += 1
            
            pickles_anzahl_txt = r"\zwischenergebnisse\pickles_anzahl.txt"
            pickles_anzahl_pfad = speicherpfad + pickles_anzahl_txt
            
            with open(pickles_anzahl_pfad, "w", encoding="utf-8") as zwischen:
                try:
                    meldung_verarbeitete_pickles = "Schon %s Pickles verarbeitet.\n" % anzahl_der_dateien_counter
                    zwischen.write(meldung_verarbeitete_pickles)
                    print(meldung_verarbeitete_pickles)
                except:
                    pass
                
        #bei jeder zehnten pickle-Datei wird die Liste der Wiki-Artikel geleert und mit der Hauptmatrix zusammengefügt
        if dateien_counter >= leerung_dateien_im_zwischenspeicher:
            for wiki_artikel in temp_wiki_artikel_liste:
                temp_matrix = kookurrenz_matrix(wiki_artikel, stoppwoerter, 2, haeufigste_list, vectorizer, gleiches_wort_null=True)
                kookurrenzmatrix += temp_matrix
            temp_wiki_artikel_liste = []
            dateien_counter = 0
            anzahl_der_dateien_counter += leerung_dateien_im_zwischenspeicher
            
            
        
        # 
        file_name = str(pfad)
        dateipfad = speicherpfad + file_name

        
        if pickle_speichern == True:
            dateipfad = dateipfad + "pickle"
            with (open(dateipfad, "rb")) as pickle_datei:
                while True:
                    try:
                        temp_pickle_liste = pickle.load(pickle_datei)
                        temp_pickle_str = "".join(temp_pickle_liste)
                        temp_wiki_artikel_liste.append(temp_pickle_str)
                    except EOFError:
                        break
        else:
            dateipfad = dateipfad + ".txt"
            with open(dateipfad, "r") as txt_datei:
                try:
                    temp_txt_liste = txt_datei.read()
                    temp_txt_str = "".join(temp_txt_liste)
                    temp_wiki_artikel_liste.append(temp_txt_str)
                except EOFError or UnicodeDecodeError:
                    pass
        
        dateien_counter += 1
        bereits_verarbeitete_dateien.append(file_name)
        
    return kookurrenzmatrix

        

def n_naechsten_nachbarn(zielwort, vokabular, dense_kookurrenz_matrix, n=10):

    try:
        index = vokabular[zielwort]
    except KeyError:
        return None
    
    # Gibt der Matrix eine neue Form, ohne ihre Struktur zu verändern
    vektor = dense_kookurrenz_matrix[index].reshape(1, -1)
    
    #berechnet die cosine similarity des Vektors des Zielwortes für die gesamte Matrix
    sim = cosine_similarity(vektor, dense_kookurrenz_matrix)
    
    
    ### ERKLÄREN!
    naechste_nachbarn_liste = sorted(vokabular.keys(), key=lambda w: sim[0][vokabular[w]], reverse=True)[:n]
    naechste_nachbarn_liste = map(lambda n: (n, sim[0][vokabular[n]]), naechste_nachbarn_liste)

    return naechste_nachbarn_liste
    

"""
    Wichtig für die CLI-Ausführung (CLI = Command Line Interfaces)
"""

programm_lauf_zeit = time.time()
wiki_pfad = r"D:\informatik_programme\word_embedding\text\’"
stopp_wörter_pfad = r'D:\informatik_programme\word_embedding\coocurrence\stoppwoerter.txt'
"""
if __name__ == "__main__":
    wiki_pfad = sys.argv[1]
    stopp_wörter_pfad = sys.argv[2]
"""

"""
    Essentielle Varibalen, wobei einige Variabelenwerte durch Eingabe der Benutzer bestimmt werden können
"""


programm_lauf_zeit = time.time()
wiki_pfad = r"D:\informatik_programme\word_embedding\text\Q"
stopp_wörter_pfad = r'D:\informatik_programme\word_embedding\coocurrence\stoppwoerter.txt'

anzahl_haeufigste_woerter = 100 #HIER INPUT
leerung_dateien_im_zwischenspeicher = 3 #HIER INPUT
speicherpfad = r"C:\Users\Jan\Desktop\zeug" #HIER INPUT
max_speicher_artikel = 10  #HIER INPUT
#NICHT False setzen, da bei txt-Dateien noch Fehler
pickle_speicherung = True #HIER INPUT
zielwort = "stadt" #HIER INPUT
anzahl_der_naechsten_nachbarn = 10


"""
    Aufrufen der Funktionen
"""
 
stoppwoerter = stoppwoerter_liste_erstellen(stopp_wörter_pfad)
generierte_dateien_verzeichnis_liste, haeufigste_dic = korpus_zusammenfassen_und_haeufigste_woerter_berechnen(wiki_pfad,
                                                                                                                stoppwoerter,
                                                                                                                anzahl_haeufigste_woerter,
                                                                                                                speicherpfad,
                                                                                                                max_speicher_artikel=max_speicher_artikel,
                                                                                                                pickle_speicherung=pickle_speicherung)

#Umwandlung wichtig für die Spalten- und Zeilenbenennung der Matrix
haeufigste_list = dict_to_list(haeufigste_dic)
leere_matrix = csr_matrix((anzahl_haeufigste_woerter, anzahl_haeufigste_woerter), dtype=int)     
kookurrenzmatrix = aus_contents_matrizen_erstellen(leere_matrix, haeufigste_list, stoppwoerter, generierte_dateien_verzeichnis_liste, speicherpfad, 
                                                   leerung_dateien_im_zwischenspeicher=leerung_dateien_im_zwischenspeicher, 
                                                   halbestunde=1800, stunde=3600, zwischenspeichern=True, 
                                                   pickle_speichern=pickle_speicherung, gleiches_wort_null=False)




#%%
"""
    Kookurrenzmatrix in Dataframe umwandeln und als csv-Datei speichern
"""

kook_liste = kookurrenzmatrix.tolist()
df = pd.DataFrame(kook_liste, index=haeufigste_list, columns=haeufigste_list)  
df.to_csv(speicherpfad + "\kookurrenzmatrix.csv")


#%%
"""
    n nächsten Nachbarn ausgeben und speichern
"""


vokabular = vokabular_erstellen(haeufigste_list)
n_naechste_nachbarn_liste = n_naechsten_nachbarn(zielwort, vokabular, kookurrenzmatrix, n=anzahl_der_naechsten_nachbarn)
n_naechste_nachbarn_pfad = speicherpfad + r"\\" +  str(anzahl_der_naechsten_nachbarn) + "_naechsten_nachbarn_von_" + zielwort

with open(n_naechste_nachbarn_pfad, "w") as f:
    f.write(str(n_naechste_nachbarn_liste))

rueckgabe_naechsten_nachbarn = "Die " + str(anzahl_der_naechsten_nachbarn) + "nächsten Nachbarn von dem Wort " + zielwort + " sind: \n"

print(rueckgabe_naechsten_nachbarn)
for nachbar in n_naechste_nachbarn_liste:
    print(*n_naechste_nachbarn_liste)
      
end_zeit = time.time() - programm_lauf_zeit
print(end_zeit)





