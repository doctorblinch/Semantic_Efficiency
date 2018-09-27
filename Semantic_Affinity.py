import re
from math import exp
from operator import itemgetter
from gensim.models import Word2Vec

def split_into_sentences(text):
    caps = "([A-Z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def deleteUneffective(text):
    fin = open("unInfluencive.words","r")
    tmp = fin.read()
    nonInfluenciveWords = tmp.split()
    nonInfluenciveWords.append(tmp.split())
    fin.close()
    words = text.split()
    for word in words:
        if word in nonInfluenciveWords:
            words.remove(word)
    text = ' '.join(words)
    return (text)


def output(order,text,mainSent):
    print("\n\n\n######################################################\nLadies and Gentelmen, the result found!\n\n\n")
    sentences = split_into_sentences(text)
    mainSentence = sentences[mainSent]
    sentences.remove(sentences[mainSent])
    lastestLast = []
    for i in order:
        lastestLast.append(sentences[i.number])
    return lastestLast

class WordForEmb:
    num = []
    words = []

def main(text,mainSent):
    sentences = split_into_sentences(text)
    sentences_ted = []
    counter = 0
    for i in range(len(sentences)):
        sentences_ted.append(sentences[i].split())
    #print(sentences_ted)
    model = Word2Vec(min_count=1)
    model.build_vocab(sentences_ted)
    model.train(sentences_ted, total_examples=model.corpus_count, epochs=model.iter)

    ######################################
    count = WordForEmb()
    print(mainSent)
    for wordsOfSent in sentences[mainSent].split():
        #print(wordsOfSent)
        for i in range(5):
            w = model.most_similar(wordsOfSent)[i][0]
            n = model.most_similar(wordsOfSent)[i][1]
            if not (w in count.words):
                count.words.append(w)
                count.num.append(n)
            else:
                count.num[count.words.index(w)] += n

#    print(count.words, count.num)
    afficiencyOfEachSentence = []
    afficiencyOfEachSentence.append(0)
    counter = 0
    for sentence in sentences:
        for i in sentence.split():
            if (i in count.words):
                #print(counter)
                afficiencyOfEachSentence[counter] += count.num[count.words.index(i)]
        counter += 1
        afficiencyOfEachSentence.append(0)
    #print(afficiencyOfEachSentence)
    return afficiencyOfEachSentence

if __name__ == "__main__":
    fin = open("in.txt","r")
    textOriginal = fin.read()
    text = deleteUneffective(textOriginal)
    number = (int)(input())
    arr = main(text,number)
    sentences = split_into_sentences(textOriginal)
    for i in range(len(arr)):
        print(sentences[arr.index(max(arr))])
        arr[arr.index(max(arr))] = 0

def outDoorCall(textOriginal,number):
    text = deleteUneffective(textOriginal)
    arr = main(text, (int)(number))
    s = []
    sentences = split_into_sentences(textOriginal)
    for i in range(len(arr)):
        s.append(sentences[arr.index(max(arr))-1])
        arr[arr.index(max(arr))] = -1
    return s