# -*- coding: utf-8 -*-

import os
import glob
import shutil


def category_photo(path):
    '''
    将目录下的 jpeg 图片和 NEF 图片分类
    '''
    jpeg_dir = os.path.join(path, 'jpeg')
    raw_dir = os.path.join(path, 'raw')

    if not os.path.exists(jpeg_dir):
        os.mkdir(jpeg_dir)
    if not os.path.exists(raw_dir):
        os.mkdir(raw_dir)

    for i in glob.glob(os.path.join(path, '*.jpeg')):
        shutil.move(i, jpeg_dir)
    for i in glob.glob(os.path.join(path, '*.NEF')):
        shutil.move(i, raw_dir)


if __name__ == '__main__':
    path = r'/Users/zhaohaoyu/Pictures/test'
    category_photo(path)