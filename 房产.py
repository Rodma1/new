# coding:utf-8
# 获取第二个连接
import requests
import json
from lxml import html
import re

etree = html.etree
import pandas as pd
from tqdm import tqdm
import time
import json
import jsonpath

headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'

}
#初始化id,为接下来判断是否是最后一页做准备
def id_init(data_month=6,data_day=1,page=1):
    url = 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=105&date=2021-0{}-{}&page={}'.format(data_month,data_day,page)
    response = requests.get(url, headers=headers)
    # dict=response.content.decode('utf-8')
    dict = response.text
    dict = dict.replace("'", '"').replace('sum', '"sum"').replace('list', '"list"').replace('id', '"id"') \
        .replace('columnName', '"columnName"').replace('columnLink', '"columnLink"').replace('time', '"time"') \
        .replace('title', '"title"').replace('desc', '"desc"')
    dict = dict.replace('"title"Link', '"titleLink"')
    dict = json.loads(dict)
    sum = jsonpath.jsonpath(dict, '$..sum')
    if sum[0] == '':
        return 0
    ids = jsonpath.jsonpath(dict, '$..id')
    id = ids[0]
    return id

def hexvn(data_month=6,data_day=1,page=1,id=0):
    labels = []
    contents = []
    url = 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=105&date=2021-0{}-{}&page={}'.format(data_month,data_day,page,id)
    print(url)
    response = requests.get(url, headers=headers)
    # dict=response.content.decode('utf-8')
    dict = response.text
    dict = dict.replace("'", '"').replace('sum', '"sum"').replace('list', '"list"').replace('id', '"id"') \
        .replace('columnName', '"columnName"').replace('columnLink', '"columnLink"').replace('time', '"time"') \
        .replace('title', '"title"').replace('desc', '"desc"')
    dict = dict.replace('"title"Link', '"titleLink"')
    dict = json.loads(dict)
    title_list = jsonpath.jsonpath(dict, '$..title')
    ids = jsonpath.jsonpath(dict, '$..id')
    if id == int(ids[0]):
        print('2021-0{}-{}的数据爬取完毕'.format(i, j))
        return 0

    hrefs = jsonpath.jsonpath(dict, '$..titleLink')

    for url in tqdm(hrefs, total=len(hrefs), desc='内容'):
        # response = requests.get(url.replace("edu.people.com.cnhttp", "121.18.212.135"), headers=headers)
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.content.decode("gbk", "ignore"))
        content_list = html.xpath(
            "/html/body/div/div/div/div/p/text()")  # //*[@id='artibody']/p/font/text()
        # print(content_list)
        content = "".join(content_list).replace(' ', '') # \n\t\n
        print(content)
        labels.append('房产')
        contents.append(content)  # 追加#这样就获取到了一条数据，最加到content里面
    temp = pd.DataFrame()
    temp['label'] = labels
    temp['title'] = title_list  # Datefram存入的是列表格式
    temp['href'] = hrefs
    temp['content'] = contents
    temp.to_csv(r"房产新闻.csv", index=None, header=None, mode='a+', encoding="utf-8")
    print('已经存储{}条数据成功'.format(len(contents)))
    print('第{}页爬取完毕'.format(page))
    return int(ids[0])




for i in range(6):#月份
    for j in range(31):#天数
        print('第{}天'.format(j+1))
        # # 初始化id
        # id = id_init(data_month=i + 1, data_day=j + 1, page=k + 1)
        # print(int(id))
        id = 33
        for k in range(15):#页数

            # hexvn(page=1)
            ids=hexvn(data_month=i+1,data_day=j+1,page=k+1,id=int(id))
            id = ids
            if ids == 0:
                break

