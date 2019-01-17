import csv
import sqlite3
import os
import logging
from pandas import read_csv, Series, DataFrame
from numpy import array, savetxt, matrix, vstack, average, nan
import datetime

priceData = read_csv('price.csv')
dateArr = priceData['date']
codeArr = priceData['code']
openArr = priceData['open']
closeArr = priceData['close']
ema10Arr = priceData['EMA10']
ema50Arr = priceData['EMA50']
ema200Arr = priceData['EMA200']

nickname = []
#duDoan10 = []
#duDoan50 = []
#duDoan200 = []
doanDung = []
tongDuDoan = []

conn = sqlite3.connect('stockbook.db')
c = conn.cursor()


query = "select post.createdBy ,PC.namecode, strftime('%Y%m%d',datetime(post.createdUnixTime/1000, 'unixepoch')) , post.standpoint from post left join (select post_code.id_post, code.namecode from post_code inner join code on post_code.id_code = code.id ) PC on PC.id_post = post.postId where post.standpoint <> 'None' and PC.namecode is not null"
#print(query)
results = c.execute(query)
for row in results:
    print(row)
    
    filePath = 'data/excel_'+str(row[1])+'_ok.csv'
    try:
        priceData = read_csv(filePath)
    except IOError:
        logging.exception('K mo duoc file')
    dateArr = priceData['ymd']
    openArr = priceData['open']
    closeArr = priceData['close']
    ema10Arr = priceData['ema10']
    ema50Arr = priceData['ema50']
    ema200Arr = priceData['ema200']
    dateForLoop = datetime.datetime.strptime(row[2], '%Y%m%d')
    tim_thay = None
    loop = 5
    open = 0
    while ((not tim_thay) and (loop>0)):
        for i in range(len(dateArr)):
            if(str(dateArr[i])==(dateForLoop.strftime('%Y%m%d')+'.0')):
                open = str(openArr[i])
                tim_thay = True
                break
        dateForLoop += datetime.timedelta(days=-1)
        loop -=1
    ################################
    after10days = datetime.datetime.strptime(row[2], '%Y%m%d') + datetime.timedelta(days=12)
    tim_thay = None
    loop = 7
    ema10 = 0
    while ((not tim_thay) and (loop>0)):
        for i in range(len(dateArr)):
            if(str(dateArr[i])==(after10days.strftime('%Y%m%d')+'.0')):
                ema10 = str(ema10Arr[i])
                tim_thay = True
                break
        after10days += datetime.timedelta(days=-1)
        loop -=1
    ################################
    after50days = datetime.datetime.strptime(row[2], '%Y%m%d') + datetime.timedelta(days=52)
    tim_thay = None
    loop = 10
    ema50 = 0
    while ((not tim_thay) and (loop>0)):
        for i in range(len(dateArr)):
            if(str(dateArr[i])==(after50days.strftime('%Y%m%d')+'.0')):
                ema50 = str(ema50Arr[i])
                tim_thay = True
                break
        after50days += datetime.timedelta(days=-1)
        loop -=1
    ################################
    after200days = datetime.datetime.strptime(row[2], '%Y%m%d') + datetime.timedelta(days=200)
    tim_thay = None
    loop = 10
    ema200 = 0
    while ((not tim_thay) and (loop>0)):
        for i in range(len(dateArr)):
            if(str(dateArr[i])==(after200days.strftime('%Y%m%d')+'.0')):
                ema200 = str(ema200Arr[i])
                tim_thay = True
                break
        after200days += datetime.timedelta(days=-1)
        loop -=1

    if (row[0] in nickname):
        index = nickname.index(row[0])
        tongDuDoan[index] +=1
        if (float(ema10) >= float(open)*1.03 or float(ema50) >= float(open)*1.07 or float(ema200) >= float(open)*1.15):
            doanDung[index] +=1
        #if float(ema10) >= float(open)*1.05:
        #    duDoan10[index] +=1
        #if float(ema50) >= float(open)*1.12:
        #    duDoan50[index] +=1
        #if float(ema200) >= float(open)*1.2:
        #    duDoan200[index] +=1
    else:
        nickname.append(row[0])
        tongDuDoan.append(1)
        if (float(ema10) >= float(open)*1.03 or float(ema50) >= float(open)*1.07 or float(ema200) >= float(open)*1.15):
            doanDung.append(1)
        else:
            doanDung.append(0)
        #if float(ema10) >= float(open)*1.05:
        #    duDoan10.append(1)
        #else:
        #    duDoan10.append(0)
        #if float(ema50) >= float(open)*1.12:
        #    duDoan50.append(1)
        #else:
        #    duDoan50.append(0)
        #if float(ema200) >= float(open)*1.2:
        #    duDoan200.append(1)
        #else:
            #duDoan200.append(0)


conn.close()
print(nickname)
#print(duDoan10)
#print(duDoan50)
#print(duDoan200)
print(doanDung)
print(tongDuDoan)

matran = [nickname,doanDung,tongDuDoan]
matran2 = list(map(list, zip(*matran)))
header = ["nickname", "doanDung", "tongDuDoan"]
df = DataFrame(matran2, columns = header)
df.to_csv('SamSoi.csv')

