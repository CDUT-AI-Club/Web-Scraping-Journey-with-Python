import requests
from bs4 import BeautifulSoup
import os

responce = requests.get(
    "https://cn.bing.com/images/search?q=%e6%88%90%e9%83%bd%e7%90%86%e5%b7%a5%e5%a4%a7%e5%ad%a6&form=HDRSC2&first=1"
)
# print("responce.status_code: ", responce.status_code)
# 2xx 状态码表示请求成功
# 4xx 状态码表示客户端错误
# 5xx 状态码表示服务器错误
# print("responce.text: ", responce.text)

soup = BeautifulSoup(responce.text, "lxml")
# print("soup: ", soup)

# print(type(responce.text))
# print(type(soup))

images = soup.find_all("img", class_="mimg")
# print(images)
# print(type(images))

for img in images:
    if img.get("src") == None:
        break
    # print(img)
    # print(type(img))
    img_url = img.get("src")
    print(img_url)


target_folder = "images"
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

img_data = requests.get(img_url).content
# print(img_data)

img_path = os.path.join(target_folder, "target_img.jpg")
with open(img_path, 'wb') as f:
    f.write(img_data)

# response.text:
# 返回的是经过解码的字符串。
# 使用响应的编码（通常是从 HTTP 头中推断）来解码内容。
# response.content:
# 返回的是原始的二进制数据。
# 不进行任何解码，适合处理图像、文件等非文本数据。