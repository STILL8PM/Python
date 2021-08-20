import requests
from lxml import etree

url = 'https://www.xxxx.com/page/4/'
response = requests.get(url)
html = etree.HTML(response.text)
href_list = html.xpath('//div[@class="item-title"]/a/@href')
for href in href_list:
    res = requests.get(href)
    html_data = etree.HTML(res.text)
    img_url_list = html_data.xpath('//div[@data-fancybox="gallery"]/@data-src')
    img_name_list = html_data.xpath('//img/@alt')
    print(img_url_list)
    for img_url, img_name in zip(img_url_list, img_name_list):
        result = requests.get(img_url).content
        with open('图片/' + img_name + ".jpg", "wb")as f:
            f.write(result)
            print("正在下载:", img_name)