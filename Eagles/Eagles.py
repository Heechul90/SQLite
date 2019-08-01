### Eagles

import sqlite3
import pandas as pd
import numpy as np

### 2. 파이썬에서 사용하는 방법
## 데이터베이스 접속

conn = sqlite3.connect('Eagles/Eagles.db')
'''
conn = sqlite3.connect(':memory:')    # 메모리 DB 접속(일회성)
'''

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
players = pd.read_csv('Data/players.csv', encoding = 'EUC-KR')

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
cur = conn.cursor()
rows = cur.fetchmany(2)
for row in rows:
    print(row)

# 모두 조회#############################################
cur = conn.cursor()
rows = cur.fetchall()
for row in rows:
    print(row)

# 필요한 column만 조회
cur = conn.cursor()
cur.execute('SELECT name FROM Eagles WHERE height > 185')
rows = cur.fetchall();
for row in rows:
    print(row)

# 조회 조건
cur = conn.cursor()
cur.execute("SELECT *FROM Eagles WHERE position like '내야수'")
rows = cur.fetchall();
for row in rows:
    print(row)

# 원하는 순서 및 갯수
# 이름으로 내림차순 정렬하기
cur = conn.cursor()
cur.execute('SELECT * FROM Eagles ORDER BY name')       # 이름으로 정렬
rows = cur.fetchall();
for row in rows:
    print(row)

# 이름으로 오름차순 정렬하기
cur = conn.cursor()
cur.execute('SELECT * FROM Eagles ORDER BY name DESC')  # 반대로 정렬
rows = cur.fetchall();
for row in rows:
    print(row)

# 이름으로 오름차순 정렬하고 5개까지 출력하기
cur = conn.cursor()
cur.execute('SELECT * FROM Eagles ORDER BY name DESC LIMIT 5')
rows = cur.fetchall();
for row in rows:
    print(row)

# 집계 함수
cur = conn.cursor()
cur.execute('SELECT count(*) FROM Eagles')
count = cur.fetchone()
print(count)

# 그룹핑, 집계함수
# 포지션별로 갯수를 세고 키의 평균을 출력
cur = conn.cursor()
cur.execute("SELECT position, count(*), avg(height) FROM Eagles GROUP BY position")
rows = cur.fetchall();
for row in rows:
    print(row)

# Placeholder를 사용해서 데이터 검색
cur = conn.cursor()
backNo = 50
cur.execute("SELECT * FROM Eagles WHERE backNo=?;", (backNo,))
player = cur.fetchone()
print(player)



## 데이터 변경
## UPDATE table SET field1 = value1, ... WHERE 조건;
cur = conn.cursor()
cur.execute("UPDATE Eagles SET hands = '우투좌타', height = 193, \
                               weight = 110 WHERE backNo = 104;")
conn.commit()



## 데이터 삭제
## DELETE FROM table WHERE 조건;
cur = conn.cursor()
cur.execute("DELETE FROM Eagles WHERE backNo = 104;")
conn.commit()




### 5. Table Join
## 테이블 생성
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Stats \
                (id INT NOT NULL, \
                 player TEXT, \
                 average REAL, \
                 rbi INT, \
                 homerun INT, \
                 PRIMARY KEY(id));")

## 데이터 삽입
stats = pd.read_csv('Data/stats.csv', encoding = 'EUC-KR')
stats

cur = conn.cursor()
sql = 'INSERT INTO Stats VALUES (?,?,?,?,?); '
for i in range(9):
    cur.execute(sql, (i + 1,
                      stats.iloc[i, 0],
                      float(stats.iloc[i, 1]),
                      int(stats.iloc[i, 2]),
                      int(stats.iloc[i, 3])))
conn.commit()

## 데이터 검색하기
cur = conn.cursor()
cur.execute("SELECT * FROM Stats")
for row in cur:
    print(row)

## Eagle로 JOIN하기
sql = "SELECT Eagles.backNo, Eagles.name, Eagles.position, \
       Stats.average, Stats.rbi, Stats.homerun \
       FROM Eagles JOIN Stats \
       ON Eagles.name like Stats.player;"
cur = conn.cursor()
cur.execute(sql)
for row in cur:
    print(row)

sql = "SELECT e.backNo, e.name, e.position, \
       s.average, s.rbi, s.homerun \
       FROM Eagles AS e JOIN Stats AS s \
       ON e.name like s.player;"
cur = conn.cursor()
cur.execute(sql)
rows = cur.fetchall();
columnName = ['등번호', '선수명', '포지션', '타율', '타점', '홈런']
eagles_df = pd.DataFrame(columns = columnName)
for row in rows:
    eagles_df = eagles_df.append(pd.DataFrame([list(row)], columns = columnName),
                                 ignore_index = True)
eagles_df

conn.close()