import requests  # 导入requests库，用于发送HTTP请求
from bs4 import BeautifulSoup  # 导入BeautifulSoup库，用于解析HTML
import os  # 导入os库，用于文件和目录操作
import pandas as pd  # 导入pandas库，用于数据处理


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


# 基础URL，用于搜索图片
base_url = "https://cn.bing.com/images/search?q="

# 读取CSV文件，假设文件中只有一列大学名称
df = pd.read_csv("./universities.csv", header=None)

# 获取大学名称列表
universities = df.iloc[:, 0]


# 定义一个函数用于创建唯一的文件夹
def create_unique_folder(base_folder):
    folder = base_folder
    counter = 1
    # 如果文件夹已存在，创建一个新的文件夹名
    while os.path.exists(folder):
        folder = f"{base_folder}_{counter}"
        counter += 1
    os.makedirs(folder)  # 创建文件夹
    return folder


# 创建存储图片的目标文件夹
target_folder = create_unique_folder("images")

# 遍历每个大学名称
for university in list(universities):
    # 构建搜索URL
    url = base_url + str(university)
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
        continue  # 跳过当前大学，继续下一个

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, "lxml")

    # 查找所有图片标签，class为“mimg”
    images = soup.find_all("img", class_="mimg")

    # 为当前大学创建一个文件夹
    university_folder = os.path.join(target_folder, str(university))
    if not os.path.exists(university_folder):
        os.makedirs(university_folder)

    # 遍历所有找到的图片标签
    for index, img in enumerate(images):
        # 获取图片的URL，优先使用“src”，如果没有则使用“data-src”
        img_url = img.get("src") or img.get("data-src")
        if img_url:
            # 定义图片的保存路径
            img_path = os.path.join(university_folder, f"{index}.jpg")
            # 调用函数下载图片
            download_image(img_url, img_path)

print("下载完成！")  # 打印下载完成的信息
