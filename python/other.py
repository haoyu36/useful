
import time


def timestamp_to_time(timestamp):
    '''
    将时间戳转为可读格式
    '''
    time_local = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)