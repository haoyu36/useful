



## 一：requests 方法

```python
requests.request()     # 构造一个请求支撑以下各方法的基础
requests.get()         # 获取HTML网页的主要方法，对应于HTTP的GET
requests.head()        # 获取HTML网页头信息的方法，对应于HTTP的HEAD
requests.post()        # 向HTML网页提交POST请求的方法，对应于HTTP的POST
requests.put()         # 向HTML网页提交PUT请求的方法，对应于HTTP的PUT
requests.patch()       # 向HTML网页提交局部修改的请求，对应于HTTP的PATCH
requests.delete()      # 向HTML网页提交删除请求，对应于HTTP的DELETE
```

## 二：GET 请求

`r = requests.get(url, params=None, **kwargs)`

通过 `get` 方法得到一个名为 `r` 的 `Response` 对象，可以从这个对象中获取所有想要的信息

`response` 包含服务器返回的信息，也包含向服务器请求的 `requests` 信息。`params` 是 `url` 中的额外参数，字典或字节流格式，`**kwargs` 是 12 个控制访问的参数

response的类型：`<class 'requests.models.Response'>`

Response对象有一些属性:

```python
r.status_code           # HTTP请求的返回状态，200表示连接成功，404表示失败
r.text                  # HTTP响应的内容的字符串形式，即url对应的页面内容
r.encoding              # 从HTTP header中猜测的响应内容编码方式
r.apparent_encoding     # 从内容中分析出的响应内容编码方式
r.content               # HTTP响应内容的二进制形式
response.headers
response.cookies        # 访问Cookies,类型为RequestsCookieJar
response.url
response.history
r.raise_for_status()    # 如果状态不是200，引发HTTPError异常
r.josn()                # json格式解析
```

如果网页返回的是 `JSON` 格式的内容，调用 `response.json()` 方法将 `JSON` 格式的字符串转化为字典

`**kwargs`: 控制访问的参数，均为可选项

```python
params      # 字典或字节序列，作为参数增加到 url 中
headers     # 字典，HTTP定制头
date        # 字典，字节序列或文件对象，作为 Request 的内容
files       # 字典类型，传输文件
cookies     # 字典或 CookieJar.request 中的 cookie
timeout     # 设置超时时间，秒为单位
proxies     # 字典类型，设定访问代理服务器，可以增加登录认证
auth        # 元组，支持 HTTP 认证功能
json        # JSON 格式的数据，作为 Request 的内容
```

### timeout

告诉 `requests` 在经过以 `timeout` 参数设定的秒数时间之后停止等待响应。基本上所有的生产代码都应该使用这一参数。如果不使用，程序可能会永远失去响应

`requests.get('http://github.com', timeout=0.001)`


## 三：相关阅读

- [官方文档](http://cn.python-requests.org/zh_CN/latest/)
- [源代码](https://github.com/requests/requests)