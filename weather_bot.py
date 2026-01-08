import requests
import os

# 从环境变量中读取敏感信息
KEY = os.environ.get("WEATHER_KEY")
CITY = os.environ.get("CITY_ID")
WEBHOOK = os.environ.get("WECHAT_WEBHOOK")

def get_weather():
    # 获取实时天气
    url = f"https://devapi.qweather.com/v7/weather/now?location={CITY}&key={KEY}"
    res = requests.get(url).json()
    if res['code'] == '200':
        now = res['now']
        return f"📍 城市：北京\n☁️ 天气：{now['text']}\n🌡️ 温度：{now['temp']}°C\n💧 湿度：{now['humidity']}%"
    return None

def send_to_wechat(content):
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": "【早安天气播报】\n" + content,
            "mentioned_list": ["@all"]  # 是否艾特所有人
        }
    }
    requests.post(WEBHOOK, json=data, headers=headers)

if __name__ == "__main__":
    weather_info = get_weather()
    if weather_info:
        send_to_wechat(weather_info)
