### 연습문제 2
### 다음의 지시대로 DB 테이블을 만들고 이를 조회하는 프로그램을 만드시오.

import sqlite3
import pandas as pd
import numpy as np

## 2-1
## 국내의 대표적인 걸그룹 또는 보이그룹 5개 이상에 대하여
## 다음과 같은 정보를 갖는 테이블을 만드시오.
## *는 Primary Key
## id(*), group_name, 구성원 수, 데뷔일자, 소속사


# 데이터베이스 접속
conn = sqlite3.connect('Idols/Idols.db')
'''
conn = sqlite3.connect(':memory:')     # 메모리 DB 접속(일회성)
'''
conn.close()

# Idols 테이블 생성
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Idols \
            (id INT NOT NULL, \
            group_name TEXT, \
            members INT, \
            debut INT, \
            company TEXT, \
            PRIMARY KEY(id));')

# 데이터 삽입
idols = pd.read_csv('Data/idols.csv', encoding = 'EUC-KR')
idols

cur = conn.cursor()
sql = 'INSERT INTO Idols VALUES (?, ?, ?, ?, ?);'
for i in range(12):
    cur.execute(sql, (int(idols.iloc[i, 0]),
                      idols.iloc[i, 1],
                      int(idols.iloc[i, 2]),
                      int(idols.iloc[i, 3]),
                      idols.iloc[i, 4]))
conn.commit()

# Idols table 검색하기
cur = conn.cursor()
cur.execute("SELECT * FROM Idols")
rows = cur.fetchall()
for row in rows:
    print(row)



## 2-2
## 이들이 불렀던 노래 또는 다른 사람이 불렀던 노래 10곡 이상에 대하여
## 다음의 정보를 갖는 테이블을 만드시오.
## song_id(*), song_name, 그룹 id, 발표년도, 작곡가, 도입부 가사

# Songs 테이블 생성
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Songs \
            (id INT NOT NULL, \
            song_name TEXT, \
            group_id INT, \
            year INT, \
            songwrite TEXT, \
            iyrics TEXT, \
            PRIMARY KEY(id));')

# 데이터 삽입
songs = pd.read_csv('Data/songs.csv', encoding = 'EUC-KR')
songs

cur = conn.cursor()
sql = "INSERT INTO Songs VALUES (?,?,?,?,?,?);"
for i in range(19):
    cur.execute(sql, (i + 101,
                      songs.iloc[i, 0],
                      int(songs.iloc[i, 1]),
                      int(songs.iloc[i, 2]),
                      songs.iloc[i, 3],
                      songs.iloc[i, 4]))
conn.commit()

# Songs Table 검색하기
cur = conn.cursor()
cur.execute("SELECT * FROM Songs")
rows = cur.fetchall()
for row in rows:
    print(row)



## 2-3
## 위 두개의 테이블을 조인한 결과를 가지고 다음의 필드를 갖는 데이터 프레임을 만드시오.
## 그룹 이름, 구성원 수, 데뷔 일자, 노래 이름, 발표 년도

# Idols Table에 INNER JOIN 하기
sql = "SELECT i.group_name, i.members, i.debut, \
       s.song_name, s.year \
       FROM Idols AS i INNER JOIN Songs AS s \
       ON i.id = s.group_id;"
cur = conn.cursor()
cur.execute(sql)
rows = cur.fetchall();
columnName = ['그룹이름', '구성원수', '데뷔일자', '노래이름', '발표년도']
idols_df = pd.DataFrame(columns = columnName)
for row in rows:
    idols_df = idols_df.append(pd.DataFrame([list(row)], columns = columnName),
                               ignore_index = True)
idols_df

# Idols Table에 LEFT OUTER JOIN 하기
sql = "SELECT i.group_name, i.members, i.debut, \
       s.song_name, s.year \
       FROM Idols AS i LEFT OUTER JOIN Songs AS s \
       ON i.id = s.group_id;"
cur = conn.cursor()
cur.execute(sql)
rows = cur.fetchall();
columnName = ['그룹이름', '구성원수', '데뷔일자', '노래이름', '발표년도']
idols_df = pd.DataFrame(columns = columnName)
for row in rows:
    idols_df = idols_df.append(pd.DataFrame([list(row)], columns = columnName),
                               ignore_index = True)
idols_df

# Idols Table에 JOIN 하고 노래발표년도 오름차순
sql = "SELECT i.group_name, i.members, i.debut, \
       s.song_name, s.year \
       FROM Idols AS i JOIN Songs AS s \
       ON i.id = s.group_id ORDER BY s.year;"
cur = conn.cursor()
cur.execute(sql)
rows = cur.fetchall();
columnName = ['그룹이름', '구성원수', '데뷔일자', '노래이름', '발표년도']
idols_df = pd.DataFrame(columns = columnName)
for row in rows:
    idols_df = idols_df.append(pd.DataFrame([list(row)], columns = columnName),
                               ignore_index = True)
idols_df