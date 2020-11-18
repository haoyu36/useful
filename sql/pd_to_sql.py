# -*- coding: utf-8 -*-

'''
通过pandas将csv写入mysql
文档:http://pandas.pydata.org/pandas-docs/stable/io.html#sql-queries
'''


from glob import glob
import os.path
import pandas as pd
from sqlalchemy import create_engine


# 连接数据库
engine = create_engine('mysql+pymysql://root:root@localhost:3306/movies3')


def csv_to_mysql(path):
    df = pd.read_csv(path, sep=',')
    file_name = os.path.splitext(os.path.split(path)[1])[0]
    # 将新建的DataFrame储存为MySQL中的数据表，不储存index列
    df.to_sql(file_name, engine, chunksize=1000,
              if_exists='replace', index=False)
    print("Write {} to MySQL successfully!".format(file_name))


if __name__ == '__main__':
    csv_files = glob('ml-20m/*.csv')
    for path in csv_files:
        csv_to_mysql(path)
