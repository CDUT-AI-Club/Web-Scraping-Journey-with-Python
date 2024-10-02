import requests
import csv
import time

# API key配置
API_KEY = "换成自己的api_key"
API_URL = "https://restapi.amap.com/v3/geocode/geo"

# 输入城市列表文件
input_file = "counties.csv"
# 输出的文件
output_file = "counties_coordinates.csv"

# 读取城市列表
with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # 跳过第一行
    cities = [row[0] for row in reader]

# 打开输出文件
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["城市名称", "经度", "纬度"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 逐个城市获取经纬度
    for i, city in enumerate(cities):
        print(f"正在处理城市: {city} ({i+1}/{len(cities)})")

        # 限制请求频率，避免被API限制
        time.sleep(0.1)

        params = {"key": API_KEY, "address": city}
        try:
            response = requests.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data["status"] == "1" and data["geocodes"]:
                geocode = data["geocodes"][0]
                location = geocode["location"].split(",")
                writer.writerow(
                    {"城市名称": city, "经度": location[0], "纬度": location[1]}
                )
            else:
                print(f"获取{city}的经纬度失败")
                print(f"响应内容: {data}")  # 打印响应内容

        except requests.RequestException as e:
            print(f"请求{city}时发生错误: {e}")

print(f"经纬度已保存到{output_file}")
