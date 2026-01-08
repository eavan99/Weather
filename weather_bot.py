import requests
import os

# 读取变量
KEY = os.environ.get("WEATHER_KEY")
CITY = os.environ.get("CITY_ID")
WEBHOOK = os.environ.get("WECHAT_WEBHOOK")

def get_weather():
    # 注意：免费订阅版 API 地址是 devapi.qweather.com
    url = f"https://devapi.qweather.com/v7/weather/now?location={CITY}&key={KEY}"
    try:
        response = requests.get(url)
        res = response.json()
        print(f"API Response Code: {res.get('code')}") # 这一行会在日志里显示返回码
        
        if res.get('code') == '200':
            now = res['now']
            # 格式化一下显示效果
            text = now['text']
            temp = now['temp']
            feelsLike = now['feelsLike']
            return f"📍 城市：{CITY}\n☁️ 天气：{text}\n🌡️ 温度：{temp}°C (体感 {feelsLike}°C)\n💧 湿度：{now['humidity']}%"
        else:
            print(f"获取天气失败，和风天气返回码：{res.get('code')}，请检查Key和城市ID")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def send_to_wechat(content):
    if not WEBHOOK:
        print("错误：未检测到 WECHAT_WEBHOOK 变量")
        return
    
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": "【早安天气播报】\n" + content
        }
    }
    r = requests.post(WEBHOOK, json=data, headers=headers)
    print(f"微信推送结果: {r.status_code}, {r.text}")

if __name__ == "__main__":
    weather_info = get_weather()
    if weather_info:
        send_to_wechat(weather_info)
    else:
        print("没有获取到天气信息，不发送消息")
