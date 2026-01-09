import requests
import os

def get_weather():
    TOKEN = os.environ.get("WEATHER_KEY")
    LOCATION = os.environ.get("CITY_ID")
    
    # 彩云 API 国际版域名，更稳定
    url = f"https://api.caiyunapp.com/v2.6/{TOKEN}/{LOCATION}/weather.json?dailysteps=1"
    
    try:
        res = requests.get(url, timeout=15).json()
        if res.get('status') == 'ok':
            result = res['result']
            realtime = result['realtime']
            daily = result['daily']
            
            # 天气图标转换
            sky_map = {"CLEAR_DAY": "☀️ 晴", "CLEAR_NIGHT": "🌙 晴", "PARTLY_CLOUDY_DAY": "⛅ 多云", "CLOUDY": "☁️ 阴", "RAIN": "🌧️ 下雨", "SNOW": "❄️ 下雪"}
            weather_text = sky_map.get(realtime['skycon'], "🌡️ 观测中")

            # 组装文本内容
            report = (
                f"今日天气：{weather_text}\n"
                f"🌡️ 实时温度：{realtime['temperature']}°C\n"
                f"📈 气温范围：{int(daily['temperature'][0]['min'])}°C ~ {int(daily['temperature'][0]['max'])}°C\n"
                f"👕 穿衣建议：{daily['life_index']['dressing'][0]['desc']}\n"
                f"📝 贴心提醒：{result.get('forecast_keypoint', '祝你今天心情愉快！')}"
            )
            return report
        return None
    except Exception as e:
        print(f"获取天气失败: {e}")
        return None

def send_to_wxpusher(content):
    app_token = os.environ.get("WXPUSHER_TOKEN")
    uids = os.environ.get("WXPUSHER_UIDS").split(",") # 支持多个UID
    
    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": app_token,
        "content": content,
        "contentType": 1, # 1表示文本
        "uids": uids,
        "summary": "今日天气提醒" # 微信卡片上显示的摘要
    }
    
    try:
        res = requests.post(url, json=data).json()
        if res.get('code') == 1000:
            print("消息通过 WxPusher 发送成功！")
        else:
            print(f"WxPusher 发送失败: {res.get('msg')}")
    except Exception as e:
        print(f"推送异常: {e}")

if __name__ == "__main__":
    weather_info = get_weather()
    if weather_info:
        send_to_wxpusher(weather_info)
