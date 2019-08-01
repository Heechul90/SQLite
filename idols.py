### idols





# 데이터베이스 접속
import sqlite3

conn = sqlite3.connect('./test.db')
'''
conn = sqlite3.connect(':memory:')     # 메모리 DB 접속(일회성)
'''

# Pitcher_stats 테이블 생성
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Idols \
            (id INT NOT NULL, \
            group_name TEXT, \
            mombers INT, \
            debut INT, \
            company TEXT, \
            PRIMARY KEY(id));')


# 데이터 삽입

import pandas as pd
idols = pd.read_csv('Resource/idols.csv', encoding = 'EUC-KR')
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


idols.iloc[0, 0]