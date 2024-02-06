import requests
from bs4 import BeautifulSoup

# 최신 회차 크롤링 함수
def get_recent_count():
    url = "https://dhlottery.co.kr/common.do?method=main"
    html = requests.get(url).text
    # print(html)
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    recent_count = soup.find('strong',id='lottoDrwNo').text  #로또 최신회차값 가져오기
    # print(recent_count)
    recent_count = int(recent_count)  # 최신회차값을 정수로 변경
    return recent_count


