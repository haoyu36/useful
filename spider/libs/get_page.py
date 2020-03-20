# -*- coding: utf-8 -*-
'''
下载网页，随机获取请求头和代理
'''

import time
import random

import requests as _requests
from redis import StrictRedis


# 当 redis 中不存在 UA 时使用 DEFAULT_UA
DEFAULT_UA = 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'  # noqa


class RequestsError(Exception):
    pass


class get_page():

    def __init__(self):
        self._session = _requests.Session()
        self.redis = StrictRedis()

    def get_proxy(self):
        '''从 redis 中随机获取 IP'''
        rv = list(self.redis.hgetall('useful_proxy').keys())
        if not rv:
            return None
        IP = random.choice(rv).decode('utf-8')
        proxy = {'http': IP, 'https': IP}
        return proxy

    def get_user_agent(self, is_mobile=False):
        '''从 redis 中随机获取 UA'''
        key = 'user_agents' if is_mobile else 'user_agents_mobile'
        ua = self.redis.srandmember(key).decode('utf-8')
        user_agent = {'User-Agent': ua or DEFAULT_UA}
        return user_agent

    def get(self, url, num_retries=2, headers={}, proxy=None, timeout=20, is_mobile=False, **kwargs):
        headers = dict(self.get_user_agent(is_mobile=is_mobile), **headers)
        # 当代理为空时，不使用代理获取响应
        if proxy is None:
            try:
                r = self._session.get(url, headers=headers, timeout=timeout, **kwargs)  # noqa
                if r.status_code == 200:
                    print(f'>>>>>> 请求成功: {url}')
                    return r
                else:
                    raise RequestsError
            except:
                if num_retries > 0:    # num_retries 为限定的重试次数
                    print('请求错误，10 秒后重新请求')
                    time.sleep(10)
                    return self.get(url, num_retries - 1)
                # 重复次数用完后，开始使用代理
                else:
                    proxy = self.get_proxy()
                    return self.get(url, num_retries=5, proxy=proxy)
        # 当代理不为空，使用代理
        else:
            try:
                proxy = self.get_proxy()
                r = self._session.get(url, headers=headers, proxies=proxy, timeout=timeout, **kwargs)  # noqa
                if r.status_code == 200:
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
                    r = self._session.get(url, headers=headers, timeout=timeout, **kwargs)    # noqa
                    if r.status_code == 200:
                        print(f'>>>>>> 请求成功: {url}')
                        return r
                    else:
                        print(f'###### 请求失败: {url}')
                        return None


if __name__ == '__main__':
    session = get_page()
