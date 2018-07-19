# -*- coding: UTF-8 -*-

import io
import sys
from urllib import request
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码

# 构造头文件，模拟浏览器访问
url = "http://www.jianshu.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
page = request.Request(url, headers=headers)
page_info = request.urlopen(page).read().decode(
    'utf-8', 'ignore')  # .replace(u'\u2713', u'')

# 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
soup = BeautifulSoup(page_info, "html.parser")
# 以格式化的形式打印html
# print(soup.prettify())

titles = soup.find_all('a', 'title')

# 打印查找到的每一个a标签的string和文章链接
for title in titles:
    print('《', title.string, '》', url, title.get('href'))

# open()是读写文件的函数,with语句会自动close()已打开文件
with open("/xx", 'w') as file:
    for title in titles:
        file.write(title.string + '\n')
        file.write(url + title.get('href') + '\n\n')
