### Pitcher_stats


## 투수들의 기록중에서 평균자책점(ERA), 투구인닝(IP), 탈삼진(SO) 기록을 찾아서
## Pitcher_stats 란 테이블을 만들고,
## Eagles 테이블과 Join 하여
## 백넘버, 선수명, 포지션, 투구인닝, 평균자책점, 탈삼진 필드를 갖는
## 데이터 프레임을 만들어서 Join 한 결과를 입력하고, 그 결과를 보이시오.

# 데이터베이스 접속
import sqlite3

conn = sqlite3.connect('./test.db')
'''
conn = sqlite3.connect(':memory:')     # 메모리 DB 접속(일회성)
'''

# Pitcher_stats 테이블 생성
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Pitcher_stats \
            (backNo INT NOT NULL, \
            name TEXT, \
            position TEXT, \
            IP INT, \
            ERA INT, \
            SO INT, \
            PRIMARY KEY(backNo));')

# 데이터 삽입
cur = conn.cursor()
cur.execute("INSERT INTO Pitcher_stats VALUES(111, '이희철', '투수', 201, 0.33, 314);")
conn.commit()


import pandas as pd
pitchers = pd.read_csv('Resource/pitchers.csv', encoding = 'EUC-KR')
pitchers

cur = conn.cursor()
sql = 'INSERT INTO Pitcher_stats VALUES (?, ?, ?, ?, ?, ?);'
for i in range(25):
    cur.execute(sql, (int(pitchers.iloc[i, 0]),
                      pitchers.iloc[i, 1],
                      pitchers.iloc[i, 2],
                      int(pitchers.iloc[i, 3]),
                      int(pitchers.iloc[i, 4]),
                      int(pitchers.iloc[i, 5])))
conn.commit()


