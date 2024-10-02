# 控制浏览器的核心模块，用于启动和管理浏览器会话
from selenium import webdriver

# 允许配置浏览器启动选项，比如无头模式、禁用扩展等
from selenium.webdriver.chrome.options import Options
# 管理 ChromeDriver 的服务，确保驱动程序正确启动和运行
from selenium.webdriver.chrome.service import Service

# 提供一系列条件，用于等待操作，比如等待元素可见、可点击等
from selenium.webdriver.support import expected_conditions as EC
# 提供多种定位策略，帮助你准确找到页面上的元素
from selenium.webdriver.common.by import By
# 实现显式等待，确保在执行操作前元素已经加载完毕，增加脚本的可靠性
from selenium.webdriver.support.ui import WebDriverWait

import requests
import os


def save_file(url, filename, folder_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"文件已保存为 {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")


# 设置 Chrome 浏览器的选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面

# 初始化 WebDriver
service = Service(
    "E:\\chromedriver-win64\\chromedriver.exe"
)  # 替换为 chromedriver 的实际路径
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://pan.uvooc.com/Learn/CET/CET4/2007年-2015年英语四级真题及解析"

folder_path = "files"

# 打开目标网页
driver.get(url)

# 等待元素加载
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.list-item.viselect-item.hope-stack")
        )
    )
    # WebDriverWait(driver, 10):
    # 创建一个 WebDriverWait 对象，设置最大等待时间为 10 秒。
    #
    # .until(...):
    # 指定等待的条件。在条件满足之前，脚本会暂停执行，直到超时。
    #
    # EC.presence_of_all_elements_located(...):
    # EC 代表 expected_conditions，提供了一系列等待条件。
    # presence_of_all_elements_located 是其中一个条件，表示等待页面上所有符合条件的元素出现。
    #
    # (By.CSS_SELECTOR, "a.list-item.viselect-item.hope-stack"): 使用 CSS 选择器定位元素。
    # By.CSS_SELECTOR 指定使用 CSS 选择器的方式。
    # "a.list-item.viselect-item.hope-stack" 是选择器字符串，用于匹配页面上的 a 标签。

    # 查找所有符合条件的 a 标签
    a_tags = driver.find_elements(
        By.CSS_SELECTOR, "a.list-item.viselect-item.hope-stack"
    )

    # # 提取 href 属性
    # for a_tag in a_tags:
    #     href = a_tag.get_attribute("href")
    #     if href:
    #         print(href)

    p_tags = driver.find_elements(
        By.CSS_SELECTOR, "p.name.hope-text.hope-c-PJLV.hope-c-PJLV.hope-c-PJLV-imGcw-css"
    )
    # for p_tag in p_tags:
    #     title = p_tag.get_attribute("title")
    #     if title:
    #         print(title)
    driver.quit()
    # 提取并保存文件
    for a_tag, p_tag in zip(a_tags, p_tags):
        href = a_tag.get_attribute("href")
        title = p_tag.get_attribute("title")
        if href and title:
            save_file(href, title, folder_path)
finally:
    # 关闭浏览器
    driver.quit()
