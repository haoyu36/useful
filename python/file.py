'''
常用的文件操作
'''

import os
import time
from pathlib import Path


path = '.'


# =================
# 获取目录列表
# =================


# 以列表的方式返回目录中所有的文件和文件夹
os.listdir(path)

# 返回一个迭代器包含目录中所有的对象，对象包含文件属性信息
with os.scandir(path) as entries:
    for entry in entries:
        print(entry.name)

# iterdir 方法返回一个迭代器包含目录中所有的对象，对象包含文件属性信息
for entry in Path(path).iterdir():
    print(entry.name)


# =================
# 获取目录中文件或目录
# =================

for entry in os.listdir(path):
    # if os.path.isdir(entry):
    if os.path.isfile(entry):
        print(entry)


with os.scandir(path) as entries:
    for entry in entries:
        # if entry.is_dir():
        if entry.is_file():
            print(entry.name)


for entry in Path(path).iterdir():
    # if entry.is_dir():
    if entry.is_file():
        print(entry.name)



# =================
# 获取文件属性
# =================


info = os.stat('config.py')
print(info.st_size)    # 文件大小，以字节为单位
print(info.st_mtime)    # 最近修改的时间
print(info.st_ctime)    # 创建的时间


with os.scandir(path) as entries:
    for entry in entries:
        info = entry.stat()
        print(info.st_mtime)
        print(info.st_size)


for entry in Path(path).iterdir():
    info = entry.stat()
    print(info.st_mtime)
    print(info.st_size)



# =================
# 遍历目录
# =================


# 使用 os 模块
def print_dir_contents(path):
    for child in os.listdir(path):
        child_path = os.path.join(path, child)
        if os.path.isdir(child_path):
            print_dir_contents(child_path)
        else:
            print(child_path)


for root, dirs, files in os.walk(path):
    for file in files:
        print(os.path.join(root, file))


def print_dir_contents2(path):
    for entry in os.scandir(path):
        if entry.is_dir():
            print_dir_contents2(entry.path)
        else:
            print(entry.path)




# =================
# 其他
# =================


def get_tree_size(path):
    '''返回当前目录和所有子目录下所有文件大小'''
    total = 0
    for entry in os.scandir(path):
        try:
            is_dir = entry.is_dir(follow_symlinks=False)
        except OSError as error:
            print('Error calling is_dir():', error, file=sys.stderr)
            continue
        if is_dir:
            total += get_tree_size(entry.path)
        else:
            try:
                total += entry.stat(follow_symlinks=False).st_size
            except OSError as error:
                print('Error calling stat():', error, file=sys.stderr)
    return total

