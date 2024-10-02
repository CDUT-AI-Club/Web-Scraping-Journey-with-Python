import requests
import json


def get_weather(config_file):
    with open(config_file, "r") as file:
        params = json.load(file)

    url = "https://restapi.amap.com/v3/weather/weatherInfo"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        print(data)

        if data.get("status") == "1":
            weather_info = data.get("lives", [])[0]
            print(f"城市: {weather_info['city']}")
            print(f"天气: {weather_info['weather']}")
            print(f"温度: {weather_info['temperature']}°C")
            print(f"湿度: {weather_info['humidity']}%")
            print(f"更新时间: {weather_info['reporttime']}")
        else:
            print("获取天气信息失败:", data.get("info"))

    except requests.exceptions.RequestException as e:
        print("请求出现错误:", e)


if __name__ == "__main__":
    get_weather("config.json")
