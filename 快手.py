"""
@author: 巳月
@file: 快手.py
@time: 2021/8/26 20:02
"""
"""
课题：爬快手短视频

课程时间：20:07开始

讲师：巳月老师

知识点：
    requests
    json
    re
    pprint

环境：
    python3.6+pycharm

课后的回放录播资料找助理老师：python10010

+python安装包 安装教程视频  anaconda等等 安装包
+pycharm社区版   专业版 及 激活码免费
"""


import json
import requests
import re
from pprint import pprint

# url = 'https://www.kuaishou.com/search/video?searchKey=慢摇'
url = 'https://www.kuaishou.com/graphql'

headers = {
    # Content-Type的格式有四种(对应data)：分别是
    # application/x-www-form-urlencoded（这也是默认格式）: 只需要将请求的参数构造成一个字典，然后传给requests.post()的data参数即可。
    # application/json: 格式的请求头是指用来告诉服务端post过去的消息主体是序列化后的 JSON 字符串。
    # text/xml: 把xml作为一个文件来传输
    # multipart/form-data: 用于文件上传

    'content-type': 'application/json',
    'Cookie': 'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_721a784b472981d650bcb8bbc5e9c9c2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
keyword = input('请输入你要搜索的关键字：')

for i in range(0, 10):
    print(f'--------------------正在爬取第{i+1}页--------------------')
    data = {
        'operationName': "visionSearchPhoto",
        'query': "query visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        photoUrl\n        liked\n        timestamp\n        expTag\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n",
        'variables': {
            'keyword': keyword,
            'pcursor': str(i),
            'page': "search",
            'searchSessionId': "MTRfMjcwOTMyMTQ2XzE2Mjk5ODcyODQ2NTJf5oWi5pGHXzQzMQ"
        }
    }
    # json数据交换格式,在JSON出现之前，大家一直用XML来传递数据
    # 由于各个语言都支持 JSON ，JSON 又支持各种数据类型，所以JSON常用于我们日常的 HTTP 交互、数据存储等。
    # 将python对象编码成Json字符串
    data = json.dumps(data)
    json_data = requests.post(url, headers=headers, data=data).json()
    data_list = json_data['data']['visionSearchPhoto']['feeds']
    for data in data_list:
        # 提取标题
        title = data['photo']['caption']
        new_title = re.sub(r'[\/:*?"<>|\n\\]', '_', title)
        url_list = data['photo']['photoUrls']
        # pprint(url_list)
        for url_1 in url_list:
            # 只取一个地址，忽略备用地址
            if url_1['cdn'] != 'v2.kwaicdn.com':
                resp = requests.get(url_1['url']).content
                with open('./video/'+new_title+'.mp4', mode='wb') as f:
                    f.write(resp)
                print(new_title, '爬取成功！！！')