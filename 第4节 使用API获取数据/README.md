# 第4节 使用API获取数据

该文档作为代码的补充。

## 一、JSON文件
JSON（JavaScript Object Notation）是一种**轻量级的数据交换格式**。它易于人类阅读和编写，同时也易于机器解析和生成。JSON通常用于在客户端和服务器之间传输数据。它的结构由键值对和数组组成，类似于Python中的字典或JavaScript中的对象。

**数据类型**：
- 字符串（String）：用双引号括起来。
- 数字（Number）：整数或浮点数。
- 布尔值（Boolean）：true 或 false。
- 空值（null）：表示空值。
- 对象（Object）：键值对的集合。
- 数组（Array）：值的有序列表。

**示例**：
```json
{
    "name": "Alice",
    "age": 30,
    "isStudent": false,
    "address": null,
    "courses": ["Math", "Science", "History"],
    "profile": {
        "id": 12345,
        "active": true
    }
}
```

**使用场景**:
- Web开发：在客户端和服务器之间传递数据。
- 配置文件：用于存储简单的配置数据。
- 数据存储：在NoSQL数据库中使用JSON格式存储数据。

## 二、高德开放平台 | 高德地图API

本代码使用API来自[高德开放平台](https://lbs.amap.com/)，官方文档：[链接](https://developer.amap.com/api/webservice/summary)