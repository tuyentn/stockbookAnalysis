import sqlite3

conn = sqlite3.connect('stockbook.db')

c = conn.cursor()
# c.execute('''CREATE TABLE code
#              (id INTEGER PRIMARY KEY, namecode text)''')
# c.execute('''CREATE TABLE post_code
#              (id_post text, id_code INTEGER)''')
# c.execute('''CREATE TABLE comment_code
#              (id_comment INTEGER, id_code INTEGER)''')

# them truong du tang du giam
c.execute('''ALTER TABLE post ADD COLUMN standpoint INT''')

conn.commit()
conn.close()