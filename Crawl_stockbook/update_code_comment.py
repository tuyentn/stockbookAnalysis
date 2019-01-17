import sqlite3
import re
conn = sqlite3.connect('stockbook.db')

c = conn.cursor()

c.execute("SELECT * FROM comment")

for comment in c.fetchall():
    content = comment[1]
    id_comment = comment[0]
    match = re.findall('(?<=\$)\w+', content)
    for code in match:
        code = code.upper()
        if (code.__len__() == 3):
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

            c.execute("SELECT * FROM comment_code WHERE id_comment='" + str(id_comment) + "' AND id_code='" + str(id_code) + "'")
            exist = str(c.fetchone())
            if (exist == 'None'):
                sql_comment_code = "INSERT INTO comment_code(id_comment, id_code) VALUES ('" + str(id_comment) + "','" + str(id_code) + "')"
                try:
                    c.execute(sql_comment_code)
                except:
                    print('loi roi, loi insert comment_code')
            else:
                print('da ton tai row in comment_code')
conn.commit()
conn.close()