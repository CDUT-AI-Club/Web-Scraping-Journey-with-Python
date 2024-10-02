# 第6节 使用scrapy框架进行爬虫

## 一、所谓“框架”

"**框架**"（Framework）在软件开发中，**是指一套用于构建和开发应用程序的基础结构**。框架提供了程序的基本结构，并包含了重复性任务的预定义功能或模块，从而减少开发者从零开始编写代码的工作量。通过使用框架，开发者可以专注于实现特定的业务逻辑，而不必为常见的底层功能（如数据库连接、网络请求、用户身份验证等）编写重复代码。

框架的核心特点包括：
- **预定义结构**：框架通常提供一个项目的基本结构，包含文件夹和模块的组织方式，开发者按照该结构开发代码。比如，Scrapy 框架会自动生成项目结构，包括爬虫、配置文件、管道等模块。
- **模块化功能**：框架包含了处理特定任务的模块，比如网络框架中会提供处理 HTTP 请求的模块，爬虫框架如 Scrapy 则提供了抓取网页、解析内容和存储数据的功能。
- **可扩展性**：框架允许开发者根据项目需求添加自定义的功能。大部分框架具有良好的扩展机制，使开发者可以轻松集成新的库或模块。
- **减少重复劳动**：框架通过提供标准化的功能模块，帮助开发者减少重复劳动，提高开发效率。开发者不需要重复编写如数据库操作、表单验证等常见的代码。
- **规范化开发**：框架通常规定了一些开发标准和最佳实践，帮助开发者编写规范的、可维护的代码。

**例子**：

**以 Scrapy 为例，它是一个 Web 爬虫框架，它的作用是简化开发者编写爬虫程序的过程**，框架会处理：
- 请求调度：Scrapy 自动调度和处理多个 HTTP 请求。
- 数据解析：框架提供了丰富的解析工具，帮助提取网页中的特定数据。
- 数据存储：Scrapy 提供了将数据导出为 JSON、CSV、数据库等的内置功能。

简言之，框架让开发更加高效、简洁，减少了重复工作，并提供了规范化的开发环境。

## 二、使用scrapy框架的基本流程
1、安装Scrapy
```
pip install scrapy
```

2、创建Scrapy项目

打开终端并输入以下命令来创建一个新的Scrapy项目：
```
scrapy startproject myproject
```

3、编写爬虫

进入你的项目目录，然后通过以下命令生成一个新的爬虫：
```
cd myproject
scrapy genspider my_spider github.com
```

这将创建一个名为my_spider.py的爬虫文件，位于spiders目录中。

4、编辑爬虫代码

打开spiders/my_spider.py文件，修改代码如下：

```python
import scrapy
from myproject.items import MyprojectItem

class MySpider(scrapy.Spider):
    name = "my_spider"
    start_urls = ["https://github.com/"]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }

    def parse(self, response):
        # 初始化 Item
        item = MyprojectItem()
        # 使用 CSS 选择器提取 <title> 标签中的文本内容
        item["title"] = response.css("title::text").get()
        yield item

```

5、编辑 items.py

确保在 myproject/items.py 中定义好你的 Item 类：
```python
import scrapy

class MyprojectItem(scrapy.Item):
    title = scrapy.Field() # 定义 title 字段
```

6、运行爬虫

使用以下命令运行你的爬虫，并将结果保存到 output.json 文件中：
```
scrapy crawl my_spider -o output.json
```

你可以输出为不同格式（如 CSV、JSON、XML）。例如，输出为 CSV：
```
scrapy crawl my_spider -o output.csv
```

**补充说明**:

确保你的项目目录结构如下：
````
myproject/
    scrapy.cfg
    myproject/
        __init__.py
        items.py
        middlewares.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            my_spider.py
````

## 三、Scrapy框架的进阶技巧与优化

#### 1、设置爬取频率与延时

在编写爬虫时，调整请求频率和设置下载延迟可以避免因频繁请求而被服务器封禁。可以在 `settings.py` 中设置：
```python
# 设置下载延迟，单位是秒
DOWNLOAD_DELAY = 2  # 每两个请求之间的等待时间

# 禁用cookies（默认启用）
COOKIES_ENABLED = False

# 禁用重试，防止由于意外问题的自动重试，尤其是429错误
RETRY_ENABLED = False
```

#### 2、处理反爬虫机制
许多网站会采取反爬虫措施，比如阻止过于频繁的请求或要求验证码。这里有一些常见的应对策略：

- **使用随机的 User-Agent**：防止因每次请求使用相同的 User-Agent 被识别为爬虫。

安装 scrapy-user-agents 插件：
```
pip install scrapy-user-agents
```

在 settings.py 中启用：
```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}
```

- **使用代理**：通过使用代理池，能够绕过 IP 限制。你可以在 `settings.py` 中配置代理：
```python
PROXY_POOL_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
}
```

#### 3、存储和导出数据
除了 CSV 和 JSON 格式，你还可以将数据保存到数据库中，例如 MySQL 或 MongoDB：

- **保存到 MySQL**：可以使用 scrapy-pipeline 来将抓取的数据保存到 MySQL 数据库。

安装所需的库：
```
pip install pymysql
```

在 `pipelines.py` 中编写将数据存储到数据库的逻辑：
```python
import pymysql

class MySQLPipeline:
    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host='localhost',
            user='youruser',
            password='yourpassword',
            db='yourdatabase',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        sql = "INSERT INTO your_table (title) VALUES (%s)"
        self.cursor.execute(sql, (item['title'],))
        self.connection.commit()
        return item
```

在 `settings.py` 中启用此 pipeline：
```python
ITEM_PIPELINES = {
    'myproject.pipelines.MySQLPipeline': 300,
}
```

#### 4、处理 AJAX 动态加载的内容

对于动态加载数据的网页（如使用 AJAX），可以使用 scrapy-splash 处理动态内容。它能渲染 JavaScript 并解析网页：

- 安装 Splash 和 Scrapy-Splash：
```
pip install scrapy-splash
```

在 `settings.py` 中启用：
```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPLASH_URL = 'http://localhost:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
```

#### 5、Scrapy中的中间件与扩展

中间件（middlewares）允许你对请求和响应进行处理或修改。可以编写自定义中间件来处理 headers、cookies、代理等。

一个简单的自定义中间件示例，可以随机添加不同的 User-Agent：
```python
import random

class RandomUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agents=crawler.settings.getlist('USER_AGENTS')
        )

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
```

在 `settings.py` 中添加 User-Agent 列表并启用此中间件：
```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0',
]
```

## 四、小结

**基本流程**部分涵盖了爬虫的搭建与运行，如项目创建、编写爬虫代码、数据导出等。这些步骤帮助读者快速上手爬取基础数据，例如通过 CSS 选择器提取网页的 title 标签。

**进阶部分**则进一步提升了爬虫的实用性和灵活性。我们探讨了如何设置请求延迟、随机 User-Agent、使用代理、处理动态内容等高级技术，并介绍了如何将抓取的数据保存到 MySQL 等数据库。借助这些技巧，爬虫可以更好地应对复杂的 Web 环境，避免被目标网站封禁或识别为爬虫。

在实际应用中，Scrapy 框架的中间件与扩展功能提供了更大的灵活性，使爬虫开发者能够根据需求自定义请求和响应的处理流程，提高爬取效率和成功率。

**后续学习建议**

- **深入 Scrapy 中间件与扩展机制**：学习编写自定义中间件以满足更多需求。
- **Scrapy 和其他库结合**：如与 Pandas、BeautifulSoup 或 Selenium 结合处理更复杂的任务。
- **分布式爬虫**：进一步学习如何使用 Scrapy-Redis 实现分布式爬虫，提升爬取效率。