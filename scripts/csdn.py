"""
与知乎网站类似，反爬虫机制比较严格，为了避免被封杀，我们在编写爬虫的过程中，需要注意以下几点：
设置随机User-Agent，模拟浏览器行为，避免被检测到是爬虫。
控制请求频率，不要过于频繁地请求，否则容易被封。
使用代理IP，避免同一IP地址过于频繁地请求。
下面是一个基于Python的爬虫示例，可以爬取指定关键词的问题及其答案
需要注意的是，CSDN的答案是存储在问题详情页中的，因此需要发送请求获取详情页的HTML，并解析HTML获取答案列表。
"""

import requests
import json
from lxml import etree

# 设置请求头，模拟浏览器行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
# 设置代理IP
proxies = {'https': 'https://111.177.174.117:9999'}

# 定义函数，获取指定关键词的问题和答案
def get_data(keyword):
    # 构造请求URL
    url = f'https://so.csdn.net/so/search/s.do?q={keyword}&t=&u='
    # 发送请求
    response = requests.get(url, headers=headers, proxies=proxies)
    # 解析HTML
    html = etree.HTML(response.text)
    # 获取问题列表
    items = html.xpath('//dl[@class="search-list J_search"]/dd')
    # 遍历问题列表
    for item in items:
        # 获取问题标题
        title = item.xpath('.//a[@class="title"]/text()')[0]
        # 获取问题链接
        link = item.xpath('.//a[@class="title"]/@href')[0]
        # 发送请求，获取问题详情页的HTML
        response = requests.get(link, headers=headers, proxies=proxies)
        # 解析HTML，获取答案列表
        html = etree.HTML(response.text)
        answers = html.xpath('//div[@class="htmledit_views"]/text()')
        # 保存结果到JSON文件中
        save_data(title, link, answers)

# 定义函数，保存数据到JSON文件中
def save_data(title, link, answers):
    # 构造JSON数据
    data = {
        'question': title,
        'link': link,
        'answers': answers
    }
    # 将数据保存为JSON格式
    with open(f'csdn_{title}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# 调用函数，获取指定关键词的问题和答案
get_data('Python爬虫')