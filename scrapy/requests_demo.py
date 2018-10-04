import requests

params = {'wd': '中国'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3519.0 Safari/537.36'
}

# parsms 接收一个字典或字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
response = requests.get('http://www.baidu.com/s', params=params, headers=headers)
# 响应内容, unicode格式
# print(response.text)

# url
print(response.url)
print(response.encoding)
print(response.status_code)

# with open('baidu.html', 'w', encoding='utf-8') as f:
#     # response.content bytes类型，未解码
#     f.write(response.content.decode('utf-8'))

# 发送post
# response.post()

# 使用代理
proxy = {
    'http': '171.14.209.180:27829'
}

# cookie
response = requests.get('http://www.baidu.com/s')
print(response.cookies)
print(response.cookies.get_dict())

# session
login_url = 'http://renren.com/PLogin.do'
data = {
    'email': '970138074@qq.com',
    'password': 'pythonspider'
}
session = requests.session()
session.post(login_url, data=data, headers=headers)
dapeng_url = 'http://www.renren.com/880151247/profile'
response = session.get(dapeng_url)
with open('renren.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# 处理不受信任的SSL证书
# verify=False