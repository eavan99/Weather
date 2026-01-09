import requests
import os

def get_weather():
    TOKEN = os.environ.get("WEATHER_KEY")
    LOCATION = os.environ.get("CITY_ID")
    
    # 彩云 API 地址，增加 dailysteps=1 确保获取当天的天级预报
    url = f"https://api.caiyunapp.com/v2.6/{TOKEN}/{LOCATION}/weather.json?dailysteps=1"
    
    try:
        res = requests.get(url, timeout=15).json()
        if res.get('status') == 'ok':
            result = res['result']
            
            # --- 1. 获取实时数据 ---
            realtime = result['realtime']
            skycon = realtime['skycon']
            sky_map = {"CLEAR_DAY": "☀️ 晴", "CLEAR_NIGHT": "🌙 晴", "PARTLY_CLOUDY_DAY": "⛅ 多云", 
                       "CLOUDY": "☁️ 阴", "RAIN": "🌧️ 下雨", "SNOW": "❄️ 下雪", "WIND": "💨 大风", "HAZE": "🌫️ 雾霾"}
            weather_text = sky_map.get(skycon, "🌡️ 观测中")

            # --- 2. 获取当天预报 (最高/最低温) ---
            daily = result['daily']
            max_temp = daily['temperature'][0]['max']
            min_temp = daily['temperature'][0]['min']

            # --- 3. 获取穿衣指南 ---
            # 彩云的生活指数在 daily.life_index 中
            dressing = daily['life_index']['dressing'][0]['desc']

            # --- 4. 组装消息 ---
            report = (
                f"今日天气：{weather_text}\n"
                f"🌡️ 实时温度：{realtime['temperature']}°C\n"
                f"📈 气温范围：{int(min_temp)}°C ~ {int(max_temp)}°C\n"
                f"💧 相对湿度：{int(realtime['humidity'] * 100)}%\n"
                f"👕 穿衣建议：{dressing}\n"
                f"📝 贴心提醒：{result.get('forecast_keypoint', '祝你今天心情愉快！')}"
            )
            return report
        else:
            print(f"API 异常: {res.get('status')}")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def send_to_wechat(content):
    webhook = os.environ.get("WECHAT_WEBHOOK")
    data = {
        "msgtype": "text",
        "text": {
            "content": "【彩云精准天气播报】\n" + content,
            "mentioned_list": ["@all"] # 如果不需要艾特所有人，可以删掉这行
        }
    }
    requests.post(webhook, json=data)

if __name__ == "__main__":
    info = get_weather()
    if info:
        send_to_wechat(info)
        print("发送成功！")
