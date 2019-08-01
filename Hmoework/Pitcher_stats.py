### 연습문제 1
### 다음의 지시대로 DB 테이블을 만들고 이를 조회하는 프로그램을 만드시오.

import sqlite3
import pandas as pd
import numpy as np

## 투수들의 기록중에서 평균자책점(ERA), 투구인닝(IP), 탈삼진(SO) 기록을 찾아서
## Pitcher_stats 란 테이블을 만들고,

# 데이터베이스 접속

conn = sqlite3.connect('Eagles/Eagles.db')
'''
conn = sqlite3.connect(':memory:')     # 메모리 DB 접속(일회성)
'''

# Pitcher_stats 테이블 생성
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Pitcher_stats \
            (id INT NOT NULL, \
            name TEXT, \
            position TEXT, \
            IP REAL, \
            ERA REAL, \
            SO INT, \
            PRIMARY KEY(id));')

# 데이터 삽입
pitchers = pd.read_csv('Data/pitchers.csv', encoding = 'EUC-KR')
pitchers

cur = conn.cursor()
sql = 'INSERT INTO Pitcher_stats VALUES (?, ?, ?, ?, ?, ?);'
for i in range(25):
    cur.execute(sql, (i + 1,
                      pitchers.iloc[i, 0],
                      pitchers.iloc[i, 1],
                      float(pitchers.iloc[i, 2]),
                      float(pitchers.iloc[i, 3]),
                      int(pitchers.iloc[i, 4])))
conn.commit()

## Eagles 테이블과 Join 하여
## 백넘버, 선수명, 포지션, 투구인닝, 평균자책점, 탈삼진 필드를 갖는
## 데이터 프레임을 만들어서 Join 한 결과를 입력하고, 그 결과를 보이시오.
sql = "SELECT e.backNo, e.name, e.position, \
       p.IP, p.ERA, p.SO \
       FROM Eagles AS e JOIN Pitcher_stats AS p \
       ON e.name like p.name;"
cur = conn.cursor()
cur.execute(sql)
rows = cur.fetchall();
columnName = ['백넘버', '선수명', '포지션', '투구이닝', '평균자책점', '탈삼진']
pitcher_df = pd.DataFrame(columns = columnName)
for row in rows:
    pitcher_df = pitcher_df.append(pd.DataFrame([list(row)], columns = columnName),
                                   ignore_index = True)
pitcher_df

conn.close()


