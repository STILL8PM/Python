# -*- coding: UTF-8 -*-
import os
import json
import chardet
import logging
import requests
from tqdm import tqdm
from fake_useragent import UserAgent

# 随机产生请求头
ua = UserAgent(verify_ssl=False, path='fake_useragent.json')

# 日志输出的基本配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 创建一个文件夹
path = 'h:/极简壁纸'
if not os.path.exists(path):
    os.mkdir(path)


# 随机切换请求头
def random_ua():
    headers = {
        "user-agent": ua.random
    }
    return headers


# 获取图片url
def get_imgae_url(url, start, display):
    # cid=6代表《美女模特》页面
    param = {
        'cid': '6',
        'start': start,
        'count': '30'
    }
    response = requests.get(url=url, headers=random_ua(), params=param)
    # 自动转换编码，与网页一致
    response.encoding = chardet.detect(response.content)['encoding']
    # 获取页面内容
    response = response.text
    # 将内容转换成json格式
    data_s = json.loads(response)
    # 提取data里的数据
    a = data_s["data"]
    # 定义一个空列表，用来放图片url
    url_list = []
    for i in range(len(a)):
        # 提取其中key值为"img_1280_800"的数据（提取其它的类似数据也一样）
        data = a[i].get("img_1280_800", "not exist")
        # 切割字符串
        b = data.split('/')
        # 将图片改为想要设置的格式
        b[4] = '{}_100'.format(display)
        # 拼接字符串，得到图片url
        image_url = '/'.join(b)
        url_list.append(image_url)
    return url_list


# 下载图片
def download_image(url):
    num = 1
    logging.info('您的需求我已经收到啦，很快就能帮你完成嗷，请稍等一会会。。。。')
    for i in tqdm(range(len(url))):
        image_url = url[i]
        image_data = requests.get(url=image_url, headers=random_ua()).content
        image_name = '{}.png'.format(num)
        save_path = path + '/' + image_name
        with open(save_path, 'wb') as f:
            f.write(image_data)
        num += 1
    logging.info('任务已完成！感谢您的使用！')


def main():
    url = 'http://www.jijianzy.com/bz/api.php?'
    page = input('请输入您想要爬取的页数：')
    display = input('请输入您想要的图片分辨率（格式为1920_1080）：')
    page = int(page) + 1
    start = 0  # 起步为0，每一组图片加30
    url_list_s = []  # 定义一个空列表装url
    for m in range(1, page):  # 多页下载
        url_list = get_imgae_url(url, start, display)
        url_list_s += url_list
        start += 30
    download_image(url_list_s)


if __name__ == '__main__':
    main()
