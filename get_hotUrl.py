# encoding=utf-8

import get_cookies
import requests
import os
import csv
import urllib
import parser
import time
import json

class get_hotUrl(object):
    def __init__(self):
        self.hotUrl=[]
        self.hotTitle=[]
        self.hotDegree = []

    def get_hotUrl(self):
        return self.hotUrl

    def get_hotUrl(self,cookies):
        params = {
            #'containerid':'106003type=1'
            'containerid': '106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot',
            'title': '%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C%E6%A6%9C',
            'hidemenu': '1',
            'extparam': 'filter_type=realtimehot&mi_cid=&pos=9&c_type=30&source=ranklist&flag=2&display_time=1512031210',
            'luicode': '10000011',
            'lfid': '106003type=1',
            'featurecode':'20000320'
        }
        url_index = 'https://m.weibo.cn/api/container/getIndex'
        r = requests.get(url_index,params=params,cookies=cookies)
        j = json.loads(r.content)
        j = j['data']
        for i in range(20):
            self.hotUrl.append(j['cards'][0]['card_group'][i+1]['scheme'])
            self.hotTitle.append(j['cards'][0]['card_group'][i+1]['desc'])
            self.hotDegree.append(j['cards'][0]['card_group'][i+1]['desc_extr'])
        return self.hotUrl

    def store2csv(self,m):
        isExists = os.path.exists(m)
        if not isExists:
            os.makedirs(m)
        else:
            print("文件已经存在")
            return
        try:
            headers = ['title','url','hot_degree']
            rows=zip(self.hotTitle,self.hotUrl,self.hotDegree)
            with open('%s\\main.csv'%m,'w') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(headers)
                f_csv.writerows(rows)
                f.close()
            print("main.csv存储成功")
        except:
            os.removedirs(m)
            print("main.csv存储失败")





