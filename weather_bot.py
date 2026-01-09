import requests
import os

def get_weather():
    # 这里依然使用你已经跑通的彩云天气逻辑
    TOKEN = os.environ.get("WEATHER_KEY")
    LOCATION = os.environ.get("CITY_ID")
    url = f"https://api.caiyunapp.com/v2.6/{TOKEN}/{LOCATION}/weather.json?dailysteps=1"
    try:
        res = requests.get(url).json()
        if res.get('status') == 'ok':
            r = res['result']
            return (f"今日{r['realtime']['skycon']}\n"
                    f"🌡️温度：{r['realtime']['temperature']}°C\n"
                    f"📈范围：{int(r['daily']['temperature'][0]['min'])}~{int(r['daily']['temperature'][0]['max'])}°C\n"
                    f"👕穿衣：{r['daily']['life_index']['dressing'][0]['desc']}\n"
                    f"📝提醒：{res['result'].get('forecast_keypoint')}")
    except: return None

def send_test_account():
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    template_id = os.environ.get("TEMPLATE_ID")
    user_ids = os.environ.get("USER_IDS").split(",")
    weather_data = get_weather()
    
    if not weather_data: return

    # 1. 获取微信 Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    token = requests.get(token_url).json().get("access_token")
    
    # 2. 推送模板消息
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    for user_id in user_ids:
        body = {
            "touser": user_id.strip(),
            "template_id": template_id,
            "data": {"content": {"value": weather_data, "color": "#173177"}}
        }
        requests.post(send_url, json=body)

if __name__ == "__main__":
    send_test_account()
