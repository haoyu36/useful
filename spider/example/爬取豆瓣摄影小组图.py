# -*- coding: utf-8 -*-
'''
使用多线程爬取豆瓣爱旅行摄影小组前500页帖子中的所有图片
'''

import re
import os
from multiprocessing.pool import ThreadPool

import lxml
from bs4 import BeautifulSoup

from get_page import get_page


MAX_PAGE = 500    # 爬取 500 页的帖子
IMG_FORMAT = ('jpg', 'png', 'gif', 'webp')    # 只下载符合要求的图片
session = get_page()    # 创建请求 session 对象
DIR = f'{os.getcwd()}/douban'    # 图片保存目录


def crawl_dir(url):
    '''迭代返回指定页数内所有帖子的链接与标题'''
    res = session.get(url, proxy=True)
    if not res:
        return
    soup = BeautifulSoup(res.text, 'lxml')
    for item in soup.find_all('tr')[2:]:
        a_tag = item.find_all('a')
        yield {
            'url': a_tag[0].get('href'),
            'title': a_tag[0].get('title'),
        }


def filter_avatar(url):
    '''使用正则表达式过滤不符合要求的图片'''
    if re.search(r'/up\d{9}', url) or re.search(r'icon', url) or re.search(r'talion', url):
        return False
    return True


def crawl_img_data(data):
    '''迭代返回每张图片的链接，标题，日期'''
    res = session.get(data.pop('url'), proxy=True)
    if not res:
        return

    soup = BeautifulSoup(res.text, 'lxml')
    data_tag1 = soup.find_all('span', class_='timestamp')
    data_tag2 = soup.find_all('span', class_='color-green')
    if data_tag1:
        date = data_tag1[0].get_text()[:10].replace('-', '')
    elif data_tag2:
        date = data_tag2[0].get_text()[:10].replace('-', '')
    else:
        date = '0000'
    data.update(date=date)

    for i in soup.find_all('img'):
        if not i.attrs.get('src'):
            continue
        url = i.attrs['src']
        if url and filter_avatar(url) and url.endswith(IMG_FORMAT):
            data.update(url=url)
            yield data


def save_image(item):
    '''下载图片并保存'''
    date = item.get('date')
    title = item.get('title')
    path = f'{DIR}/{date}/{title}'
    if not os.path.exists(path):
        os.makedirs(path)

    url = item.get('url')
    res = session.get(url, proxy=True)
    if not res:
        return
    
    size = len(res.content)
    if size < 10240:
        return
    suffix = url.split('.')[-1]    # 图片后缀格式
    img_path = f'{path}/{size}.{suffix}'
    if not os.path.exists(img_path):
        with open(img_path, 'wb') as f:
            f.write(res.content)


def main(page):
    '''主函数，控制程序执行'''
    url = f'https://www.douban.com/group/lvxing/discussion?start={str(page)}'
    for data in crawl_dir(url):
        img_data = crawl_img_data(data)
        for i in img_data:
            save_image(i)


if __name__ == '__main__':
    pool = ThreadPool(10)
    pool.starmap(main, [(i*25,) for i in range(MAX_PAGE)])
    pool.close()
    pool.join()
