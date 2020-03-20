# -*- coding: utf-8 -*-
'''
爬取 user_agent 并写入 redis
'''

import requests
from redis import StrictRedis
from bs4 import BeautifulSoup


URL = 'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/{os}/{page}'


user_agents = []
user_agents_mobile = []


for os in ['android', 'ios']:
    for page in range(1, 5):
        url = URL.format(os=os, page=page)
        print('请求 url: {}'.format(url))
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        for i in soup.find_all('td', class_="useragent"):
            ua = i.string.strip()
            user_agents_mobile.append(ua)


for os in ['windows', 'linux', 'macos']:
    for page in range(1, 5):
        url = URL.format(os=os, page=page)
        print('请求 url: {}'.format(url))
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        for i in soup.find_all('td', class_="useragent"):
            ua = i.string.strip()
            user_agents.append(ua)


# 将user_agent写入redis
redis = StrictRedis(host='localhost', port=6379)

for i in user_agents:
    redis.sadd('user_agents', i)

for i in user_agents_mobile:
    redis.sadd('user_agents_mobile', i)


def read_to_redis():
    '''从redis中随机读取user_agent'''
    from redis import StrictRedis
    redis = StrictRedis(host='localhost', port=6379)
    key = 'user_agents'
    user_agent = redis.srandmember(key)
    return user_agent
