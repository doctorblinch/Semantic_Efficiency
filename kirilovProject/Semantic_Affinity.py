import re
from math import exp
from operator import itemgetter

class Sentence:
    def __init__(self):
        return
    kOfSimilarity = 0
    number = 0


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

def distance(a, b):
   n, m = len(a), len(b)
   if n > m:
      a, b = b, a
      n, m = m, n

   current_column = range(n+1)
   for i in range(1, m+1):
      previous_column, current_column = current_column, [i]+[0]*n
      for j in range(1,n+1):
         add, delete, change = previous_column[j]+1, current_column[j-1]+1, previous_column[j-1]
         if a[j-1] != b[i-1]:
            change += 1
         current_column[j] = min(add, delete, change)

   return current_column[n]



def getText():
    fin = open("in.txt","r")
    string = fin.read()
    print(string)
    return string

def deleteUneffective(text):
    nonInfluenciveWords = ['not','yes','on','or','not','under','between','because','through','behind','begin','after','into','to','from','just','for','some','any','that','by','he','she','it','they','we','i','I','the','my','her','his','with','as','a','of','is','are','were','was','been','have','had','when','where','which','you','what']
    words = text.split()
    for word in words:
        if word in nonInfluenciveWords:
            words.remove(word)
    text = ' '.join(words)
    return (text)

def mainSentence():
    fin = open("inNum.txt","r")
    a = (int)(fin.read())
    return a

def f(x):
    return 1/exp(x/2)

def quickSort(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0].kOfSimilarity
        for x in array:
            if x.kOfSimilarity > pivot:
                less.append(x)
            if x.kOfSimilarity == pivot:
                equal.append(x)
            if x.kOfSimilarity < pivot:
                greater.append(x)
        return quickSort(less)+equal+quickSort(greater)
    else:
        return array

def output(order,text,mainSent):
    print("\n\n\n######################################################\nLadies and Gentelmen, the result found!\n\n\n")
    sentences = split_into_sentences(text)
    mainSentence = sentences[mainSent]
    sentences.remove(sentences[mainSent])
    lastestLast = []
    for i in order:
        lastestLast.append(sentences[i.number])
        #print(sentences[i.number])
    return lastestLast


def sorting(text, numberOfMain):
    sentences = split_into_sentences(text)
    mainSent = sentences[numberOfMain]
    sentences.remove(sentences[numberOfMain])
    a = [0] * len(sentences)
    wordsInMainSent = mainSent.split()


    obj = [ Sentence() for i in range(len(sentences))]

    counter = 0
    for currentSent in sentences:
       sum = 0
       for mWord in wordsInMainSent:
           curSent = currentSent.split()
           for curWord in curSent:
               sum = f(distance(mWord,curWord))
           a[counter] = sum
           obj[counter].number = counter
           obj[counter].kOfSimilarity = sum
       counter +=1

    ##############################################
  #  for i in obj:
 #       print(i.number,i.kOfSimilarity, sep = ' ')
    obj = quickSort(obj)
    #obj.sort(key=itemgetter('number'))
    obj = sorted(obj, key=lambda num: num.kOfSimilarity)
  #  print('\n\n\n')
    ##############################################
   # for i in obj:
    #   print(i.number,i.kOfSimilarity, sep = ' ')

    return obj




def main():
  mainSent = mainSentence()
  text = getText()
  string = deleteUneffective(text)
  print('\n\n\n')
  order = sorting(string,mainSent)
  finalText = output(order,text,mainSent)
  return finalText

#main()
