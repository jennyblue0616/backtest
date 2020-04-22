# -*- coding: utf-8 -*-
# !usr/bin/python3
import sqlite3
import datetime
import time

# 备份
def bakSqlite():
    conn = sqlite3.connect("database.db")
    with open('file.bak', "wb+") as f:
        for line in conn.iterdump():
            data = line + '\n'
            data = data.encode("utf-8")
            f.write(data)
    # 假装做这件事情需要一分钟
    time.sleep(60)

# 每天0点备份
def main(h=0, m=0):
    '''h表示设定的小时，m为设定的分钟'''
    while True:
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            if now.hour == h and now.minute == m:
                break
            # 不到时间就等20秒之后再次检测
            time.sleep(20)
        # 做正事，一天做一次
        bakSqlite()

main()