# 第1节 爬虫基础

该文档作为代码的补充。

## 一、HTTP/HTTPS协议

HTTP（HyperText Transfer Protocol）是用于传输网页的协议。

HTTPS 是加密的 HTTP，使用 TLS/SSL 加密数据以提高安全性。

#### 1、请求方法

常见的有 GET（获取资源）、POST（提交数据）、PUT（更新资源）、DELETE（删除资源）等。

爬虫主要依赖于 GET 请求来抓取网页内容。在 Python 中使用 requests 库时，**requests.get() 用于发送 GET 请求**，除此之外，使用http.client（Python内置库）、urllib（Python内置库）、httpx（第三方库，支持异步）、aiohttp（异步请求）也可以发送GET请求。

#### 2、请求结构

- **请求行**：包含请求方法（如 GET、POST）、请求的 URL 路径和 HTTP 版本，示例：
```
GET /index.html HTTP/1.1
```
- **请求头（Headers）**：提供请求的附加信息，如用户代理、接受的内容类型等。示例：
```
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
```
- **空行**：用于分隔请求头和请求体。
- **请求体（Body）**（可选）：包含发送到服务器的数据，通常在 POST 请求中使用。

#### 3、响应结构
- **状态行**：包含 HTTP 版本、状态码和状态描述。
```
HTTP/1.1 200 OK
```
- **响应头（Headers）**：提供关于响应的附加信息。常见的有：Content-Type: 响应内容的类型（如 text/html）；Content-Length: 响应体的长度；Set-Cookie: 设置 Cookies；Server: 服务器信息。
- **空行**：用于分隔响应头和响应体。
- **响应体（Body）**：包含实际的数据内容，如 HTML 文档、JSON 数据、图像等。

#### 4、状态码
HTTP 状态码有如下五类（部分）：

- 1xx（信息性状态）：
  - 100 Continue：继续请求。
  - 101 Switching Protocols：切换协议。
- 2xx（成功）：
  - **200 OK：请求成功。**
  - 201 Created：已创建新资源。
  - 204 No Content：无内容。
- 3xx（重定向）：
  - 301 Moved Permanently：永久重定向。
  - 302 Found：临时重定向。
  - 304 Not Modified：未修改。
- 4xx（客户端错误）：
  - 400 Bad Request：请求错误。
  - 401 Unauthorized：未授权。
  - 403 Forbidden：禁止访问。
  - **404 Not Found：未找到资源。**
- 5xx（服务器错误）：
  - 500 Internal Server Error：服务器内部错误。
  - **502 Bad Gateway：错误网关。**
  - 503 Service Unavailable：服务不可用。

**重定向**是指服务器告诉客户端请求的资源已被移动到另一个位置，客户端需要访问新的 URL。

## 二、浏览器的开发者工具
按下网页的 F12 键会打开浏览器的开发者工具。开发者工具提供多种功能，帮助开发者和用户进行调试和分析网页，包括：

- **元素（Elements）**
  - 查看和编辑 HTML 和 CSS：可以实时查看和修改网页的结构和样式。
  - 检查 DOM 树：了解页面元素的层次结构。
- 控制台（Console）
  - 调试 JavaScript：输入和执行代码，查看输出和错误信息。
  - 日志信息：查看网页运行时的日志、警告和错误。
- **网络（Network）**
  - 监控请求和响应：查看所有网络请求的详细信息，包括状态码、头信息、加载时间等。
  - 分析性能：识别哪些资源影响了页面加载速度。
- 性能（Performance）
  - 记录和分析页面性能：帮助识别和解决性能瓶颈。
  - 帧速率、内存使用：查看页面的渲染和内存使用情况。
- 应用程序（Application）
  - 管理存储：查看和管理 Cookies、Local Storage、Session Storage 等。
  - 检查缓存和服务工作线程：管理和调试 PWA（渐进式 Web 应用）的相关功能。
- 安全性（Security）
  - 查看安全信息：检查页面的安全状态和 SSL 证书信息。
- 网络条件（Network Conditions）
  - 模拟网络速度：测试页面在不同网络条件下的表现。
  - 切换 User-Agent：模拟不同设备和浏览器的请求。

## 三、爬虫的伦理和法律

#### 1、伦理：
- 尊重网站的使用条款：查看并遵守网站的 robots.txt 文件和使用条款。
- 不影响网站性能：控制请求频率，避免对网站服务器造成负担。
- 尊重隐私：不收集或使用个人敏感信息。
- 透明和诚实：明确说明数据的使用目的。

#### 2、法律
- 遵守版权法：不侵犯网站的版权或知识产权。
- 数据保护法：遵循相关的数据保护法律，如 GDPR（适用于欧盟）。
- 合法使用数据：确保数据的使用符合法律规定，并获得必要的许可。

在中国，主要的数据保护法是**《中华人民共和国个人信息保护法》（PIPL）**。它于2021年生效，旨在保护个人信息安全，规范个人信息处理活动。

#### 3、实践建议
- 获取许可：在可能的情况下，联系网站管理员并获得数据使用许可。
- **使用API：如果网站提供官方 API，优先使用它来获取数据。**
- 记录日志：记录爬虫活动日志，以便在出现问题时进行审查。

#### 4、如何查看robots.txt
- 打开浏览器。
- 在地址栏输入网址：输入网站的主域名后加上 /robots.txt。
例如，要查看 github.com/ 的 robots.txt，在地址栏输入 https://www.github.com/robots.txt。
查看内容：
- 你将看到该网站的 robots.txt 文件内容，其中包含爬虫的访问规则。
