
import time


def timestamp_to_time(timestamp):
    '''
    将时间戳转为可读格式
    '''
    time_local = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)




# 序列化时间
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


with open('fff.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(a, indent=2, ensure_ascii=False, default=myconverter) + '\n') 

