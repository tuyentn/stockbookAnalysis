import sqlite3
import requests
import re
conn = sqlite3.connect('stockbook.db')

c = conn.cursor()

c.execute("SELECT * FROM post")
count = 0
for post in c.fetchall():
    count += 1
    id_post = post[0]
    try:
        r2 = requests.get('https://sb-api.vndirect.com.vn/api/posts/' + id_post)
        json_data2 = r2.json()
        print(json_data2)
        if(json_data2):
            standpoint = json_data2.get('standpoint')
            data_standpoint = ''
            if standpoint == 'up':
                data_standpoint = 1
            elif standpoint == 'down':
                data_standpoint = 0
            # print(id_post)
            if(standpoint):
                sql_query = "UPDATE post SET standpoint = '"+ str(data_standpoint) +"' WHERE postId='" + str(id_post) + "'"
                c.execute(sql_query)
    except:
        print('loi roi' + id_post)
conn.commit()
conn.close()