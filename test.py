### 2. 파이썬에서 사용하는 방법
## 데이터베이스 접속

import sqlite3

conn = sqlite3.connect('./test.db')
'''
conn = sqlite3.connect(':memory:')    # 메모리 DB 접속(일회성)
'''


## with 문 이용
# import sqlite3
# conn = sqlite3.connect('./test.db')
#
# with conn:
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM test_table')
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)


### 3. Data Definition Language(DDL)
## 테이블 생성
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Eagles \
    (backNo INT NOT NULL, \
     name TEXT, \
     position TEXT, \
     hands TEXT, \
     height INT, \
     weight INT, \
     PRIMARY KEY(backNo));')

## 테이블 변경
cur.execute('ALTER TABLE Eagles ADD COLUMN birth INTEGER')


## 데이블 삭제
cur.execute('DROP TABLE Eagles')




### 4. 데이터 조작 언어(Data Manipulation Language, DML)
## 데이터 삽입
# 기본 스트링 쿼리
cur = conn.cursor()
cur.execute("INSERT INTO Eagles VALUES(8, '정근우', '외야수', '우투우타', 172, 75);")
cur.execute("INSERT INTO Eagles VALUES(57, '정우람', '투수', '좌투좌타', 181, 82), \
                                      (99, '류현진', '투수', '좌투우타', 190, 115);")
conn.commit()     # 변경사항 저장


# 파일에서 읽어서 데이터베이스에 쓰기
import pandas as pd
players = pd.read_csv('Resource/players.csv', encoding = 'EUC-KR')

cur = conn.cursor()
sql = 'INSERT INTO Eagles VALUES (?, ?, ?, ?, ?, ?);'
for i in range(10):
    cur.execute(sql, (int(players.iloc[i, 0]),
                      players.iloc[i, 1],
                      players.iloc[i, 2],
                      players.iloc[i, 3],
                      int(players.iloc[i, 4]),
                      int(players.iloc[i, 5])))
conn.commit()
conn.close()


# 파라메터: 튜플 사용
backNo = 50
name = '이성열'
position = '외야수'
hands = '좌투좌타'
height = 185
weight = 102
cur = conn.cursor()
sql = 'INSERT INTO Eagles VALUES (?, ?, ?, ?, ?, ?);'
cur.execute(sql, (backNo, name, position, hands, height, weight))
conn.commit()


# 튜플 리스트 사용
players = ((22, '이태양', '투수', '우투우타', 192, 97), (12, '김창혁', '포수', '우투우타', 179, 79))
cur = conn.cursor()
sql = 'INSERT INTO Eagles VALUES (?, ?, ?, ?, ?, ?);'
cur.executemany(sql, players)
conn.commit()



## 데이터 조회
# 순회 조회
cur = conn.cursor()
cur.execute('SELECT * FROM Eagles')
for row in cur:
    print(row)


# 단건 조회
cur = conn.cursor()
cur.execute('SELECT * FROM Eagles')
row = cur.fetchone()
print(row)

# 다건 조회
rows = cur.fetchmany(2)


# 모두 조회
rows = cur.fetchall()
for row in rows:
    print(row)


# 필요한 column만 조회
cur = conn.cursor()
cur.execute('SELECT name FROM Eagles WHERE backNo > 10')
rows = cur.fetchall();
for row in rows:
    print(row)


# 원하는 순서 및 갯수
cur.execute('SELECT * FROM Eagles ORDER BY name')
cur.execute('SELECT * FROM Eagles ORDER BY name DESC')
cur.execute('SELECT * FROM Eagles ORDER BY name DESC LIMIT 1')
row = cur.fetchone()
print(row[1])          # '호잉'



# 집계 함수
cur.execute('SELECT count(*) FROM Eagles')
count = cur.fetchone()

max(height), min(height), sum(height), avg(height)



## 데이터 검색

# 기본 스트링 쿼리
cur = conn.cursor()
cur.execute("SELECT * FROM Eagles WHERE position='내야수';")
rows = cur.fetchall();
for row in rows:
    print(row)


# Placeholder
cur = conn.cursor()
backNo = 50
cur.execute('SELECT * FROM Eagles WHERE backNo=?;', (backNo,))
player = cur.fetchone()
print(player[0])            # 50


# Grouping
sql = 'SELECT position, count(*) FROM Eagles GROUP BY position'



## 데이터 변경
position = '외야수'
back_no = 8
cur.execute('UPDATE Eagles SET position=? WHERE backNo=?;',
            (position, backNo))
cur.execute('SELECT * FROM Eagles WHERE backNo=?‘, (backNo,))
cur.fetchone()
data = ((1995,1), (1986,57))
sql = 'UPDATE Eagles SET position=? WHERE backNo=?'
cur.executedmany(sql, data)



## 데이터 삭제
cur = conn.cursor()
cur.execute('DELETE FROM Eagles WHERE backNo=1);')