import requests

# 请求头字典
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}
# 在get请求内，添加user-agent
response = requests.get(url='https://www.zhihu.com/explore', headers=headers)
print(response.status_code)  # 200
print(response.text)
with open('爬虫100例\zhihu.html', 'w', encoding='utf-8') as f:  #创建一个zhihu.html文件
    f.write(response.text)
