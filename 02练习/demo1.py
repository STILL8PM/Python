import requests
import re
url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=392402545'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
response = requests.get(url=url, headers=headers)
response.encoding = response.apparent_encoding
# re 正则表达式
html_data = re.findall('<d p=".*?">(.*?)</d>', response.text)
print(html_data)
for index in html_data:
    with open('弹幕1.txt', mode='a', encoding='utf-8')  as f:
        f.write(index)
        f.write('\n')
        print(index)
