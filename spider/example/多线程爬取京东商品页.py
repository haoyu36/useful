# -*- coding: utf-8 -*-

import os
import re
import csv
import json
import random
import string
from multiprocessing.pool import ThreadPool
from libs.get_page import get_page


base_dir = os.getcwd()
session = get_page()

KEYWORD = 'iphone'
MAX_PAGE = 50
ESCAPE_REGEX = re.compile(r'\\(?![/u"])')

SEARCH_PAGE = 'https://so.m.jd.com/ware/search._m2wq_list?keyword={keyword}&datatype=1&callback=jdSearchResultBkC{callback_str}&page={page}&pagesize=10&ext_attr=no&brand_col=no&price_col=no&color_col=no&size_col=no&ext_attr_sort=no&merge_sku=yes&multi_suppliers=yes&area_ids=1,72,2819&qp_disable=no&fdesc=%E5%8C%97%E4%BA%AC&t1=1553481462604'


def crawl(url):
    res = session.get(url, is_mobile=True)
    if not res:
        return
    try:
       rv = json.loads(ESCAPE_REGEX.sub('', res.text[20: -2]))
    except json.decoder.JSONDecodeError as e:
       raise Exception(e)

    if rv['errmsg']:
        return rv['errmsg']
    items = rv['data']['searchm']['Paragraph']
    for item in items:
        yield {
            '标题': item['Content']['warename'],
            '价格': item['dredisprice'], 
            '评论数': item['commentcount'], 
            '好评率': item['good']
        }


def write_to_json(content):
    path = f'{base_dir}/results/jd.json'
    with open(path, 'a', encoding='utf-8') as f:
        for i in content:
            f.write(json.dumps(i, indent=2, ensure_ascii=False) + '\n') 


def main(page):
    callback_str = ''.join(random.sample(string.ascii_letters, 2))
    url =  SEARCH_PAGE.format(page=page, keyword=KEYWORD, callback_str=callback_str)
    data = crawl(url)
    write_to_json(data)


if __name__ == '__main__':
    pool = ThreadPool(5)
    pool.starmap(main, [(page,) for page in range(1, MAX_PAGE + 1)])
    pool.close()
    pool.join()
