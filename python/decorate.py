'''
常用的一些装饰器
'''


def spend_time(f):
    '''
    计算函数执行花费的时间
    '''
    import time
    def _(*args, **kwargs):
        beg = time.time()
        res = f(*args, **kwargs)
        print(f'spend time: {time.time()-beg}')
        return res
    return _


'''
In : import time

In : @spend_time
   : def test_spend_time():
   :     time.sleep(2)

In : test_spend_time()
spend time: 2.001162052154541
'''

