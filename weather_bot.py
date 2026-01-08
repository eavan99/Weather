import requests
import os
import json

KEY = os.environ.get("WEATHER_KEY")
CITY = os.environ.get("CITY_ID")
WEBHOOK = os.environ.get("WECHAT_WEBHOOK")

def get_weather():
    url = f"https://devapi.qweather.com/v7/weather/now?location={CITY}&key={KEY}"
    response = requests.get(url)
    print(f"API返回状态码: {response.status_code}") # 调试用
    res = response.json()
    print(f"API返回数据: {res}") # 调试用
    
    if res.get('code') == '200':
        now = res['now']
        return f"📍 城市ID：{CITY}\n☁️ 天气：{now['text']}\n🌡️ 温度：{now['temp']}°C"
    else:
        print(f"获取天气失败，错误码：{res.get('code')}")
        return None
