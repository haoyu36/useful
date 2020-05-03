## Selenium

`Selenium` 是一个自动化测试工具，利用它可以驱动浏览器执行特定的动作，如点击、下拉等操作，同时还可以获取浏览器当前呈现的页面的源代码，做到可见即可爬

[中文文档](http://selenium-python-zh.readthedocs.io/en/latest/)

```python
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.get('https://www.baidu.com')
print(browser.page_source)
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    #print(browser.page_source)
finally:
    browser.close()
```

## 声明浏览器对象

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser = webdriver.Edge()
browser = webdriver.PhantomJS()
browser = webdriver.Safari()
```

## 访问页面

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.taobao.com')
print(browser.page_source)
browser.close()
```


## 查找单个元素

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.taobao.com')
input_first = browser.find_element_by_id('q')
input_second = browser.find_element_by_css_selector('#q')
input_third = browser.find_element_by_xpath('//*[@id="q"]')

print(input_first,'\n',input_second,'\n',input_third)
browser.close()


find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector


from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get('http://www.taobao.com')
input_first = browser.find_element(By.ID,'q')
print(input_first)
browser.close()
```

## 查找多个元素

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.taobao.com')
its = browser.find_elements_by_css_selector('.service-bd li')
print(its)
browser.close()


from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get('http://www.taobao.com')
its = browser.find_elements(By.CSS_SELECTOR,'.service-bd li')
print(its)
browser.close()


find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector
```

## 元素交互操作

输入文字时用 `send_keys()` 方法，清空文字时用clear()方法，点击按钮时用click()方法

```python
from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('http://www.taobao.com')
input_c = browser.find_element_by_id('q')
input_c.send_keys('iPhone')
time.sleep(1)
input_c.clear()
input_c.send_keys('iPad')
button = browser.find_element_by_class_name('btn-search')
button.click()
```