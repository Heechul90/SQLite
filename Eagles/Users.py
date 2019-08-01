### 연습문제 3

import sqlite3
import pandas as pd
import numpy as np

## 사용자의 이름과, 비밀번호를 갖는 Users 테이블이 있다.
## 사용자의 이름과 비밀번호를 올바르게 입력하면 ‘성공’을 출력하고,
## 잘못 입력하면 ‘실패’를 출력하는 프로그램을 작성하시오.

# 데이터베이스 접속하기
conn = sqlite3.connect('Eagles/Eagles.db')
'''
conn = sqlite3.connect(':memory:')     # 메모리 DB 접속(일회성)
'''

# Users 테이블 만들기
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Users \
    (uid TEXT PRIMARY KEY, \
     name TEXT NOT NULL, \
     password TEXT);')

# 데이터 삽입하기
users = pd.DataFrame({
    'uid': ['jhchoi','tkkim','kmsong','sylee','ewchung'],
    'name': ['최진행','김태균','송광민','이성열','정은원'],
    'password': ['1234','1234','1234','1234','1234']})
users

cur = conn.cursor()
sql = 'INSERT INTO Users VALUES (?, ?, ?);'
for i in range(5):
    cur.execute(sql, (users.iloc[i,0],
                      users.iloc[i,1],
                      users.iloc[i,2]))
conn.commit()

# 데이터 검색하기
cur = conn.cursor()
cur.execute("SELECT * FROM Users;")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()

# 이름, 패스워드 가져오는 함수 만들기
def checkUser(uid, password):
    print(uid, password)
    conn = sqlite3.connect('Eagles/Eagles.db')
    cur = conn.cursor()
    sql = "SELECT name, password FROM Users WHERE uid like ?;"
    cur.execute(sql, (uid,))
    dbname, dbpassword = cur.fetchone()
    print(dbname, dbpassword)
    conn.close()

# uid, password 입력창 만들기
uid, password = input('uid password 입력하시오.: ').split()
checkUser(uid, password)

# Exception 함수 만들기

CHECK_SUCCESS = 0
INVALID_UID = 1
INCORRECT_PASSWORD = 2
DATABASE_ERROR = 3

def checkUser(uid, password):
    conn = sqlite3.connect('Eagles/Eagles.db')
    name = ''
    try:
        cur = conn.cursor()
        sql = "SELECT name, password FROM Users WHERE uid like ?;"
        cur.execute(sql, (uid,))
        dbName, dbPassword = cur.fetchone()
        if password == dbPassword:
            returnCode = CHECK_SUCCESS
            name = dbName
        else:
            returnCode = INCORRECT_PASSWORD
    except TypeError as te:
        returnCode = INVALID_UID
    except Exception as e:
        print('예외가 발생했습니다.', e)
        returnCode = DATABASE_ERROR
    finally:
        conn.close()
        return returnCode, name

# uid, password 입력창 만들기
uid, password = input("uid password 입력> ").split()
result, name = checkUser(uid, password)
if result == CHECK_SUCCESS:
    print('로그인 성공, 사용자 이름 =', name)
elif result == INVALID_UID:
    print('실패 - 잘못된 User ID')
elif result == INCORRECT_PASSWORD:
    print('실패 - 패스워드 불일치')
else:
    print('실패 - 데이터베이스 에러')