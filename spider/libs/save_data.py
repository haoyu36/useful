
def write_to_json(path, content):
    '''
    存储为 JSON 格式的数据
    :path :文件路径
    :context :可迭代的数据对象，须为字典格式
    '''
    import json
    import os
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(path, 'a', encoding='utf-8') as f:
        for i in content:
            f.write(json.dumps(i, indent=2, ensure_ascii=False) + '\n') 


def write_to_csv(path, first_line, context):
    '''
    存储为 CSV 格式的数据
    :path :文件路径
    :first_line :每行数据标题
    :context :可迭代的数据对象，须为字典格式
    '''
    import csv
    import os
    if not os.path.exists(path):
        os.makedir(path)
    with open(path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['index', 'image', 'title', 'actor', 'time', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in context:
            writer.writerow(i)


def write_to_redis(path, key, context):
    '''
    存储到 Redis 数据库集合中
    :path :数据库路径
    :key :Redis 的键
    :context :可迭代的数据对象
    '''
    import json
    from redis import StrictRedis
    redis = StrictRedis(host='localhost', port=6379, password=None)
    for i in context:
        redis.hset(key, i['index'], json.dumps(i))


# 序列化时间
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


with open('fff.json', 'a', encoding='utf-8') as f:
    f.write(json.dumps(a, indent=2, ensure_ascii=False, default=myconverter) + '\n') 
