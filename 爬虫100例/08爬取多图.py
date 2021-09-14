import re
import requests


def download(html):
    # 通过正则匹配
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    i = 1
    for key in pic_url:
        print("开始下载图片：" + key + "\r\n")
        try:
            pic = requests.get(key, timeout=10)
        except requests.exceptions.ConnectionError:
            print('图片无法下载')
            continue
        # 保存图片路径
        dir = 'tp' + str(i) + '.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1


def main():
    url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1596723403215_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%E5%88%98%E4%BA%A6%E8%8F%B2"
    result = requests.get(url)
    download(result.text)


if __name__ == '__main__':
    main()