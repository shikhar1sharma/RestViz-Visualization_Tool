# coding=utf-8
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import string
import mysql.connector


stemmer = PorterStemmer()


con = mysql.connector.connect(database="yelp",user="root", host= "localhost", password="admin123");
cursor = con.cursor()


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


def word_count(text):

    lowers = text.lower()
    translator = str.maketrans('', '', string.punctuation)
    lowers_without_punctuations = lowers.translate(translator)
    word_tokens = word_tokenize(lowers_without_punctuations)
    stems = stem_tokens(word_tokens, stemmer)

    stop_words = set(stopwords.words('english'))

    filtered_text = [w for w in word_tokens if not w in stop_words]

    wordlist = wordListToFreqDict(filtered_text)
    sorteddict = sortFreqDict(wordlist)

    return (sorteddict)






reviewDict = dict()
businessIds= []
file = open('review_final.csv', encoding="utf8")

with open('review_final.csv', encoding="utf8") as csvfile:
    review_reader = csv.reader(csvfile, delimiter=',')
    for row in review_reader:
        if not row[1] in reviewDict:
            reviewDict[row[1]]=row[5]
            businessIds.append(row[1])
        else:
            reviewDict[row[1]] = reviewDict[row[1]]+ row[5]

businessList = set(businessIds)

print(len(reviewDict))

wordCloud = []
i=0
for business in businessList:
    #print(reviewDict[business])
    wordcount_pairs = word_count(reviewDict[business])[:50]
    wordCloud.append({"business_id":business, "count": wordcount_pairs})

    words = ""
    counts=""
    for  tuple in wordcount_pairs:
        words = words + str(tuple[0])
        words = words + ","
        counts = counts + tuple[1]
        counts = counts + ","

    cursor.execute("""INSERT INTO wordcloud VALUES (%s,%s,%s)""", (business, words[:-1],counts[:-1]))
    con.commit()
    print(i)
    i = i + 1


print("done")