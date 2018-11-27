"""
    Wörterzählen mithilfe von Counter
"""
"""
counter_liste = Counter()
zeit = 0

for root, dirs, files in os.walk(wiki_pfad, topdown=True):
    #if counter >= 3000:
    #    break
    for datei in files:
        if counter >= 30:
            break
        d = str(os.path.join(root, datei))
        c_counter_liste = Counter()
        with open(d, "r", encoding="utf-8") as artikel:
            text = artikel.read().lower()
            #liste = sent_tokenize(text)
            wörter = word_tokenize(text)
            reduzierte_wörter = []
            for wort in wörter:
                if wort in stopp_wörter:
                    pass
                elif wort in satzzeichen:
                    pass
                else:
                    reduzierte_wörter.append(wort)
            if counter == 0:
                counter_liste = Counter(reduzierte_wörter).most_common(15)
                #ACHTUNG: most_common gibt eine Liste, keinen Counter zurück
            else:
                temp_counter = Counter(reduzierte_wörter)
                counter_liste2 = Counter(counter_liste) + temp_counter
                counter_liste = counter_liste2.most_common(15)
            
        counter += 1
        zeit = zeit + timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
        print(zeit)
print(counter_liste)

test_liste = []
for element in counter_liste:
    test_liste.append(element[0])
print(test_liste)

matrix = pd.DataFrame(0, index=test_liste, columns=test_liste)
print(matrix)
"""

"""
    Versuch eines Dataframes
"""
"""
a = pd.Series(häufigsten_wörter_wörterbuch)
b = pd.Series(häufigsten_wörter_wörterbuch.values(), index=häufigsten_wörter_wörterbuch)
#print(b)
matrix2 = pd.DataFrame(häufigsten_wörter_wörterbuch, index=häufigsten_wörter_wörterbuch)
#print(matrix2)
matrix3 = pd.DataFrame.from_dict(häufigsten_wörter_wörterbuch, orient="index")
print(matrix3)
"""
"""
from nltk.tokenize import sent_tokenize, word_tokenize
import os
from stop_words import get_stop_words
from collections import Counter 
<<<<<<< HEAD
import timeit


wiki_pfad = r"D:\informatik_programme\word_embedding\wikipedia_kookurrenz\text"
counter = 0

satzzeichen = [".", ",", "!", ";", "?", "(", ")", r"'", 
               r"`", ":", r"„", r"''", "%", r"“", "-", 
               "_", r"``", "–", ">", "<", "†", "/",
               "doc", "ab", "id=", "url=", "https", "title=",
               "/doc", "*", "seit", "sowie"]
stopp_wörter = get_stop_words('de') #type = Liste
top_100 = [('wurde', 1281), ('doc', 518), ('id=', 518), ('url=', 518), ('https', 518), 
           ('//de.wikipedia.org/wiki', 518), ('title=', 518), ('/doc', 518), ('jahr', 268), 
           ('wurden', 252), ('ab', 248), ('*', 223), ('seit', 216), ('sowie', 213), ('mitglied', 186), 
           ('jahren', 162), ('ersten', 161), ('zwei', 156), ('oktober', 146), ('jahre', 144), 
           ('kam', 133), ('†', 131), ('saison', 130), ('teil', 129), ('2009', 126), ('juni', 122), 
           ('stadt', 118), ('zweiten', 117), ('später', 117), ('drei', 114), ('1.', 112), ('zeit', 112), 
           ('mai', 111), ('ende', 107), ('dezember', 106), ('gehörte', 105), ('jedoch', 104), ('november', 102), 
           ('erste', 102), ('juli', 101), ('september', 100), ('erhielt', 100), ('deutschen', 99), ('april', 99), 
           ('januar', 98), ('märz', 96), ('august', 95), ('liegt', 94), ('müller', 94), ('altenburg', 92), 
           ('de', 91), ('the', 91), ('beim', 90), ('bereits', 89), ('nahm', 89), ('heute', 86), ('etwa', 84), 
           ('mehr', 83), ('universität', 82), ('of', 81), ('deutscher', 79), ('ort', 79), ('konnte', 79), 
           ('tätig', 77), ('neben', 76), ('vier', 76), ('folgender', 76), ('februar', 74), ('trat', 72), 
           ('spielte', 72), ('zudem', 71), ('weitere', 71), ('2.', 70), ('personen', 70), ('politiker', 70), 
           ('bekannt', 69), ('kirche', 69), ('namen', 68), ('gewann', 68), ('bzw', 68), ('zunächst', 67), 
           ('zurück', 67), ('nachdem', 67), ('begann', 67), ('new', 67), ('band', 67), ('herzogtum', 67), 
           ('gab', 66), ('1945', 64), ('2008', 64), ('name', 64), ('landkreis', 64), ('denen', 63), 
           ('zusammen', 63), ('außerdem', 63), ('stand', 62), ('neu', 62), ('beiden', 62), ('platz', 61), 
           ('johann', 61)]

counter_liste = Counter()
zeit = 0
for root, dirs, files in os.walk(wiki_pfad, topdown=True):
    #if counter >= 3000:
    #    break
    for datei in files:
        #if counter >= 50000:
        #    break
        d = str(os.path.join(root, datei))
        c_counter_liste = Counter()
        with open(d, "r", encoding="utf-8") as artikel:
            text = artikel.read().lower()
            #liste = sent_tokenize(text)
            wörter = word_tokenize(text)
            reduzierte_wörter = []
            for wort in wörter:
                if wort in stopp_wörter:
                    pass
                elif wort in satzzeichen:
                    pass
                else:
                    reduzierte_wörter.append(wort)
            if counter == 0:
                counter_liste = Counter(reduzierte_wörter).most_common(15)
                #ACHTUNG: most_common gibt eine Liste, keinen Counter zurück
            else:
                temp_counter = Counter(reduzierte_wörter)
                counter_liste2 = Counter(counter_liste) + temp_counter
                counter_liste = counter_liste2.most_common(15)
            
        counter += 1
        zeit = zeit + timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
        print(zeit)
print(counter_liste)
=======
import time

"""
        
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
    #for-Schleife, die die Häufigkeit aller Wörter zählt außer den Satzzeichen
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

"""

sorted(counter_wörterbuch.values())
häufigsten_wörter = Counter(counter_wörterbuch).most_common(10)
print(häufigsten_wörter)


>>>>>>> c765aeb9884e0cd668640146b8efdc93eb9be419
"""

"""
nachbar_wörterbuch = None
start_time = time.time()
for datei in alle_sätze_aller_artikel:
    zeit = time.time() - start_time
    if zeit > 3:
        break
    for satz in datei:
        t_satz = word_tokenize(satz)
        for word in t_satz:
            if word in satzzeichen:
                t_satz.remove(word)
            elif word in stopp_wörter:
                t_satz.remove(word)
            elif word in weitere_stopp_wörter:
                t_satz.remove(word)
            #elif word, anzahl in häufigsten_wörter_wörterbuch
        nachbar_wörterbuch = nachbarn_suchen(2, t_satz)
        for k,v in nachbar_wörterbuch.items():
            if k in häufigsten_wörter_wörterbuch.keys():
                if k in meta_dic.keys():
                    meta_dic[k] += v
                else:
                    meta_dic[k] = v
"""
#print(meta_dic)                    
"""        
for k,v in nachbar_wörterbuch.items():
    for liste in v:
        meta_dic[k] = Counter(liste)
"""
      
        
"""
        for k,v in nachbar_wörterbuch.items():
            if k in häufigsten_wörter_wörterbuch:
                if k2,v2 in meta_dic.items():
                    
                    meta_dic[k2] = v + v2 #stimmt? nein bestimmt nicht
                else:
                    meta_dic[k2] = v2
"""

#c = Anzahl der Nachbarn einer Seite, string = vortokenisierter satz, k = ergebnis_dictionary
def nachbarn_suchen(nachbarn, string, zielwort, k={}):
    wort = zielwort
    for n, wort in enumerate(string):
        if n - nachbarn <= 0:
            if wort not in k.keys():
                k[wort] = []
                k[wort] = string[:n+(nachbarn+1)]
            else:
                k[wort] += string[:n+(nachbarn+1)]
        elif n + nachbarn > len(string)+1:
            if wort not in k.keys():
                k[wort] = []
                k[wort] = string[n-nachbarn:]
            else:
                k[wort] += string[n-nachbarn:]
        else:
            if wort not in k.keys():
                k[wort] = []
                k[wort] = string[n-nachbarn:n+(nachbarn+1)]
            else:
                k[wort] += string[n-nachbarn:n+(nachbarn+1)]
    return k

def nachbarn_suchen2(nachbarn, string, zielwort, wörterbuch, k={}):
    wort = zielwort
    for n, wort in enumerate(string):
        if n - nachbarn <= 0:
            if wort not in k.keys():
                k[wort] = []
                k[wort] = string[:n+(nachbarn+1)]
            else:
                k[wort] += string[:n+(nachbarn+1)]
        elif n + nachbarn > len(string)+1:
            if wort not in k.keys():
                k[wort] = []
                k[wort] = string[n-nachbarn:]
            else:
                k[wort] += string[n-nachbarn:]
        else:
            if wort not in k.keys():
                k[wort] = []
                k[wort] = string[n-nachbarn:n+(nachbarn+1)]
            else:
                k[wort] += string[n-nachbarn:n+(nachbarn+1)]
    
    """
    temp_v = k.get(wort)
    new_value = []
    for element in temp_v:
        if element in wörterbuch.keys():
            new_value.append(element)
    """
    
    return k

s = ["jan", "ist", "fast", "so", "gut", "wie", "stefan", "in", "python", ",", "oder", "doch" "nicht" "?"]
s2 = "jan ist fast so gut wie stefan in python, oder doch nicht jan?"
s3 = word_tokenize(s2)
for word in s3:
    if word in satzzeichen:
        s3.remove(word)
#print(nachbarn_suchen3(2, s3, "jan", häufigsten_wörter_wörterbuch))