import os
import time
import random
import pickle
import csv
import pytz
import datetime
from urllib.parse import urlparse, parse_qs
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd


class BilibiliCommentScraper:
    def __init__(self, chromedriver_path, cookie_file, video_url):
        self.chromedriver_path = chromedriver_path
        self.cookie_file = cookie_file
        self.video_url = video_url
        self.driver = None
        self.session = None
        self.cookies_info = None
        self.params = None
        self.beijing_tz = pytz.timezone("Asia/Shanghai")
        self.ua = UserAgent()

    def setup_selenium_driver(self):
        """设置 Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_service = Service(self.chromedriver_path)
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    def load_cookies(self):
        """从文件加载 cookies 并添加到 driver"""
        self.driver.get("https://www.bilibili.com/")
        with open(self.cookie_file, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    def scroll_page(self, times):
        """滚动页面指定次数"""
        for _ in range(times):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    def get_last_request(self):
        """获取最后一个符合条件的网络请求"""
        for request in reversed(self.driver.requests):
            if "main?oid=" in request.url and request.response:
                return request
        return None

    def extract_params(self, url):
        """从 URL 中提取参数"""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        self.params = {
            "oid": query_params.get("oid", [None])[0],
            "type": query_params.get("type", [None])[0],
        }

    def get_cookies_info(self):
        """获取 cookies 信息"""
        all_cookies = self.driver.get_cookies()
        cookies_dict = {cookie["name"]: cookie["value"] for cookie in all_cookies}
        cookies_str = "; ".join(
            [f"{name}={value}" for name, value in cookies_dict.items()]
        )
        self.cookies_info = {
            "cookies_str": cookies_str,
            "bili_jct": cookies_dict.get("bili_jct", ""),
            "sessdata": cookies_dict.get("SESSDATA", ""),
        }

    def setup_request_session(self):
        """设置 requests 会话"""
        self.session = requests.Session()
        retries = Retry(
            total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def fetch_comments(self, url, params, headers, proxies):
        """获取评论数据"""
        response = self.session.get(
            url, params=params, headers=headers, proxies=proxies
        )
        if response.status_code == 200:
            return response.json()
        return None

    def process_comment(self, comment):
        """处理单个评论数据"""
        ctime = comment["ctime"]
        dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
        formatted_time = (
            dt_object.astimezone(self.beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
            + " 北京时间"
        )

        location = comment["reply_control"].get("location", "未知")
        location = location.replace("IP属地：", "") if location else location

        return [
            comment["member"]["uname"],
            comment["member"]["sex"],
            formatted_time,
            comment["like"],
            comment["content"]["message"].replace("\n", ","),
            location,
            comment["rcount"],
            comment["member"]["level_info"]["current_level"],
            str(comment["member"]["mid"]),
            str(comment["rpid"]),
        ]

    def write_to_csv(self, file_path, data):
        """将数据写入 CSV 文件"""
        with open(file_path, mode="a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def initialize(self):
        """初始化爬虫"""
        self.setup_selenium_driver()
        self.load_cookies()
        self.driver.get(self.video_url)
        time.sleep(5)
        self.scroll_page(10)
        last_request = self.get_last_request()
        if not last_request:
            raise Exception("未找到符合条件的请求")
        self.extract_params(last_request.url)
        self.get_cookies_info()
        self.driver.quit()
        self.setup_request_session()

    def scrape_comments(
        self, start_page, end_page, main_comment_file, reply_comment_file
    ):
        """爬取评论"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Cookie": self.cookies_info["cookies_str"],
            "SESSDATA": self.cookies_info["sessdata"],
            "csrf": self.cookies_info["bili_jct"],
        }

        url_main = "https://api.bilibili.com/x/v2/reply/main"
        url_reply = "https://api.bilibili.com/x/v2/reply/reply"

        for page in range(start_page, end_page + 1):
            data = {
                "next": str(page),
                "type": self.params["type"],
                "oid": self.params["oid"],
                "ps": 20,
                "mode": "3",
            }

            json_data = self.fetch_comments(url_main, data, headers, {})
            if (
                not json_data
                or "data" not in json_data
                or "replies" not in json_data["data"]
            ):
                print(f"页面 {page} 没有有效的评论数据")
                continue

            for comment in json_data["data"]["replies"]:
                comment_data = self.process_comment(comment)
                self.write_to_csv(main_comment_file, [comment_data])

                count = comment["rcount"]
                if count > 0:
                    print(
                        f"在第{page}页中含有二级评论,该条回复下面总共含有{count}个二级评论"
                    )
                    total_pages = (count // 20) + 2

                    for page_pn in range(1, total_pages):
                        data_2 = {
                            "type": self.params["type"],
                            "oid": self.params["oid"],
                            "ps": 20,
                            "pn": str(page_pn),
                            "root": comment_data[-1],  # rpid
                        }

                        json_data_2 = self.fetch_comments(
                            url_reply, data_2, headers, {}
                        )
                        if (
                            not json_data_2
                            or "data" not in json_data_2
                            or "replies" not in json_data_2["data"]
                        ):
                            print(f"在页面{page}下第{page_pn}条评论没有子评论。")
                            continue

                        for reply in json_data_2["data"]["replies"]:
                            reply_data = self.process_comment(reply)
                            self.write_to_csv(reply_comment_file, [reply_data])

                        time.sleep(random.uniform(0.2, 0.3))

            print(f"已经爬取第{page}页。")
            time.sleep(random.uniform(0.2, 0.3))


def main():
    chromedriver_path = "E:\\chromedriver-win64\\chromedriver.exe"
    cookie_file = "cookies.pkl"
    base_url = "https://www.bilibili.com/video/"

    level_1_folder = "comments"
    os.makedirs(level_1_folder, exist_ok=True)

    file_path = "./UP主稿件数据.csv"
    df = pd.read_csv(file_path)

    for column_name in df.columns:
        level_2_folder = level_1_folder + "/" + str(column_name)
        os.makedirs(level_2_folder, exist_ok=True)
        bv_numbers = df[column_name]
        for bv_number in bv_numbers:
            video_url = base_url + str(bv_number) + "/"
            # print(video_url)

            scraper = BilibiliCommentScraper(chromedriver_path, cookie_file, video_url)

            try:
                scraper.initialize()

                level_3_folder = level_2_folder + "/" + str(bv_number)
                os.makedirs(level_3_folder, exist_ok=True)

                main_comment_file = level_3_folder + "/主评论_1.1.csv"
                reply_comment_file = level_3_folder + "/二级评论_1.2.csv"

                # 写入CSV头部
                scraper.write_to_csv(
                    main_comment_file,
                    [
                        [
                            "昵称",
                            "性别",
                            "时间",
                            "点赞",
                            "评论",
                            "IP属地",
                            "二级评论条数",
                            "等级",
                            "uid",
                            "rpid",
                        ]
                    ],
                )
                scraper.write_to_csv(
                    reply_comment_file,
                    [
                        [
                            "昵称",
                            "性别",
                            "时间",
                            "点赞",
                            "评论",
                            "IP属地",
                            "二级评论条数,条数相同说明在同一个人下面",
                            "等级",
                            "uid",
                            "rpid",
                        ]
                    ],
                )

                scraper.scrape_comments(1, 10, main_comment_file, reply_comment_file)
            except Exception as e:
                print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
