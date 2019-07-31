### 2. 파이썬에서 사용하는 방법
## 데이터베이스 접속

import sqlite3
conn = sqlite3.connect(':memory:') # 메모리 DB 접속(일회성) conn = sqlite3.connect(‘./test.db') # 파일 DB 접속(일회성)
. . .
데이터 쿼리 수행
. . .
conn.commit() # 변경사항 저장
conn.close()


## with 문 이용
import sqlite3
conn = sqlite3.connect('./test.db')

with conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM test_table')
    rows = cur.fetchall()
    for row in rows:
        print(row)


### 3. Data Definition Language(DDL)
## 테이블 생성
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Eagles
(backNo INT NOT NULL,
name TEXT,
position TEXT,
hands TEXT,
height TEXT,
weight TEXT,
PRIMARY KEY(backNo));'')


## 테이블 변경
cur.execute('ALTER TABLE Eagles ADD COLUMN birth INTEGER')


## 데이블 삭제
cur.execute('DROP TABLE Eagles')




### 4. 데이터 조작 언어(Data Manipulation Language, DML)
## 데이터 삽입
# 기본 스트링 쿼리
cur = conn.cursor()
cur.execute("INSERT INTO Eagles VALUES(8, '정근우', '외야수', 172, 75);")
cur.execute("INSERT INTO Eagles VALUES(57, '정우람', '투수', 181, 82), (99, '류현진', '투수', 190, 115);")


# 파라메터: 튜플 사용
back_no = 50
name = '이성열'
position = '외야수'
height = 185
weight = 102
cur = conn.cursor()
sql = 'INSERT INTO Eagles VALUES (?, ?, ?, ?, ?);'
cur.execute(sql, (back_no, name, position, height, weight))


# 튜플 리스트 사용
players = ((22, '이태양', '투수', 192, 97), (12, '김창혁', '포수', 179, 79))
cur = conn.cursor()
sql = 'INSERT INTO Eagles VALUES (?, ?, ?, ?, ?);'
cur.executemany(sql, players)



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


# 다건 조회
rows = cur.fetchmany(2)


# 모두 조회
rows = cur.fetchall()
for row in rows:
    print(row)


# 필요한 column만 조회
cur = conn.cursor()
cur.execute('SELECT name FROM Eagles WHERE back_no > 10')
rows = cur.fetchall();
for row in rows:
    print(row)


# 원하는 순서 및 갯수
cur.execute('SELECT * FROM Eagles ORDER BY name')
cur.execute('SELECT * FROM Eagles ORDER BY name DESC')
cur.execute('SELECT * FROM Eagles ORDER BY name DESC LIMIT 1')
row = cur.fetchone()
print(row[1]) # '하주석'



# 집계 함수
cur.execute('SELECT count(*) FROM Eagles')
count = cur.fetchone()

max(column), min(column), sum(column), avg(column)



## 데이터 검색

# 기본 스트링 쿼리
cur = conn.cursor()
cur.execute("SELECT * FROM Eagles WHERE position='내야수';") rows = cur.fetchall();
for row in rows:
    print(row)


# Placeholder
cur = con.cursor()
back_no = 50
cur.execute('SELECT * FROM Eagles WHERE back_no=?;', (back_no,))
player = cur.fetchone()
print(player[0])            # 50


# Grouping
sql = 'SELECT position, count(*) FROM Eagles GROUP BY position'



## 데이터 변경
position = '외야수'
back_no = 8
cur.execute('UPDATE Eagles SET position=? WHERE back_no=?;',
            (position, back_no))
cur.execute('SELECT * FROM Eagles WHERE back_no=?‘, (back_no,))
cur.fetchone()
data = ((1995,1), (1986,57))
sql = 'UPDATE Eagles SET position=? WHERE back_no=?'
cur.executedmany(sql, data)



## 데이터 삭제
cur = con.cursor() cur.execute('DELETE FROM Eagles WHERE back_no=1);')