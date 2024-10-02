# 第0节 网页前端基础

## 一、HTML常见标签

| 标签类型 | 标签                                         |
| -------- | -------------------------------------------- |
| 结构标签 | html, head, body                             |
| 文本标签 | h1, p, a, **span**                           |
| 头部标签 | title, meta, link, script                    |
| 列表标签 | ul, ol, li                                   |
| 表格标签 | table, tr, td, th                            |
| 媒体标签 | img, video, audio                            |
| 表单标签 | form, input, textarea, button, label         |
| 语义标签 | header, footer, nav, article, section, aside |
| 特殊标签 | **div**                                      |


## 二、HTML通用容器

通用容器主要指 div 和 span 标签，它们没有特定的语义，仅用于布局和样式应用。

#### 1、div 标签
- 类型：块级元素
- 用途：用于分组其他元素，创建布局结构。
- 特点：默认占据一整行，常与 CSS 一起使用来控制页面布局。

#### 2、span 标签
- 类型：内联元素
- 用途：用于在文本中标记小块内容，便于应用样式。
- 特点：不会打断文本流，适合对文本中的特定部分进行样式化。

这两个标签主要用于通过 CSS 和 JavaScript 操作页面元素，提供灵活的结构化方式。

## 三、CSS基础
#### 1、CSS选择器
- **元素选择器**：直接选择 HTML 标签，如 p、h1。
- **类选择器**：使用 . 选择类名，如 .className。
- **ID 选择器**：使用 # 选择 ID，如 #idName。
- **属性选择器**：选择具有特定属性的元素，如 [type="text"]。

#### 2、样式优先级
- **内联样式**（直接写在元素上的 style 属性）优先级最高。
- **ID 选择器**（如 #id）优先级第二高。
- **类选择器、伪类选择器**（如 .class、:hover）优先级第三高。
- **元素选择器、伪元素选择器**（如 div、p、::before）优先级最低。

#### 3、实践中的应用
- **内联样式**：直接在 HTML 标签中使用 style 属性，不推荐用于大规模样式。
- **内部样式表**：在 HTML 文件的 head 部分使用 style 标签。
- **外部样式表**：通过 link 标签引入外部 CSS 文件，推荐用于维护和复用。

## 四、HTML和CSS的关系
HTML 的全称是 HyperText Markup Language，中文是超文本标记语言

CSS 的全称是 Cascading Style Sheets，中文是层叠样式表

#### 1、HTML 的作用
- **结构化内容**：HTML 定义了网页的基本结构和内容。
- **语义化标签**：通过使用语义化标签提高网页的可读性和可访问性。

#### 2、CSS 的作用
- **样式化内容**：CSS 用于控制网页的视觉表现，包括颜色、字体、布局等。
- **响应式设计**：通过媒体查询和弹性布局，使网页适应不同设备和屏幕尺寸。

#### 3、二者的结合
**分离结构与样式**：HTML 负责内容和结构，CSS 负责样式和布局，实现关注点分离。

## 五、DOM简介
#### 1、DOM 的定义
DOM（文档对象模型）是浏览器将 HTML 和 XML 文档解析成的树形结构，允许编程语言（如 JavaScript）对文档的内容和结构进行动态访问和更新。

#### 2、DOM 的结构
- **节点**：文档中的每个部分都是一个节点，包括元素节点、文本节点、属性节点等。
- **树形结构**：整个文档被表示为一个树形结构，根节点是 document。

#### 3、常见操作
- **访问节点**：使用 document.getElementById、document.querySelector 等方法。
- **修改节点**：更改节点的内容、属性和样式。
- **添加和删除节点**：使用 appendChild、removeChild 等方法操作节点。

## 六、JavaScript 简介

JavaScript 是一种轻量级的编程语言，主要用于为网页添加交互功能。

#### 1、JavaScript 的作用
- **动态交互**：为网页添加交互功能，如表单验证、动态内容更新。
- **操作 DOM**：通过 JavaScript 修改 HTML 和 CSS，实现动态效果。
- **事件处理**：响应用户操作，如点击、输入等事件。

#### 2、DOM、JavaScript 和 HTML 之间的关系
HTML 定义了网页的基本结构和内容；浏览器将 HTML 转换为 DOM 树，提供了一组接口，允许脚本语言动态访问和修改文档结构、样式和内容；JavaScript用于操作 DOM，实现动态交互。

## 七、补充

以下是一些`<meta>`标签常见的类型：
```html
字符集：
<meta charset="UTF-8">
视口设置：
<meta name="viewport" content="width=device-width, initial-scale=1.0">
描述：
<meta name="description" content="A brief description of the webpage.">
关键词：
<meta name="keywords" content="HTML, CSS, JavaScript">
作者：
<meta name="author" content="Your Name">
刷新：
<meta http-equiv="refresh" content="30">
兼容性：
<meta http-equiv="X-UA-Compatible" content="IE=edge">
版权：
<meta name="copyright" content="© 2024 Your Company">
主题颜色（用于移动浏览器）：
<meta name="theme-color" content="#ffffff">
```

以下是一些`<link>`标签常见的类型：
```html
外部样式表：
<link rel="stylesheet" href="styles.css">
网站图标（favicon）:
<link rel="icon" href="favicon.ico" type="image/x-icon">
预加载资源:
<link rel="preload" href="image.jpg" as="image">
字体:
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans">
RSS 或 Atom 订阅:
<link rel="alternate" type="application/rss+xml" title="RSS" href="feed.xml">
样式切换:
<link rel="alternate stylesheet" href="alternative.css" title="Alternative Style">
```
