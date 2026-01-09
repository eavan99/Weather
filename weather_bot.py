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

def send_wechat_app(content):
    corpid = os.environ.get("CORP_ID")
    corpsecret = os.environ.get("CORP_SECRET")
    agentid = os.environ.get("AGENT_ID")
    
    # 1. 获取 token
    token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    token_res = requests.get(token_url).json()
    token = token_res.get("access_token")
    
    # 2. 发送消息
    send_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
    data = {
        "touser": "@all",
        "msgtype": "text",
        "agentid": agentid,
        "text": {"content": content},
        "safe": 0
    }
    
    response = requests.post(send_url, json=data)
    res = response.json()
    
    # 这一行是排查问题的关键！
    print("--- 微信服务器返回结果 ---")
    print(res)
    print("-----------------------")

if __name__ == "__main__":
    weather_info = get_weather()
    if weather_info:
        print("天气获取成功，正在推送...")
        send_wechat_app(weather_info)
    else:
        print("天气获取失败，请检查 WEATHER_KEY 和 CITY_ID")
