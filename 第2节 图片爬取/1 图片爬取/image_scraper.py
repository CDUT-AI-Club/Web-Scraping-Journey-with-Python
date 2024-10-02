import requests  # 导入请求库，用于发送HTTP请求
from bs4 import BeautifulSoup  # 导入BeautifulSoup库，用于解析HTML
import os  # 导入os库，用于文件和目录操作


# 定义一个函数用于下载图片
def download_image(url, path):
    try:
        # 发送请求获取图片数据
        img_data = requests.get(url, timeout=10).content
        # 以二进制写入方式保存图片
        with open(path, "wb") as f:
            f.write(img_data)
        print(f"Downloaded {path}")  # 打印下载成功的信息
    except requests.exceptions.RequestException as e:
        # 打印下载失败的信息
        print(f"Failed to download {url}: {e}")


# 目标URL，搜索成都理工大学的图片
url = "https://cn.bing.com/images/search?q=成都理工大学"

# 定义存储图片的目标文件夹
target_folder = "images"
# 如果文件夹不存在，则创建
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

try:
    # 发送HTTP GET请求获取网页内容
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},  # 设置用户代理
        timeout=10,  # 设置超时时间
    )
    # 检查请求是否成功
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    # 打印请求失败的信息
    print(f"Request failed: {e}")

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(response.text, "lxml")

# 查找所有图片标签，class为“mimg”
images = soup.find_all("img", class_="mimg")

# 遍历所有找到的图片标签
for index, img in enumerate(images):
    # 获取图片的URL，优先使用“src”，如果没有则使用“data-src”
    img_url = img.get("src") or img.get("data-src")
    if img_url:
        # 定义图片的保存路径
        img_path = os.path.join(target_folder, f"image_{index}.jpg")
        # 调用函数下载图片
        download_image(img_url, img_path)
    else:
        continue  # 如果没有找到URL，跳过

print("下载完成！")  # 打印下载完成的信息
