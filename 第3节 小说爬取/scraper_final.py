import requests  # 导入requests库，用于发送HTTP请求
from bs4 import BeautifulSoup  # 导入BeautifulSoup库，用于解析HTML
import os  # 导入os库，用于文件和目录操作
import time  # 导入time库，用于延时操作
import pandas as pd  # 导入pandas库，用于数据处理

# 基础URL，用于访问龙族小说章节
base_url = "https://www.kunnu.com/longzu/"

# 章节名称列表
chapters = [
    "龙族1火之晨曦",
    "龙族2悼亡者之瞳",
    "龙族3黑月之潮 前传 冰海王座",
    "龙族3黑月之潮 上",
    "龙族3黑月之潮 中",
    "龙族3黑月之潮 下",
    "龙族4奥丁之渊",
    "龙族前传 · 哀悼之翼",
]

# 章节对应的URL后缀
extra_urls = [
    "lz-1/",
    "lz-2/",
    "lz-3-0/",
    "lz-3-1/",
    "lz-3-2/",
    "lz-3-3/",
    "lz-4/",
    "lz-0/",
]

# 创建存储小说的目标文件夹
target_folder = "龙族小说"
os.makedirs(target_folder, exist_ok=True)

# 记录下载失败的信息
failed_downloads = []


# 定义一个函数用于请求网页内容，带有重试机制
def fetch_url(url, retries=3, timeout=20):
    for attempt in range(retries):
        try:
            # 发送HTTP GET请求
            response = requests.get(url, timeout=timeout)
            # 检查请求是否成功
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            # 打印失败信息并等待2秒后重试
            print(f"尝试 {attempt + 1} 获取 {url} 失败: {e}")
            time.sleep(2)
    return None


# 保存下载失败的信息到CSV文件
def save_failed_downloads(failed_downloads, folder):
    df = pd.DataFrame(failed_downloads, columns=["Chapter", "URL", "Error"])
    failed_csv_path = os.path.join(folder, "failed_downloads.csv")
    df.to_csv(failed_csv_path, index=False, encoding="utf-8")


# 将章节名称和URL后缀配对
combined_data = zip(chapters, extra_urls)

# 遍历每个章节
for chapter, extra_url in combined_data:
    # 为每个章节创建一个文件夹
    chapter_folder = os.path.join(target_folder, chapter)
    os.makedirs(chapter_folder, exist_ok=True)

    # 构建章节列表页面的URL
    url = base_url + extra_url
    response = fetch_url(url)

    if not response:
        # 如果获取失败，记录失败信息并跳过
        print(f"无法获取章节列表页面: {url}")
        failed_downloads.append((chapter, url, "Failed to fetch chapter list page"))
        continue

    # 解析章节列表页面
    soup = BeautifulSoup(response.text, "lxml")
    links = soup.find_all("a")[23:]  # 假设章节链接从第24个开始

    # 遍历每个章节链接
    for count, link in enumerate(links):
        href = link.get("href")
        title = link.get("title")

        if not href or not title:
            # 如果链接或标题无效，记录失败信息并跳过
            print(f"跳过无效链接或标题: {link}")
            failed_downloads.append((chapter, href, "Invalid link or title"))
            continue

        # 获取章节内容页面
        response_1 = fetch_url(href)

        if not response_1:
            # 如果获取失败，记录失败信息并跳过
            print(f"无法获取章节内容: {href}")
            failed_downloads.append((chapter, href, "Failed to fetch chapter content"))
            continue

        # 解析章节内容页面
        soup_1 = BeautifulSoup(response_1.text, "lxml")
        paragraphs = soup_1.find("div", id="nr1")

        if paragraphs:
            # 将章节内容写入文本文件
            file_name = f"{count:03d} {title}.txt"
            file_path = os.path.join(chapter_folder, file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                for p in paragraphs.find_all("p"):
                    file.write(p.text.strip() + "\n")
            print(f"成功下载: {file_name}")
        else:
            # 如果未找到内容，记录失败信息
            print(f"未找到内容: {href}")
            failed_downloads.append((chapter, href, "No content found"))

# 保存所有下载失败的信息
save_failed_downloads(failed_downloads, target_folder)

print("下载完成！")  # 打印下载完成的信息
