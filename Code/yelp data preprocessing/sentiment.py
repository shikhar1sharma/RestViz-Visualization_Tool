# coding=utf-8


from textblob import TextBlob
import mysql.connector
import csv



con = mysql.connector.connect(database="yelp",user="root", host= "localhost", password="admin123");

cursor = con.cursor()


reviewDict = dict()

with open('review_final.csv', encoding='utf8') as csvfile:
    review_reader = csv.reader(csvfile, delimiter=',')
    senti=''
    for row in review_reader:
        #print row
        sentiment = TextBlob(row[5]).sentiment
        if(sentiment[0]>0.2):
            senti = "positive"
        elif(sentiment[0]<-0.1):
            senti = "negative"
        else:
            senti = "neutral"
        if(row[1] not in reviewDict):
            reviewDict[row[1]] = {"positive": 0, "negative": 0, "neutral": 0,'count':0, 'ratingValues':[]}
            reviewDict[row[1]][senti] = reviewDict[row[1]][senti]+1
            reviewDict[row[1]]['count'] = reviewDict[row[1]]['count'] +1
            reviewDict[row[1]]['ratingValues'].append(row[3])
        else:
            reviewDict[row[1]][senti] = reviewDict[row[1]][senti] + 1
            reviewDict[row[1]]['count'] = reviewDict[row[1]]['count'] + 1
            reviewDict[row[1]]['ratingValues'].append(row[3])

#print(reviewDict)

for item in reviewDict:

    ratingsVal = reviewDict[item]['ratingValues']
    sum = 0
    for num in ratingsVal:
        sum = sum + int(num)

    reviewDict[item]['rating'] = sum / float(reviewDict[item]['count'])

    maxcolor = ""
    if reviewDict[item]["positive"] >= reviewDict[item]["negative"]:
        if reviewDict[item]["positive"] >= reviewDict[item]["neutral"]:
            maxcolor = "positive"
        else:
            if reviewDict[item]['rating']<2.5:
                maxcolor = "negative"
            else:
                maxcolor = "neutral"
    elif reviewDict[item]["negative"] >= reviewDict[item]["neutral"]:
        maxcolor = "negative"
    else:
        if reviewDict[item]['rating'] < 2.5:
            maxcolor = "negative"
        else:
            maxcolor = "neutral"

    reviewDict[item]["sentiment"]= maxcolor
    try:
        cursor.execute("""INSERT INTO business_review VALUES (%s,%s,%s,%s,%s,%s)""", (item, reviewDict[item]['rating'],reviewDict[item]['positive'],reviewDict[item]['negative'],reviewDict[item]['neutral'],reviewDict[item]['sentiment']))
        con.commit()
    except:
        con.rollback()

#print reviewDict
print ('done')

con.close()