

import requests

from time import sleep
import json
import random
import pymysql

FILE = '/Volumes/Elements/py练习题/高级爬虫实战/代码/Proxy-IP.txt'  # 读取的txt文件路径

db = pymysql.connect("localhost", "root", "12345678", charset="utf8")
cursor=db.cursor()
cursor.execute('use  知乎数据库信息;')

def intosql(id,authorName,userDesc,comment,quesHead,vateup_count):
    print(id,authorName,userDesc,comment,quesHead,vateup_count)
    print('准备保存数据库')
    s_insert = "insert into zhihu(作者编号,用户名,用户描述,评论数,问题标题,点赞数)values('%s','%s','%s','%d','%s','%d');"% (id,authorName,userDesc,comment,quesHead,vateup_count)


    cursor.execute(s_insert)
    # 提交
    db.commit()
    print('已保存入数据库')



# 获取代理IP
def proxy_ip():
    ip_list = []
    with open(FILE, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            ip_list.append(line.strip())
    ip_port = random.choice(ip_list)
    return ip_port



#  要爬取的数据的url
intourl='https://www.zhihu.com/api/v3/feed/topstory/recommend'

def pageurl(num):
    # 调用 随机的一个 代理port
    port =proxy_ip()
    # 绑定 一个 代理
    proxies = {"HTTP":port}
    #  要发送的get参数
    params={
    "desktop":"true",
    "limit":"7",
    "action":"down",
    "after_id":str(num),
    }
    #  请求头  最后弄一个  随机的请求头  ，没回发送的都不一样
    headers = {"User-Agent":"Mozilla5.0"}

    html=requests.get(url=intourl,headers=headers,cookies={'cookies':'_zap=de88f2b0-bb59-4611-9816-63c98cad23ff; d_c0="AACm7Ep_Rg6PTufqUu1hInGoN1GzBlmKyGU=|1538029158"; l_cap_id="ZDI3MzM3MWE2N2IwNDkzZWI3YzE4N2YwZjNhZTZmNTU=|1538123550|102d8fea7811471e3b6bbe7d836acb7e5e9a3dd1"; r_cap_id="YmNjMGY0N2Y3M2I2NDc0Y2ExY2MzZWQ3ODg5MDRkOTM=|1538123550|ee0a4f1345606febc7a9b7ac41cb77c8a0eb9640"; cap_id="MmQzZDIyMTNhZGYyNGY0Njg2Y2UyODIzZGYyYzU0OWI=|1538123550|fb1ab582f1cbfec404c289d0812e9877fedcb249"; q_c1=1f6dba22a2764dab9da9b8fbc90b4c86|1539053123000|1539053123000; _xsrf=aa7mXxSgJoqpZWViWL1Xc0c7TC8FRpNv; tst=r; capsion_ticket="2|1:0|10:1539397270|14:capsion_ticket|44:YWQwNjI2ZmI1ZjNiNGUyZjk5MTQ0ZmRlNjJiMTJlYmE=|5f82870bd4da1eb7ef6e55e6b4a12ce9d29db27b077604f63a00578a81519fa1"; z_c0="2|1:0|10:1539397272|4:z_c0|92:Mi4xUHdyU0F3QUFBQUFBQUtic1NuOUdEaVlBQUFCZ0FsVk5tS1N1WEFDUDJxUHJNYjBZWDRnejNjUVhVV2dSWGlSbjRR|52503e5426077c3a94e620346941702ba852a813c9848cf2a54a0aefdb98cabb"; tgw_l7_route=9553ebf607071b8b9dd310a140c349c5'},
                      params=params,proxies=proxies)
    html.encoding='utf-8'
    html=html.text
    sleep(1)
    #   将得到的json 数据 转换为 python 字典的数据
    pythonstr=json.loads(html)

    pythonstr['data'].pop()

    # 得到的字典，取出数据
    for x in pythonstr['data']:



        # 取姓名和标题等信息的键值对
        nameAndTitle = x['target']['author']

        id=x['id']
        authorName=nameAndTitle['name']
        userDesc=nameAndTitle['headline']
        comment = x['target']['comment_count']  # 评论数
        quesHead=x['target']['question']['title']
        vateup_count = x['target']['voteup_count']


        #print('_id:',id,'用户名：',authorName,'用户描述：', userDesc, '评论数：',comment, x['target']['excerpt'],
              #'问题标题：',quesHead, '点赞数:',vateup_count)
        comment=int(comment)
        vateup_count=int(vateup_count)

        intosql(id,authorName,userDesc,comment,quesHead,vateup_count)





x = -1
 # "after_id":str(num)  等于这个值



 # 循环读取下一页的json数据
while True:

    try:
        # 调用爬取函数
        pageurl(x)
        x += 7

    except:
        # 如果报错的话 就从这个跳过去
        continue

    # x['voteup_count'],, x['title']
    # print(x['excerpt'])




