import re
import time
import requests
import urllib
import json
from urllib import parse
from hashlib import md5
import pandas as pd

# 导入必要的库
# 创建一个data.xlsx文件 长这样

df=pd.read_excel(r'Comments\data.xlsx')

# 从源网页获取oid
origin_url='https://www.bilibili.com/video/BV1Pp4y1u7fW/'
# 请求头
header1={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}

# 正则匹配 这个是我测试过的 自己可以试一下
obj=re.compile(r'"cidMap":{"(.*?)":{',re.S)
# 请求
resp1=requests.get(url=origin_url,headers=header1)
# 获取评论的oid
oid=obj.findall(resp1.text)[0]
# print(oid) 成功
resp1.close()
# print(resp1.text)

# 前面知道 wrid=md5（Ut+ct) ct是定值
# ------------------定值--------------------- #
ct="ea1db124af3c7062474693fa704f4ff8"
# "ea1db124af3c7062474693fa704f4ff8"
# 评论需要加cookie才能拿到
header2={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Cookie":"buvid3=87AB7053-858C-6093-B4CF-4A3CD150773376912infoc; b_nut=1695788176; i-wanna-go-back=-1; b_ut=7; _uuid=4A989FC6-FFDF-B15D-1EFA-77EF610BAEB9F75574infoc; buvid_fp=a1709f14cbd2b8a5c1fef5b37aab8ea2; buvid4=8743E9DB-5F18-800A-7E83-8359CA1BF4D677562-023092712-PdJr0jKE6N5pSQNdyTYMzr8F2IhY9DzV; home_feed_column=5; CURRENT_FNVAL=4048; rpdid=0z9Zw2XHhL|NXO5GbV6|gz|3w1QLlYS; DedeUserID=476956332; DedeUserID__ckMd5=8bb8ec02cf438f22; hit-dyn-v2=1; enable_web_push=DISABLE; header_theme_version=CLOSE; LIVE_BUVID=AUTO1616989118604773; bp_video_offset_476956332=866271891190448181; PVID=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDIwMTM1NzEsImlhdCI6MTcwMTc1NDMxMSwicGx0IjotMX0.aD__KJ-pV9WBQCt-wekR6eZA-4H57XqqcmRHuRysqms; bili_ticket_expires=1702013511; SESSDATA=97586540%2C1717306372%2C74114%2Ac1CjBsSFaCHhPrjxmOj2MCE6WCS9H5hO3mzl7edFjwXxbIQNJXUNDwv9SV6_GziyWckl4SVjI3UjlJbkhhYnpXNDVYajVvbjF2YklzNVJYdUVRMUFNbVNjZUdfMks1VUduSE0xb2hGRm9QYlAweGRJVERub3ZHQmNvcW14ZEhaMEpqVU5GdzlEWTlRIIEC; bili_jct=50ae985be86cba663bdf669a8e12452c; sid=4xea3k1c; fingerprint=9d56312efc56e939901cacbfe8ab854a; b_lsid=894108A87_18C3D498EF3; bsource=search_bing; browser_resolution=1872-966",
}

# 组合参数

# ------------------请求第一页的----------------------#
# --获取wts 时间戳
wts=int(time.time())
# 第一页和剩下页的有不一样
# --获取pagination_str1
pagination_str1='{"offset":""}'
# 进行url编码
pagination_str1=urllib.parse.quote(pagination_str1)

# --------解析w_rid-------#
# 在Ut中加入三个参数
Ut1=f"""mode=3&oid={oid}&pagination_str={pagination_str1}&plat=1&seek_rpid=&type=1&web_location=1315875&wts={wts}"""
# md5加密 得到w_rid
w_rid=md5((Ut1+ct).encode()).hexdigest()
# 组合访问的网址
base_url=f'https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type=1&mode=3&pagination_str={pagination_str1}&plat=1&seek_rpid=&web_location=1315875&w_rid={w_rid}&wts={wts}'
# 进行请求
resp2=requests.get(url=base_url,headers=header2)
# print(resp2.text) 可以得到数据的

# 从第一页获取session_id 为后续页码做准备
json_data1=json.loads(resp2.text)
# 需要加上cookie才能得到seesion_id
session_id=json_data1['data']['cursor']['session_id']
# print(session_id) 拿到

# 得到一个回复列表 数据解析
replies_list=json_data1['data']['replies']
for reply in replies_list:
    msg=reply['content']['message']
    # print(msg)
    comment={
        "评论":msg,
    }
    df=df._append(comment,ignore_index=True)

# print(df) 拿到第一页的评论

# # ----------------------------解析第二页和其他页--------------------------#
# 定义一个函数，因为会重复用到
def req_other():
    # 获取wts 同理
    wts2=int(time.time())
    # --获取pagination_str2 组合pagination_str2 在这里加上session_id
    pagination_str2=r'{"offset":"{\"type\":1,\"direction\":1,\"session_id\":\"'+str(session_id)+r'\",\"data\":{}}"}'

    # 进行url编码
    pagination_str2=urllib.parse.quote(pagination_str2)

    # --------解析w_rid-------#
    Ut2=f'mode=3&oid={oid}&pagination_str={pagination_str2}&plat=1&type=1&web_location=1315875&wts={wts2}'
    # md5加密
    w_rid2=md5((Ut2+ct).encode()).hexdigest()

    base_url2=f'https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type=1&mode=3&pagination_str={pagination_str2}&plat=1&web_location=1315875&w_rid={w_rid2}&wts={wts2}'
    # print(base_url2)
    # 同理可得
    # 请求
    resp=requests.get(url=base_url2,headers=header2)
    # print(resp.text)
    json_data2=json.loads(resp.text)
    replies_list=json_data2['data']['replies']
    for reply in replies_list:
        msg=reply['content']['message']
        print(msg)
        comment={
            "评论":msg,
        }
        global df
        df=df._append(comment,ignore_index=True)
        # 解析过程一样


# # ----------------------------是否爬取其他页-----------------------------#
# 需要爬取 除第一页以外 的 页数
page=4

for i in range(page):
    print(f"-------第{i+2}页爬取完成---------")
    # 请求地址
    req_other()
    time.sleep(1) # 需要延迟一下


# 保存文件
df.to_excel(r"Comments/评论.xlsx",index=None)

# 这里我只爬取评论，没有进行爬取回复评论的评论
# 那个道理是一样的，解析数据即可
