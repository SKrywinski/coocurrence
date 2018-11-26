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