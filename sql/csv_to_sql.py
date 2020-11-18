# -*- coding: utf-8 -*-

import csv
from datetime import datetime

from app import Database

# 创建4张表的 sql 语句
# 电影的在线资料库链接
links = '''
	CREATE TABLE links(
		id INT(11) auto_increment PRIMARY KEY ,
		movieId INT(11) DEFAULT NULL ,
		imdbId INT(11) DEFAULT NULL ,
		tmdbId INT(11) DEFAULT NULL,
        INDEX(movieId)
	) ENGINE = INNODB  charset = utf8
'''

# 用户对电影评分
ratings = '''
	CREATE TABLE ratings(
		id INT(11) auto_increment PRIMARY KEY ,
		userId INT(11) DEFAULT NULL ,
		movieId INT(11) DEFAULT NULL ,
		rating FLOAT DEFAULT NULL ,
		timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
        INDEX(userId),
        INDEX(movieId),
        INDEX(rating)
	) ENGINE = INNODB charset = utf8
'''

# 用户对电影的标签
tags = '''
	CREATE TABLE tags(
		id INT(11) auto_increment PRIMARY KEY ,
		userId INT(11) DEFAULT NULL ,
		movieId INT(11) DEFAULT NULL ,
		tag VARCHAR(255) DEFAULT '' ,
		timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
        INDEX(userId),
        INDEX(movieId)
	) ENGINE = INNODB charset = utf8
'''

# 电影信息
movies = '''
	CREATE TABLE movies(
		id INT(11) auto_increment PRIMARY KEY ,
		movieId INT(11) DEFAULT NULL ,
		title VARCHAR(255) DEFAULT '' ,
		genres VARCHAR(255) DEFAULT '',
        INDEX(movieId),
        INDEX(title)
	) ENGINE = INNODB charset = utf8
'''


create_tables = [links, tags, movies, ratings]
tables = ['links', 'tags', 'movies', 'ratings']


def trans_null(reader):
    # 将数据行最后字段为空的转为0
	for line in reader:
		line[-1] = line[-1] or 0
		yield line


def trans_datetime(reader):
    # 对数据行的最后字段时间戳进行转换
	for line in reader:
		line[-1] = datetime.fromtimestamp(int(line[-1]))
		yield line


def nothing(reader):
    # 不对数据行做任何处理
	for line in reader:
		yield line


gen_datas = {
        'links': trans_null,
        'tags': trans_datetime,
        'movies': nothing,
        'ratings': trans_datetime
        }


d = Database()


def import_data(table, filename, gen_data):
	with open(filename) as f:
		reader = csv.reader(f)
		keys = next(reader)
		d.insertmany(table, keys, gen_data(reader))


def main():
    for tb in create_tables:
        d.query(tb)
        print(f'{tb} 表创建成功')
    print('开始导入数据')
    for tb in tables:
        path = f'ml-20m/{tb}.csv'
        gen_data = gen_datas[tb]
        print(f'导入 {tb} 表数据······ ')
        import_data(tb, path, gen_data)
        print(f'{tb} 表数据导入完毕')


if __name__ == '__main__':
    main()
