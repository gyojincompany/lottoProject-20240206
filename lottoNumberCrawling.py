import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine


# 최신 회차 크롤링 함수
def get_recent_count():
    url = "https://dhlottery.co.kr/common.do?method=main"
    html = requests.get(url).text
    # print(html)
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    recent_count = soup.find('strong', id='lottoDrwNo').text  #로또 최신회차값 가져오기
    # print(recent_count)
    recent_count = int(recent_count)  # 최신회차값을 정수로 변경
    return recent_count

# 회차별 로또번호, 추첨일, 보너스 번호를 조회 함수
def get_lotto_number(count):
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={count}"

    html = requests.get(url).text

    # print(html)

    soup = BeautifulSoup(html, 'lxml')

    date = datetime.strptime(soup.find('p', class_='desc').text, '(%Y년 %m월 %d일 추첨)')   

    lottoNum_list = soup.find('div', class_='num win').find('p').text.strip().split('\n')
    lottoNum_list_int = []
    # 1회 당첨번호 6개를 리스트로 변환
    for i in lottoNum_list:  # 문자열 로또번호 6개를 모두 정수로 변환
        lottoNum_list_int.append(int(i))

    bonus_num = int(soup.find('div', class_='num bonus').find('p').text.strip())  # 보너스 번호 크롤링

    lotto_dic = {'date': date, 'lottoNumber': lottoNum_list_int, 'bonusNumber': bonus_num}
    
    return lotto_dic

recent_count = get_recent_count()  # 최신회차 가져오기(정수값) ex:1105

list_df = []

for i in range(1, recent_count+1):
    result = get_lotto_number(i)

    list_df.append({
                    'count': i,  # 로또 회차
                    'date': result['date'],  # 로또 추첨일
                    'num1': result['lottoNumber'][0],
                    'num2': result['lottoNumber'][1],
                    'num3': result['lottoNumber'][2],
                    'num4': result['lottoNumber'][3],
                    'num5': result['lottoNumber'][4],
                    'num6': result['lottoNumber'][5],
                    'bonus': result['bonusNumber']
    })

    print(i)

# print(list_df)

lotto_df = pd.DataFrame(data=list_df, columns=['count','date','num1','num2','num3','num4','num5','num6','bonus'])
# print(lotto_df)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/pydb?charset=utf8mb4")
engine.connect()

lotto_df.to_sql(name='lotto_tbl', con=engine, if_exists='append', index=False)

# lotto_df.to_csv('lotto_Data.csv', index=False)  # csv로 변환

