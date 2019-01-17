import csv
import sqlite3
import os
from pandas import read_csv, Series
from numpy import array, savetxt, matrix, vstack, average, nan


conn = sqlite3.connect('stockbook.db')
c = conn.cursor()

for _file in os.listdir('data'):
    duLieu = read_csv('data/'+_file)
    tenMa = _file[6:-7]
    print(tenMa)
    inputs = {
        'date': duLieu['ymd'],
        'open': duLieu['open'],
        'close': duLieu['close'],
        'volume': duLieu['volume'],
        'EMA10': duLieu['ema10'],
        'EMA50': duLieu['ema50'],
        'EMA200': duLieu['ema200']
    }
    date = inputs['date']
    open = inputs['open']
    close = inputs['close']
    volume = inputs['volume']
    EMA10 = inputs['EMA10']
    EMA50 = inputs['EMA50']
    EMA200 = inputs['EMA200']
    for i in list(range(339)):
        query = "INSERT INTO price(date, code, open, close, volume, EMA10, EMA50, EMA200) VALUES ("+str(date[i])+",'"+str(tenMa)+"', '"+str(open[i])+"', '"+str(close[i])+"', '"+str(volume[i])+"', '"+str(EMA10[i])+"', '"+str(EMA50[i])+"', '"+str(EMA200[i])+"');"
        print(query)
        c.execute(query)
conn.close()



