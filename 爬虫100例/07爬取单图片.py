# 简单的爬取图片，只爬取一张
import requests

# 这是一个图片的url
url = 'https://img.ithome.com/newsuploadfiles/2021/9/71d6f70e-b4f3-4530-b0b2-7da1cad892c6.jpg'
response = requests.get(url)
# 获取的文本实际上是图片的二进制文本
img = response.content
# 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
with open('爬虫100例\\a.jpg', 'wb') as f:
    f.write(img)
