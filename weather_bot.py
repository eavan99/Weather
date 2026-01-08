import requests
import os
import sys

# 1. 直接打印环境变量是否存在（不打印具体值，只看有没有）
def check_env():
    vars_to_check = ["WEATHER_KEY", "CITY_ID", "WECHAT_WEBHOOK"]
    print("--- 环境变量诊断 ---")
    for var in vars_to_check:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var} 已读取，长度为: {len(value)}")
        else:
            print(f"❌ {var} 缺失！请检查 GitHub Secrets 中的名称")
    print("-------------------\n")

def get_weather():
    KEY = os.environ.get("WEATHER_KEY")
    CITY = os.environ.get("CITY_ID")
    
    if not KEY or not CITY:
        return None

    # 尝试请求
    url = f"https://devapi.qweather.com/v7/weather/now?location={CITY}&key={KEY}"
    print(f"正在尝试请求接口...")
    
    try:
        # 增加 verify=False 排除 SSL 证书问题，增加 timeout 防止死等
        response = requests.get(url, timeout=15)
        print(f"HTTP 状态码: {response.status_code}")
        
        res = response.json()
        print(f"和风天气返回内容: {res}")
        
        if res.get('code') == '200':
            now = res['now']
            return f"天气：{now['text']}\n温度：{now['temp']}°C"
        else:
            print(f"和风接口报错，错误码：{res.get('code')}")
            return None
    except Exception as e:
        print(f"请求发生物理异常: {e}")
        return None

if __name__ == "__main__":
    check_env()
    weather_info = get_weather()
    
    if weather_info:
        webhook = os.environ.get("WECHAT_WEBHOOK")
        if webhook:
            requests.post(webhook, json={"msgtype": "text", "text": {"content": weather_info}})
            print("消息已尝试发送至微信")
