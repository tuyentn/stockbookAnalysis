import timeit
import requests
import sqlite3
import re

start = timeit.default_timer()

conn = sqlite3.connect('stockbook.db')

c = conn.cursor()
headers = {'authorization': 'lD00Fu3bbIq2vz5xltdaKqDYtXjWnvzs',
           'user-aget': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
           }
def insertUser(nickname):
    c.execute("SELECT * FROM user WHERE nickname='" + nickname + "'")
    exist = str(c.fetchone())
    if (exist == 'None'):
        req = requests.get('https://sb-api.vndirect.com.vn/api/users/' + nickname + '/info?api_version=2.0&nickname=' + nickname, headers=headers)
        data_user = req.json()['additionalData']['userData']
        nickname = str(data_user.get('nickname'))
        fullname = str(data_user.get('fullname'))
        email = str(data_user.get('email'))
        gender = str(data_user.get('gender'))
        homeTown = str(data_user.get('homeTown'))
        likeCount = str(data_user.get('likeCount', 0))
        if (likeCount == 'None'):
            likeCount = '0'
        followingCount = str(data_user.get('followingCount', 0))
        followerCount = str(data_user.get('followerCount', 0))
        postCount = str(data_user.get('postCount', 0))
        if (postCount == 'None'):
            postCount = '0'
        investmentPerspective = str(data_user.get('investmentPerspective')).replace("'"," ")
        verifiedStatus = str(data_user.get('verifiedStatus'))
        if (verifiedStatus == 'True'):
            verifiedStatus = '1'
        else:
            verifiedStatus = '0'
        registeredTime = str(data_user.get('registeredTime'))

        sql_user = "INSERT INTO user VALUES ('" + nickname + "', '" + fullname + "', '" + email + "', '" + gender + "', '" + homeTown + "', " + likeCount + ", " + followingCount + ", " + followerCount + ", " + postCount + ", '" + investmentPerspective + "', " + verifiedStatus + ", '" + registeredTime + "')"
        try:
            c.execute(sql_user)
        except:
            print('loi roi, loi insert user')

    return nickname

def crawlpage(number_page):
    # r2 = requests.get('https://sb-api.vndirect.com.vn/api/feeds/new/community?page_index='+ str(number_page) +'&api_version=2.0', headers=headers)
    r2 = requests.get('https://sb-api.vndirect.com.vn/api/feeds/new/community?api_version=2.0&page_index='+ str(number_page), headers=headers)

    json_data2 = r2.json()
    print(json_data2.get('feeds'))
    items = list(json_data2.get('feeds'))

    for post in list(items):
        first = post
        created_by = str(first.get('createdBy'))

        if(created_by != 'None'):
            insertUser(created_by)
            postId = str(first.get("postId"))
            content = str(first.get("content")).replace("'"," ")
            posterIsVerify = str(first.get("posterIsVerify"))
            if (posterIsVerify == 'True'):
                posterIsVerify = '1'
            else:
                posterIsVerify = '0'

            numOfComments = str(first.get("numOfComments", 0))
            likeCounts = str(first.get("likeCounts", 0))
            viewCounts = str(first.get("viewCounts", 0))
            createdUnixTime = str(first.get("createdUnixTime"))
            lastUpdated = str(first.get("lastUpdated"))
            #standpoint
            standpoint = json_data2.get('standpoint')
            data_standpoint = ''
            if standpoint == 'up':
                data_standpoint = 1
            elif standpoint == 'down':
                data_standpoint = 0

            sql_post = "INSERT INTO post VALUES ('" + postId + "', '" + content + "', '" + posterIsVerify + "', " + numOfComments + ", " + likeCounts + ", " + viewCounts + ", '" + createdUnixTime + "', '" + lastUpdated + "', '" + created_by + "', '" + data_standpoint + "')"
            # print(sql_post)
            try:
                c.execute("SELECT * FROM post WHERE postId='" + postId + "'")
                exist = str(c.fetchone())
                if (exist == 'None'):
                    c.execute(sql_post)
                else:
                    print("ton tai roi")
            except:
                print('loi roi, loi insert post')

            #likes
            userslike = first.get("usersLike")
            if(userslike != None):
                list_like = [(postId, str(key), str(value)) for key, value in userslike.items()]
                for key, value in userslike.items():
                    insertUser(key)
                try:
                    c.executemany('INSERT INTO likes (postId,nickname,time) VALUES (?,?,?)', list_like)
                except:
                    print('da like')

            #comments
            try:
                r4 = requests.get('https://sb-api.vndirect.com.vn/api/posts/' + postId + '/comments')
                data_comments = r4.json()

                for comment in data_comments:
                    insertUser(comment.get('createdBy'))
                list_comment = [(str(i.get("content")), str(i.get("createdAt")), 1, 0, str(i.get("postId")), str(i.get("createdBy"))) for i in data_comments]

                c.executemany('INSERT INTO comment (content,createdAt,commenterIsVerify,likeCounts,postId,createdBy) VALUES (?,?,?,?,?,?)', list_comment)
            except:
                print('loi roi, loi insert comment')

            # code_post
            content = str(first.get("content")).replace("'"," ")
            id_post = postId
            match = re.findall('(?<=\$)\w+', content)
            for code in match:
                code = code.upper()
                if (code.__len__() == 3):
                    c.execute("SELECT * FROM code WHERE namecode='" + code + "'")
                    check = c.fetchone()
                    exist = str(check)
                    if (exist == 'None'):

                        sql_code = "INSERT INTO code(namecode) VALUES ('" + code + "')"
                        try:
                            c.execute(sql_code)
                            id_code = c.lastrowid
                        except:
                            print('loi roi, loi insert code')
                    else:
                        id_code = check[0]

                    c.execute(
                        "SELECT * FROM post_code WHERE id_post='" + id_post + "' AND id_code='" + str(id_code) + "'")
                    exist = str(c.fetchone())
                    if (exist == 'None'):
                        sql_post_code = "INSERT INTO post_code(id_post, id_code) VALUES ('" + id_post + "','" + str(
                            id_code) + "')"
                        try:
                            c.execute(sql_post_code)
                        except:
                            print('loi roi, loi insert post_code')
                    else:
                        print('da ton tai row in post_code')

for i in range(500):
    crawlpage(i+1)
conn.commit()
conn.close()

stop = timeit.default_timer()
print('Success, time: ')
print(stop - start)
