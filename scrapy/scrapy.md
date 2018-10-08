爬虫：网络请求，数据解析，数据存储，反爬虫机制（更换IP代理/设置请求头），异步请求


 
```
scrapy startproject [名称]
cd

# 开始爬取
scrapy crawl 文件名
```

settings.py
```
ROBOTSTXT_OBEY = False
```

#### pipeline 存储

中间件

#### 问题整理
Scrapy运行时出错：ImportError: No module named win32api
```
pip install pypiwin32
```