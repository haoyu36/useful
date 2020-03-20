# -*- coding: utf-8 -*-

import os
from multiprocessing.pool import ThreadPool

from lxml import html

from libs.get_page import get_page
from libs.save_data import write_to_json

path = os.path.join(os.getcwd(), 'results/maoyan.json')
session = get_page()


def crawl(url):
    '''返回指定页榜单排名的生成器'''
    res = session.get(url)
    if not res:
        return

    root = html.fromstring(res.text.strip())
    for item in root.xpath('//dl[@class="board-wrapper"]/dd'):
        try:
            index = item.xpath('i/text()')[0]
            image = item.xpath('.//img[2]/@data-src')[0]
            title = item.xpath('.//p[@class="name"]/a/@title')[0]
            actor = item.xpath('.//p[@class="star"]/text()')[0].strip()[3:]
            data_time = item.xpath(
                './/p[@class="releasetime"]/text()')[0].strip()[5:]
            score = item.xpath('.//p[@class="score"]/*/text()')

            yield {
                'index': index,
                'image': image,
                'title': title,
                'actor': actor,
                'time': data_time,
                'score': ''.join(score),
            }
        except:
            continue


def main(page):
    url = f'http://maoyan.com/board/4?offset={str(page)}'
    item = crawl(url)
    write_to_json(path, item)
    # write_to_redis(item)
    # write_to_csv(item)


if __name__ == '__main__':
    '''榜单共10页，100项'''
    pool = ThreadPool(5)
    pool.starmap(main, [(i*10,) for i in range(10)])
    pool.close()
    pool.join()
