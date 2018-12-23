# coding=utf-8

import mysql.connector
import csv



con = mysql.connector.connect(database="yelp",user="root", host= "localhost", password="admin123");

cursor = con.cursor()


attribDict = dict()

with open('attribute.csv', encoding='utf8') as csvfile:
    attrib_reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in attrib_reader:
        if i==0:
            i=1
            continue
        if row[1] not in attribDict:
            attribDict[row[1]]= {}
            attribDict[row[1]][row[2]] = row[3]
        else:
            attribDict[row[1]][row[2]] = row[3]


for item in attribDict:
    cursor.execute("""INSERT INTO attributes VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (item, attribDict[item].get("GoodForMeal", "null"), attribDict[item].get("Alcohol","null"),attribDict[item].get("RestaurantsGoodForGroups","null"),attribDict[item].get("NoiseLevel","null"),attribDict[item].get("WiFi","null"), \
                                                                                               attribDict[item].get("RestaurantsReservations","null"),attribDict[item].get("BusinessAcceptsCreditCards","null"),attribDict[item].get("RestaurantsPriceRange2","null"), attribDict[item].get("RestaurantsDelivery","null"), \
                                                                                               attribDict[item].get("RestaurantsTakeOut","null"), attribDict[item].get("BusinessParking","null")))
    con.commit()




print ('done')

con.close()