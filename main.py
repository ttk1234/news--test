import os
import requests
import json
import urllib.request
import datetime

# ==========================================
# 👇 [설정] 원하는 뉴스 주제를 여기에 적으세요!
KEYWORDS = ["IT", "인공지능", "AI", "QA"] 
# ==========================================

# 환경변수 가져오기
NAVER_ID = os.environ['NAVER_ID']
NAVER_SECRET = os.environ['NAVER_SECRET']
DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']

def get_news(keyword):
    encText = urllib.parse.quote(keyword)
    # 검색어당 최신순으로 3개만 가져오기 (display=3)
    url = f"https://openapi.naver.com/v1/search/news?query={encText}&display=3&sort=date"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", NAVER_ID)
    request.add_header("X-Naver-Client-Secret", NAVER_SECRET)
    
    try:
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return json.loads(response.read().decode('utf-8'))['items']
    except Exception as e:
        print(f"Error fetching news for {keyword}: {e}")
    return []

def send_discord_message():
    # 현재 날짜
    today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    
    embeds = []
    
    for keyword in KEYWORDS:
        news_list = get_news(keyword)
        if not news_list:
            continue
            
        # 각 키워드별로 임베드 하나씩 생성
        field_text = ""
        for news in news_list:
            title = news['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
            link = news['link']
            field_text += f"• [{title}]({link})\n"
            
        embed = {
            "title": f"🔍 {keyword} 주요 뉴스",
            "description": field_text,
            "color": 5814783 # 파란색 계열
        }
        embeds.append(embed)

    if not embeds:
        print("보낼 뉴스가 없습니다.")
        return

    # 디스코드로 전송
    data = {
        "content": f"📢 **{today} 뉴스 브리핑이 도착했습니다!**",
        "embeds": embeds
    }
    
    result = requests.post(DISCORD_WEBHOOK, json=data)
    if result.status_code == 204:
        print("뉴스 전송 완료!")
    else:
        print(f"전송 실패: {result.status_code}")

if __name__ == "__main__":
    send_discord_message()
