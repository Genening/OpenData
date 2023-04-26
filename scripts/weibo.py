"""
微博的反爬虫机制比较严格，需要使用一些技巧来避免被封禁IP。
下面是一个基于Python的爬虫示例，可以爬取微博上与指定关键词相关的微博及其评论，并将结果保存为JSON文件。
在上述代码中，我们使用正则表达式从HTML中提取微博及其评论的相关信息，并使用Python内置的json模块将结果保存为JSON文件。
需要注意的是，由于微博的反爬虫机制比较严格，我们需要使用一些技巧来避免被封禁IP，例如间隔一段时间发送请求，或使用代理IP等。
"""
import requests
import json
import re
import time

# 设置请求头，模拟浏览器行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 定义函数，获取指定关键词的微博及其评论
def get_data(keyword):
    # 构造请求URL
    url = f'https://s.weibo.com/weibo?q={keyword}&typeall=1&suball=1&timescope=custom:2023-04-01-0:2023-04-30-23&Refer=g'
    # 发送请求
    response = requests.get(url, headers=headers)
    # 解析HTML，获取微博列表
    html = response.text
    cards = re.findall(r'<div class="card-wrap" mid="(.*?)">.*?<\/div>\s+<\/div>\s+<\/div>', html, re.DOTALL)
    # 遍历微博列表
    for card in cards:
        # 获取微博ID
        mid = card.split('"')[1]
        # 获取微博内容
        text = re.findall(r'<p class="txt">(.*?)<\/p>', card, re.DOTALL)[0]
        # 获取微博发布时间
        pub_time = re.findall(r'<p class="from">.*?<a.*?>(.*?)<\/a>', card, re.DOTALL)[0]
        # 获取微博评论数
        comment_count = re.findall(r'<span class="line S_line1">(.*?)<\/span>', card, re.DOTALL)[0]
        # 发送请求，获取微博评论
        comments = get_comments(mid)
        # 保存结果到JSON文件中
        save_data(mid, text, pub_time, comment_count, comments)

# 定义函数，获取指定微博的评论
def get_comments(mid):
    # 构造请求URL
    url = f'https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page=1'
    # 发送请求，获取评论页数
    response = requests.get(url, headers=headers)
    html = response.text
    total_pages = int(re.findall(r'"total":(\d+)', html)[0])
    # 遍历评论页
    comments = []
    for page in range(1, total_pages+1):
        # 发送请求，获取评论列表
        url = f'https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page}'
        response = requests.get(url, headers=headers)
        html = response.text
        items = re.findall(r'<div class="list_li S_line1 clearfix"(.+?)<\/div>\s+<\/div>', html, re.DOTALL)
        # 遍历评论列表
        for item in items:
            # 获取评论用户
            user = re.findall(r'<a.*?nick-name="(.*?)".*?>', item, re.DOTALL)[0]
            # 获取评论内容
            text = re.findall(r'<div class="WB_text.*?>(.*?)<\/div>', item, re.DOTALL)[0]
            # 获取评论时间
            pub_time = re.findall(r'<div class="WB_from S_txt2">(.*?)<\/div>', item, re.DOTALL)[0]
            # 将评论添加到列表中
            comments.append({'user': user, 'text': text, 'pub_time': pub_time})
        # 间隔一段时间，避免被封禁IP
        time.sleep(1)
    return comments

# 定义函数，保存数据到JSON文件中
def save_data(mid, text, pub_time, comment_count, comments):
    # 构造JSON数据
    data = {
        'mid': mid,
        'text': text,
        'pub_time': pub_time,
        'comment_count': comment_count,
        'comments': comments
    }
    # 将数据保存为JSON格式
    with open(f'weibo_{mid}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# 调用函数，获取指定关键词的微博及其评论
get_data('Python爬虫')