import sqlite3
import re
conn = sqlite3.connect('stockbook.db')

c = conn.cursor()

c.execute("SELECT * FROM post")

for post in c.fetchall():
    content = post[1]
    id_post = post[0]
    match = re.findall('(?<=\$)\w+', content)
    for code in match:
        code = code.upper()
        if(code.__len__() == 3):
            c.execute("SELECT * FROM code WHERE namecode='" + code + "'")
            check = c.fetchone()
            exist = str(check)
            if(exist == 'None'):

                sql_code = "INSERT INTO code(namecode) VALUES ('" + code + "')"
                try:
                    c.execute(sql_code)
                    id_code = c.lastrowid
                except:
                    print('loi roi, loi insert code')
            else:
                id_code = check[0]

            c.execute("SELECT * FROM post_code WHERE id_post='" + id_post + "' AND id_code='" + str(id_code) + "'")
            exist = str(c.fetchone())
            if (exist == 'None'):
                sql_post_code = "INSERT INTO post_code(id_post, id_code) VALUES ('" + id_post + "','" + str(id_code) + "')"
                try:
                    c.execute(sql_post_code)
                except:
                    print('loi roi, loi insert post_code')
            else:
                print('da ton tai row in post_code')
conn.commit()
conn.close()