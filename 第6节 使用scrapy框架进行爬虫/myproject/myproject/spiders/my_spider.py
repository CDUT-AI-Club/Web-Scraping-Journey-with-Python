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
