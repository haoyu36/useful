# -*- coding: utf-8 -*-
'''
获取网页，随机获取请求头和代理
'''


import time
import random
import requests as _requests
from redis import StrictRedis


DEFAULT_UA = 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'


class RequestsError(Exception):
    pass


class get_page():

    def __init__(self):
        self._session = _requests.Session()
        self.redis = StrictRedis(host='localhost', port=6379, password=None)

    def get_proxy(self):
        '''从代理池中获取代理'''
        rv = list(self.redis.hgetall('useful_proxy').keys())
        if rv:
            IP = random.choice(rv)
            if isinstance(IP, bytes):
                IP = IP.decode('utf-8')
            proxy = {'http': IP, 'https': IP}
            return proxy
        else:
            return None

    def get_user_agent(self, is_mobile=False):
        '''随机获取user_agent'''
        if not is_mobile:
            key = 'user_agents'
        else:
            key = 'user_agents_mobile'
        ua = self.redis.srandmember(key)
        if isinstance(ua, bytes):
            ua = ua.decode('utf-8')
        user_agent = {'User-Agent': ua or DEFAULT_UA}
        return user_agent

    def get(self, url, num_retries=1, headers={}, proxy=None, timeout=20, is_mobile=False, **kwargs):
        headers = dict(self.get_user_agent(is_mobile=is_mobile), **headers)
        # 当代理为空时，不使用代理获取响应
        if proxy is None:
            try:
                r = self._session.get(
                    url, headers=headers, timeout=timeout, **kwargs)
                if r and r.status_code == 200:
                    print(f'>>>>>> 请求成功: {url}')
                    return r
                else:
                    raise RequestsError
            except:
                # num_retries为限定的重试次数
                if num_retries > 0:
                    print('请求错误，10 秒后重新请求')
                    time.sleep(10)
                    return self.get(url, num_retries-1)
                 # 重复次数用完后，开始使用代理
                else:
                    proxy = self.get_proxy()
                    # 开始使用代理
                    return self.get(url, num_retries=5, proxy=proxy)
        # 当代理不为空，使用代理
        else:
            try:
                proxy = self.get_proxy()
                # 更换代理
                r = self._session.get(
                    url, headers=headers, proxies=proxy, timeout=timeout, **kwargs)
                if r and r.status_code == 200:
                    print(f'>>>>>> 请求成功: {url}')
                    return r
                else:
                    raise RequestsError
            except:
                if num_retries > 0:
                    # 使用代理请求失败，直接删除
                    self.redis.hdel('useful_proxy', proxy['http'])
                    return self.get(url, num_retries-1, proxy=proxy)
                else:
                    r = self._session.get(
                        url, headers=headers, timeout=timeout, **kwargs)
                    if r and r.status_code == 200:
                        print(f'>>>>>> 请求成功: {url}')
                        return r
                    else:
                        print(f'###### 请求失败: {url}')
                        return


if __name__ == '__main__':
    session = get_page()
