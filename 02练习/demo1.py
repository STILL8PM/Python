from urllib import request,parse

from requests.models import Response
from requests.sessions import RequestsCookieJar
url = 'http://httpbin.org/'

# 请求头设置
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    'Host': 'httpbin.org' 
}
# 参数设置
dict = {
    'name': 'Germey'
}
data = bytes(parse.urlencode(dict),encoding='utf8')
Response = request.Request(url=url,data=data,headers=headers,method='post')
Response = request.urlopen(Response)
print(Response.read())

