import requests
from anaconda3.Lib.multiprocessing.sharedctypes import class_cache
from bs4 import BeautifulSoup
from datetime import datetime


url="https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=1"

html = requests.get(url).text

print(html)

soup = BeautifulSoup(html, 'lxml')

date = datetime.strptime(soup.find('p', class_='desc').text, '(%Y년 %m월 %d일 추첨)')

print(date)

lottoNum_list = soup.find('div', class_='num win').find('p').text.strip().split('\n')
lottoNum_list_int = []
# 1회 당첨번호 6개를 리스트로 변환
for i in lottoNum_list:  # 문자열 로또번호 6개를 모두 정수로 변환
    lottoNum_list_int.append(int(i))

print(lottoNum_list_int)

bonus_num = int(soup.find('div', class_='num bonus').find('p').text.strip())  #보너스 번호 크롤링

lotto_dic = {'date':date, 'lottoNumber':lottoNum_list_int, 'bonusNumber':bonus_num}

print(lotto_dic)



