# 월별 상위 최다 당첨번호 6개 시각화

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# 그래프의 한글 깨짐 방지(한글 폰트 설정)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='pydb')

sql = "select * from lotto_tbl"

cur = dbConn.cursor()
cur.execute(sql)

rows = cur.fetchall()  # 테이블에서 모두 가져오기

lotto_df = pd.DataFrame(rows, columns=['count', 'date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus'])
# print(lotto_df)

# print(lotto_df['date'])

lotto_df['date'] = pd.to_datetime(lotto_df['date'])  # date 필드를 날짜 데이터로 변경
lotto_df['month'] = lotto_df['date'].dt.month  
# 날짜 date 필드에서 월만 추출하여 lotto_df 에 새로운 month 필드를 생성

# print(lotto_df)
#
# print(lotto_df[lotto_df['month'] == 1])

lotto_jan = lotto_df[lotto_df['month'] == 1]

numlist_01 = list(lotto_jan['num1']) + list(lotto_jan['num2']) + list(lotto_jan['num3']) + list(lotto_jan['num4']) + list(lotto_jan['num5']) + list(lotto_jan['num6'])

# print(Counter(numlist_01))

for i in range(1, 13):  # 1~12월까지
    lotto_month_df = lotto_df[lotto_df['month'] == i]  # 1~12월까지의 월별 로또번호 df
    # print(lotto_month_df)
    lotto_month_list = list(lotto_month_df['num1']) + list(lotto_month_df['num2']) + list(lotto_month_df['num3']) + list(lotto_month_df['num4']) + list(lotto_month_df['num5']) + list(lotto_month_df['num6'])
    lotto_month_data = pd.Series(Counter(lotto_month_list))
    # print(lotto_month_data)

    lotto_month_data = lotto_month_data.sort_values(ascending=False)  # 빈도수의 내림차순으로 정렬
    # print('------------------------')
    # print(lotto_month_data)
    # print('------------------------')
    lotto_month_top6 = lotto_month_data.head(6)
    print('*******************')
    print(lotto_month_top6)
    print('*******************')