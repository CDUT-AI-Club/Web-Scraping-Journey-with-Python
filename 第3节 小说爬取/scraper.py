import requests
from bs4 import BeautifulSoup
import os

base_url = "https://www.kunnu.com/longzu/"

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

target_folder = "龙族小说"
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

combined_data = zip(chapters, extra_urls)

for chapter, extra_url in combined_data:
    count = 0

    chapter_folder = os.path.join(target_folder, chapter)
    if not os.path.exists(chapter_folder):
        os.makedirs(chapter_folder)

    url = base_url + extra_url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    links = soup.find_all("a")[23:]

    for link in links:
        href = link.get("href")
        title = link.get("title")

        if not href or not title:
            continue

        response_1 = requests.get(href)
        soup_1 = BeautifulSoup(response_1.text, "lxml")
        paragraphs = soup_1.find("div", id="nr1")

        if paragraphs:
            # 使用章节标题作为文件名
            file_name = f"{count} {title}.txt"
            file_path = os.path.join(chapter_folder, file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                for p in paragraphs.find_all("p"):
                    file.write(p.text.strip() + "\n")
            count = count + 1

print("下载完成！")
