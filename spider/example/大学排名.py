# -*- coding: utf-8 -*-

import os
import csv
from bs4 import BeautifulSoup
from libs.get_page import get_page


session = get_page()
base_dir = os.getcwd()


def crawl(url):
    '''以生成器形式返回每个学校的相关信息'''
    r = session.get(url)
    if not r:
        return
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.find_all('tr'):
        try:
            ranking = item.find_all('td')[0].string
            school = item.find_all('td')[1].string
            provinces = item.find_all('td')[2].string
            score = item.find_all('td')[3].string            
            yield {
                'ranking': ranking,
                'school': school,
                'provinces': provinces,
                'score': score,
                }
        except:
            continue

   
def write_to_csv(context):
    path = f'{base_dir}/results/school.csv'
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ranking','school','provinces','score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in context:
            writer.writerow(i)


if __name__ == '__main__':
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html' 
    data = crawl(url)
    write_to_csv(data)
