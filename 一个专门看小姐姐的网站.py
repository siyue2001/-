import time

import requests
import parsel
import re
import os
import threading
import concurrent.futures


def get_html(url):
    """发送请求"""
    response = requests.get(url)
    return response


def create_mkdir(title):
    """创建文件加"""
    if not os.path.exists('img\\'+title):
        os.mkdir('img\\'+title)


def parse_data(data_html):
    """一次解析"""
    url_list = re.findall('<a class="entry-thumbnail" href="(.*?)" target="_blank">', data_html, re.S)
    title_list = re.findall('<a href=".*?" target="_blank"rel="bookmark">(.*?)</a>', data_html, re.S)
    return url_list, title_list


def parse_data_2(url_data):
    """二次解析"""
    selector = parsel.Selector(url_data)
    img_list = selector.css('p>img::attr(src)').getall()
    return img_list


def save_data(data, title, file_name):
    """保存数据"""
    with open("img\\" + title + '\\' + file_name, mode='wb') as f:
        f.write(data)
    print(file_name, '爬取成功！！！')


def run(url):
    """主函数"""
    data_html = get_html(url).text
    # 一次提取 详情页地址以及文件夹名称
    url_list, title_list = parse_data(data_html)
    for url_1, title in zip(url_list, title_list):
        # 创建文件加
        create_mkdir(title)
        # 请求相册页
        url_data = get_html(url_1).text
        # 二次解析数据
        img_list = parse_data_2(url_data)
        for img in img_list:
            img_data = get_html(img).content
            file_name = img.split('/')[-1]
            save_data(img_data, title, file_name)

# run('https://www.kanxiaojiejie.com/')
# for page in range(1, 86):
#     url = f'https://www.kanxiaojiejie.com/page/{page}'
#     run_thread = threading.Thread(target=run, args=(url, ))
#     run_thread.start()


start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for page in range(1, 86):
        url = f'https://www.kanxiaojiejie.com/page/{page}'
        executor.submit(run, url)

print('花费书简：', time.time()-start_time)