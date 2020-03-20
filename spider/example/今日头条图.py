# -*- coding: utf-8 -*-

import re
import os
from libs.get_page import get_page
from multiprocessing.pool import ThreadPool

base_dir = os.getcwd()
session = get_page()

KEYWORD = '街拍'
MAX_PAGE = 5
SEARCH_PAGE = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={offset}&format=json&keyword={keyword}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1553515713562'


def crawl(url):
    res = session.get(url)
    if not res:
        return
    data = res.json().get('data')
    if data:
        for item in data:
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                origin_image = re.sub("list", "origin", image.get('url'))
                yield {
                    'image': origin_image,
                    'title': title,
                }


def save_image(item):
    path = f'{base_dir}/results/img'
    if not os.path.exists(path):
        os.makedirs(path)
    res = session.get(item.get('image'))
    if not res:
        return
    file_path = path + os.path.sep + f'{res.url[-4:]}.jpg'
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(res.content)


def main(offset):
    url = SEARCH_PAGE.format(offset=offset, keyword=KEYWORD)
    for item in crawl(url):
        print(item)
        save_image(item)


if __name__ == '__main__':
    pool = ThreadPool(10)
    pool.starmap(main, [(i*20,) for i in range(MAX_PAGE)])
    pool.close()
    pool.join()
