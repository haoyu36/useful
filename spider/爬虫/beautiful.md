## 一：Beautiful Soup

[中文文档](http://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/#)

`BeautifulSoup` 库是解析、遍历、维护"标签数"的功能库，`Beautiful Soup` 将复杂 `HTML` 文档转换成一个复杂的树形结构，每个节点都是 `Python` 对象

```python
import requests
from bs4 import BeautifulSoup        # 导入BeautifulSoup

r = requests.get("https://python123.io/ws/demo.html")
demo = r.text
soup = BeautifulSoup(demo, "lxml")   # 使用lxml解析器
print (soup.prettify())              # 格式化打印网页源代码
type(soup)                           # bs4.BeautifulSoup
```

1. `Tag`: 标签，最基本的信息组织单元，分别用<>和</>标明开头和结尾
2. `Name`: 标签的名字，格式: `<Tag>.Name`
3. `Attributes`: 标签的属性，字典格式形式，格式: `<Tag>.Attributes`
4. `NavigableString`: 标签内非属性字符串，格式: `<Tag>.string`
5. `Comment`: 标签内字符串的注释部分，一种特殊的 `Comment` 类型

## 二：方法过滤器

`<>.find_all(name, attrs, recursive, string, **kwargs)`

搜索当前 tag 的所有 tag 子节点，返回一个列表类型，储存查找的结果

### 2.1 name参数

查找所有名字为 `name` 的 `tag`。`name` 参数的值可以使任一类型的过滤器、字符串、正则表达式、列表、方法或是`True`


```python
soup.find_all('a')
soup.find_all(['a','b'])
soup.find_all(re.compile('b'))`
```

### 2.2 attrs参数

对标签属性的检索字符串，可标注属性检索。搜索指定名字的属性时可以使用的参数值包括字符串、正则表达式、列表、`True`

如果一个指定名字的参数不是搜索内置的参数名,搜索时会把该参数当作指定名字 tag 的属性来搜索

```python
soup.find_all('p', 'course')
soup.find_all('p', class_='course')
soup.find_all(id='link2')
soup.find_all(id=re.compile('link'))
soup.find_all(id=True)        # 查找所有包含 id 属性的tag
```

### 2.3 recursive参数

是否对子孙全部检索，默认为 Ture， `recursive=False` 搜索 tag 的直接子节点

### 2.4 string参数

搜文档中的字符串内容。返回符合条件字符串的列表。`string` 参数接受字符串、正则表达式、列表、`True`。 如果将字符串参数和其他参数混合使用，返回`Tag`

```python
soup.find_all(string='Basic Python')
soup.find_all(string=re.compile('Basic Python'))
```

### 2.5 limit参数

当搜索到的结果数量达到 `limit` 的限制时，就停止搜索返回结果

与 `find_all()` 方法类似的方法是 `find()` 。区别是前者返回结果是列表，后者直接返回结果；前者没有找到目标是返回空列表，后者找不到目标时，返回`None`

```html
<html>
 <head>
  <title>
   This is a python demo page
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The demo python introduces several python courses.
   </b>
  </p>
  <p class="course">
   Python is a wonderful general-purpose programming language. You can learn Python from novice to professional by tracking the following courses:
   <a class="py1" href="http://www.icourse163.org/course/BIT-268001" id="link1">
    Basic Python
   </a>
   and
   <a class="py2" href="http://www.icourse163.org/course/BIT-1001870001" id="link2">
    Advanced Python
   </a>
   .
  </p>
 </body>
</html>
```

```python
soup.title                  # 返回<title>标签的选择结果，类型为bs4.element.Tag
soup.title.name             # 该标签的名称
soup.title.string           # 节点的文本内容
soup.title.parent.name      # 父节点的标签名
soup.p                      # 第一个<p>标签的结果
soup.p['class']             # <p>标签的class属性，列表形式返回
soup.find_all('a')          # 列表形式返回所有<a>标签
soup.find(id="link3")       # 返回id="link3"的标签，find直接返回Tag
soup.get_text()             # 从文档中获取所有文字内容
soup.a.get('href')          # 找到<a>标签的链接

soup.a.attrs                # 以字典形式返回标签的多值属性
soup.a.attrs['class']       # 获取指定的属性值

{'href': 'http://www.icourse163.org/course/BIT-268001', 'class': ['py1'], 'id': 'link1'}
['py1']
```

## 三：CSS选择器

`Beautiful Soup` 支持大部分的 `CSS` 选择器，在 `Tag` 或 `BeautifulSoup` 对象的 `.select()` 方法中传入字符串参数，即可使用 `CSS` 选择器的语法找到 `tag`

`CSS` 返回的结果均是符合 `CSS` 选择器的节点组成的列表

```python
soup.select("body a")        # 通过tag标签逐层查找
soup.select("head > title")  # 找到某个tag标签下的直接子标签
soup.select(".sister")       # 通过CSS的类名查找
soup.select("#link1")        # 通过tag的id查找
```