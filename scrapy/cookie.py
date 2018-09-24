from urllib import request, parse

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# cookie
from http.cookiejar import CookieJar
cookiejar = CookieJar()
handler = request.HTTPCookieProcessor(cookiejar)
opener = request.build_opener(handler)
data = {
    'email': '970138074@qq.com',
    'password': 'pythonspider'
}
login_url = 'http://renren.com/PLogin.do'
req = request.Request(login_url, data=parse.urlencode(
    data).encode('utf-8'), headers=headers)
# 登录,
opener.open(req)
# 个人主页
dapeng_url = 'http://www.renren.com/880151247/profile'
# resp = opener.open(dapeng_url)
req = request.Request(dapeng_url, headers=headers)
resp = opener.open(req)
with open('renren.html', 'w', encoding='utf-8') as f:
    f.write(resp.read().decode('utf-8'))
