import requests
import os

def get_weather():
    TOKEN = os.environ.get("WEATHER_KEY")
    LOCATION = os.environ.get("CITY_ID")
    
    # 使用最稳定的国际域名
    url = f"https://api.caiyunapp.com/v2.6/{TOKEN}/{LOCATION}/realtime.json"
    
    # 增加重试机制
    for i in range(3): 
        try:
            print(f"正在尝试获取天气 (第 {i+1} 次)...")
            res = requests.get(url, timeout=15).json()
            if res.get('status') == 'ok':
                result = res['result']['realtime']
                skycon = result['skycon']
                # 常见天气转换
                sky_map = {"CLEAR_DAY": "☀️ 晴", "CLEAR_NIGHT": "🌙 晴", "PARTLY_CLOUDY_DAY": "⛅ 多云", "CLOUDY": "☁️ 阴", "RAIN": "🌧️ 下雨", "SNOW": "❄️ 下雪", "WIND": "💨 大风"}
                weather_text = sky_map.get(skycon, "🌡️ 观测中")
                
                report = (
                    f"🌡️ 当前温度：{result['temperature']}°C\n"
                    f"☁️ 天气状况：{weather_text}\n"
                    f"🍃 风速：{result['wind']['speed']} km/h\n"
                    f"📝 预报建议：{res['result'].get('forecast_keypoint', '祝你今天心情愉快！')}"
                )
                return report
            else:
                print(f"API 返回异常状态: {res.get('status')}")
        except Exception as e:
            print(f"第 {i+1} 次请求失败: {e}")
            if i == 2: # 最后一次尝试也失败了
                return None
    return None

def send_to_wechat(content):
    webhook = os.environ.get("WECHAT_WEBHOOK")
    data = {
        "msgtype": "text",
        "text": {"content": "【彩云精准天气播报】\n" + content}
    }
    requests.post(webhook, json=data)

if __name__ == "__main__":
    info = get_weather()
    if info:
        send_to_wechat(info)
        print("发送成功！")
