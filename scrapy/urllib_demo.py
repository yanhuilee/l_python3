# ending: utf-8

from urllib import request

try:
    resp = request.urlopen('http://www.baidu.com')
except TimeoutError as e:
    raise e
finally:
    pass

print(resp.getcode())
print(resp.readline())

# 下载url
# request.urlretrieve('url', 'file')

# 编码
from urllib import parse
params = {'name': '中文', 'age': 18, 'greet': 'hi'}
result = parse.urlencode(params)
print(result)

# url = 'http://www.baidu.com/s?wd=刘德华'
# 解码 parse.parse_qs()
parse.parse_qs(result)

# url 解析（scheme host port path query-string anchor）
url = 'http://tpcsc.ibeife.com/Course/Course/Video?PurchaseProductId=558d0046&StudyPlanArrangeId=b4beba7e&CourseId=a326d579&ChapterId=cf197a4a-&SubchapterId=d57bc7c4'
result = parse.urlparse(url)  # urlsplit
print('sceme: ' + result.scheme)
print('netloc: ' + result.netloc)
print('-'*30)

# 爬虫
url = 'https://www.zhipin.com/job_detail/?query=python&scity=101010100&industry=&position='
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
req = request.Request(url, headers=headers)
resp = request.urlopen(req)
# print(resp.read().decode('utf-8'))

# 代理
try:
    proxy_url = 'http://httpbin.org/ip'
    handler = request.ProxyHandler({'http': "233.241.78.43:8081"})
    opener = request.build_opener(handler)
    resp = opener.open(url)
    print(resp.readline())
except Exception as e:
    pass
