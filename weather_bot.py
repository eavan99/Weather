import requests
import os

def get_weather():
    TOKEN = os.environ.get("WEATHER_KEY")
    LOCATION = os.environ.get("CITY_ID") # 这里存的是经纬度，如 116.40,39.90
    
    # 彩云天气 API 地址 (实时数据接口)
    url = f"https://api.cyapi.cn/v2.6/{TOKEN}/{LOCATION}/realtime.json"
    
    try:
        res = requests.get(url).json()
        if res.get('status') == 'ok':
            result = res['result']['realtime']
            
            # 翻译天气状况代码
            skycon = result['skycon'] 
            # 简单转换一下几个常见的
            sky_map = {"CLEAR_DAY": "晴", "CLEAR_NIGHT": "晴", "PARTLY_CLOUDY_DAY": "多云", "CLOUDY": "阴", "RAIN": "下雨", "SNOW": "下雪"}
            weather_text = sky_map.get(skycon, skycon)
            
            report = (
                f"🌡️ 当前气温：{result['temperature']}°C\n"
                f"☁️ 天气状况：{weather_text}\n"
                f"💨 风速：{result['wind']['speed']} km/h\n"
                f"💧 相对湿度：{int(result['humidity'] * 100)}%\n"
                f"🛰️ PM2.5指数：{result['air_quality']['pm25']}\n"
                f"📝 实时提醒：{res['result'].get('forecast_keypoint', '祝你有愉快的一天！')}"
            )
            return report
        else:
            print(f"彩云 API 报错：{res.get('status')}")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
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
