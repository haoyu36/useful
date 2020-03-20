# -*- coding: utf-8 -*-

import re
import os
import json
from multiprocessing.pool import ThreadPool

from bs4 import BeautifulSoup
from libs.get_page import get_page


session = get_page()
base_dir = os.getcwd()


def crawl(url):
    r = session.get(url)
    r.encoding = r.apparent_encoding
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    try:
        tree_name = soup.find('dt', string=re.compile(
            '中文[学]名')).next_sibling.next_sibling.string
        tree_ke = soup.find('dt', string=re.compile(
            '^科$')).next_sibling.next_sibling.get_text()
        tree_shu = soup.find('dt', string=re.compile(
            '^属$')).next_sibling.next_sibling.get_text()
        tree_pec = soup.find('div', class_="lemma-summary").get_text()

        tree_value = ""
        tree_value_list = soup.find_all('h3', class_="title-text")
        for i in tree_value_list:
            if "价值" in i.get_text():
                tree_value += i.parent.next_sibling.next_sibling.get_text()

        json = {
            '名称': tree_name.strip(),
            '科': tree_ke.strip(),
            '属': tree_shu.strip(),
            '特征': tree_pec.strip(),
            '价值': tree_value.strip(),
        }
        return json
    except:
        if soup.find(class_='lemmaWgt-subLemmaListTitle'):
            href = soup.find('li', class_='list-dot').a.get('href')
            url = "https://baike.baidu.com" + href
            return crawl(url)
        else:
            return


def write_to_json(content):
    path = f'{base_dir}/results/plants.json'
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, indent=2, ensure_ascii=False) + '\n')


def main(tree):
    start_url = "https://baike.baidu.com/item/"
    url = start_url + tree
    json = crawl(url)
    write_to_json(json)


tree_list = ['榆叶梅', '金枝槐', '五叶槐', '蝴蝶槐', '金银忍冬', '构树', '月季', '胶东卫矛',
             '冬青卫矛', '国槐', '栾树', '旱柳', '松树', '圆柏', '红豆杉', '臭椿', '山梅花', '金叶白蜡', '山桃',
             '碧桃', '西府海棠', '榆树', '沙枣', '南蛇藤', '绚丽海棠', '珍珠梅', '迎春花', '连翘', '丁香',
             '山刺玫', '雪柳', '水荀子', '黄芦', '荊条', '大果榆', '臭檀吴茱萸', '文冠果', '杜仲', '南蛇藤',
             '春榆', '元宝枫', '五角枫', '白杜', '山荊子', '雪松', '君迁子', '黑桃', '山皂荚', '洒金柏',
             '刺槐', '白皮松', '紫藤', '臭椿', '红瑞木']


if __name__ == '__main__':
    pool = ThreadPool(5)
    pool.starmap(main, [(i,) for i in tree_list])
    pool.close()
    pool.join()
