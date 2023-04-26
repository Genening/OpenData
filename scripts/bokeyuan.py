"""
博客园的反爬虫机制相对微博来说较为宽松，但仍需注意不要频繁发送请求，以免被封禁IP。
下面是一个基于Python的爬虫示例，可以爬取博客园上与指定关键词相关的博客及其评论，并将结果保存为JSON文件。
请注意，这只是一个示例，实际应用中还需根据具体需求进行适当修改。
另外，为了避免被封禁IP，建议设置适当的请求间隔时间，例如在每次发送请求后暂停1秒钟。
"""

import requests
import json
import re
import time

# 设置请求头，模拟浏览器行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 定义函数，获取指定关键词的博客及其评论
def get_data(keyword):
    # 构造请求URL
    url = f'https://www.cnblogs.com/mvc/AggSite/PostList.aspx?Keywords={keyword}&PageIndex=0&AnchorId=0&_=0'
    # 发送请求
    response = requests.get(url, headers=headers)
    # 解析JSON，获取博客列表
    data = json.loads(response.text)
    entries = data['Entrylist']
    # 遍历博客列表
    for entry in entries:
        # 获取博客ID
        id = entry['PostId']
        # 获取博客标题
        title = entry['Title']
        # 获取博客内容
        content = get_content(id)
        # 获取博客评论数
        comment_count = entry['CommentCount']
        # 发送请求，获取博客评论
        comments = get_comments(id)
        # 保存结果到JSON文件中
        save_data(id, title, content, comment_count, comments)

# 定义函数，获取指定博客的内容
def get_content(id):
    # 构造请求URL
    url = f'https://www.cnblogs.com/{id}.html'
    # 发送请求
    response = requests.get(url, headers=headers)
    # 解析HTML，获取博客内容
    html = response.text
    content = re.findall(r'<div id="cnblogs_post_body" class="blogpost-body">([\s\S]*)<\/div>\s*<div class="feedback">', html)[0]
    return content

# 定义函数，获取指定博客的评论
def get_comments(id):
    # 构造请求URL
    url = f'https://www.cnblogs.com/mvc/blog/GetComments.aspx?postId={id}&blogApp=&pageIndex=0&anchorCommentId=0&_=0'
    # 发送请求
    response = requests.get(url, headers=headers)
    # 解析JSON，获取评论列表
    data = json.loads(response.text)
    comments = data['comments']
    # 将评论列表转换为标准格式
    formatted_comments = []
    for comment in comments:
        formatted_comment = {
            'user': comment['userName'],
            'text': comment['body'],
            'pub_time': comment['postTime']
        }
        formatted_comments.append(formatted_comment)
    return formatted_comments

# 定义函数，保存数据到JSON文件中
def save_data(id, title, content, comment_count, comments):
    # 构造JSON数据
    data = {
        'id': id,
        'title': title,
        'content': content,
        'comment_count': comment_count,
        'comments': comments
    }
    # 将数据保存为JSON格式
    with open(f'cnblogs_{id}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# 调用函数，获取指定关键词的博客及其评论
get_data('Python爬虫')