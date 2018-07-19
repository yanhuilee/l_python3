# -*- coding: UTF-8 -*-

import re
import time
import io
import sys
from urllib import request
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码

url = "https://www.zhihu.com/question/22918070"
html = request.urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())

# 用BeautifulSoup结合正则表达式来提取包含所有图片链接（img标签中，class=**，以.jpg结尾的链接）的语句
links = soup.find_all(
    'img', 'origin_image zh-lightbox-thumb', src=re.compile(r'.jpg$'))
# print(links)

# 设置保存图片的路径，否则会保存到程序当前路径
path = r''  # 不转义
for link in links:
    src = link.attrs['src']
    print(src, path + '%s.jpg' % time.time())
    # request.urlretrieve(src, path + r'\%s.jpg' % time.time())
