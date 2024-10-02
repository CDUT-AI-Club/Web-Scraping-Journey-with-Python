# 第5节 使用selenium爬取动态内容

## 一、下载 WebDriver

以 chromedriver 为例：
- 下载 chrome，在浏览器输入 `chrome://settings/help`
- 查看你的chrome的版本号
- 到官网 [Chrome for Testing (CfT) 可用性信息中心](https://googlechromelabs.github.io/chrome-for-testing/) 下载你的Chrome对应的ChromeDriver的版本

## 二、设置 Chrome 浏览器的选项
在使用 Selenium 的 Chrome 浏览器时，可以通过 chrome_options.add_argument() 添加多种启动参数来配置浏览器行为。以下是一些常用的选项：

| 选项                                 | 描述                                                   |
| ------------------------------------ | ------------------------------------------------------ |
| `--headless`                         | 启用无头模式，不显示浏览器界面。                       |
| `--disable-gpu`                      | 在无头模式下禁用 GPU 加速（某些系统上可能需要）。      |
| `--window-size=width,height`         | 设置浏览器窗口的大小，例如 `--window-size=1920,1080`。 |
| `--incognito`                        | 启动浏览器的隐身模式。                                 |
| `--disable-extensions`               | 禁用所有扩展。                                         |
| `--start-maximized`                  | 启动时最大化窗口。                                     |
| `--no-sandbox`                       | 禁用沙盒模式（可能会提高性能，但存在安全风险）。       |
| `--disable-dev-shm-usage`            | 在某些 Linux 系统上使用，以避免共享内存不足的问题。    |
| `--remote-debugging-port=9222`       | 启用远程调试，指定调试端口。                           |
| `--user-agent=CustomUserAgentString` | 设置自定义的用户代理字符串。                           |

## 三、使用 Selenium 做爬虫的基本流程
1、安装 Selenium 和 WebDriver
- 安装 Selenium 库：
```python
pip install selenium
```
- 下载与浏览器版本匹配的 WebDriver（如 **ChromeDriver**）。

2、导入必要的库

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

3、配置 WebDriver
- 设置浏览器选项：
```python
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
```

- 初始化 WebDriver：
```python
service = Service('path/to/chromedriver')  # 替换为实际路径
driver = webdriver.Chrome(service=service, options=chrome_options)
```

4、打开目标网页
```python
url = "https://example.com"
driver.get(url)
```

5、查找并操作元素
- 使用**各种选择器**查找元素：
```python
element = driver.find_element(By.CSS_SELECTOR, "selector")
```

- 提取信息或进行交互：
```python
text = element.text
element.click()
```

6、等待元素加载（可选）
- 使用显式等待确保元素加载完毕：
```python
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "element_id"))
)
```

7、处理数据
- 提取并处理所需数据，可能包括存储在文件或数据库中。

8、清理资源
- 关闭浏览器：
```python
driver.quit()
```

## 四、常见的选择器
- **ID** 使用元素的唯一 ID。
```python
element = driver.find_element(By.ID, "element_id")
```
- **Class Name** 使用元素的类名。
```python
element = driver.find_element(By.CLASS_NAME, "class_name")
```
- **Name** 使用元素的名称属性。
```python
element = driver.find_element(By.NAME, "name")
```
- **Tag Name** 使用元素的标签名。
```python
element = driver.find_element(By.TAG_NAME, "div")
```
- **CSS Selector** 使用 CSS 选择器。
```python
element = driver.find_element(By.CSS_SELECTOR, ".class_name #element_id")
```
- **XPath** 使用 XPath 表达式。
```python
element = driver.find_element(By.XPATH, "//div[@id='element_id']")
```
- **Link Text** 使用链接文本。
```python
element = driver.find_element(By.LINK_TEXT, "Full Link Text")
```
- **Partial Link Text** 使用部分链接文本。
```python
element = driver.find_element(By.PARTIAL_LINK_TEXT, "Partial Text")
```