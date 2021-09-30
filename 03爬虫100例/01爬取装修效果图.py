import requests
import threading  # 多线程模块
import re  # 正则表达式模块
import time  # 时间模块
import os  # 目录操作模块

# 图片列表页面的数组
all_img_urls = []
# 初始化一个锁
g_lock = threading.Lock()

# 我们拼接好的图片集和列表路径
all_urls = []

# 图片地址列表
pic_links = []


class Spider():
    # 构造函数，初始化数据使用
    def __init__(self, target_url, headers):
        self.target_url = target_url
        self.headers = headers

    # 获取所有的想要抓取的 URL
    def getUrls(self, start_page, page_num):

        global all_urls
        # 循环得到URL
        for i in range(start_page, page_num+1):
            url = self.target_url % i
            all_urls.append(url)


# 生产者，负责从每个页面提取图片列表链接
class Producer(threading.Thread):

    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'HOST': 'home.fang.com'
        }
        global all_urls
        while len(all_urls) > 0:
            # 在访问all_urls的时候，需要使用锁机制
            g_lock.acquire()
            # 通过pop方法移除最后一个元素，并且返回该值
            page_url = all_urls.pop()
            # 使用完成之后及时把锁给释放，方便其他线程使用
            g_lock.release()
            try:
                print("分析"+page_url)
                response = requests.get(page_url, headers=headers, timeout=3)
                # 提取详情页地址的正则表达式，需要重新编写
                all_pic_link = re.findall(
                    '<a href="(.*?)" title=".*?" target="_blank">', response.text)
                global all_img_urls
                # 这里还有一个锁
                g_lock.acquire()
                # 这个地方注意数组的拼接，没有用 append 直接用的+=也算是 python 的一个新语法
                # 这里还需要将图片地址拼接完整
                all_img_urls += [
                    f"https://home.fang.com{link}" for link in all_pic_link]
                # print(all_img_urls)
                # 释放锁
                g_lock.release()
                time.sleep(0.5)
            except:
                pass

# 消费者


class Consumer(threading.Thread):
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'HOST': 'home.fang.com'
        }
        global all_img_urls   # 调用全局的图片详情页面的数组
        print("%s is running " % threading.current_thread)
        # print(len(all_img_urls))
        while len(all_img_urls) > 0:
            g_lock.acquire()
            img_url = all_img_urls.pop()
            g_lock.release()
            try:
                response = requests.get(img_url, headers=headers)
                # 设置案例编码
                response.encoding = 'utf-8'
                title = re.search(
                    '<title>(.*?)-房天下家居装修网</title>', response.text).group(1)
                all_pic_src = re.findall(
                    '<img src[2]?="(.*?)" onerror=".*?"/>', response.text)

                pic_dict = {title: all_pic_src}   # python字典
                global pic_links
                g_lock.acquire()
                pic_links.append(pic_dict)    # 字典数组
                print(title+" 获取成功")
                g_lock.release()

            except Exception as e:
                print(e)
            time.sleep(0.5)


class DownPic(threading.Thread):

    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'HOST': 'imgwcs3.soufunimg.com'

        }
        while True:  # 这个地方写成死循环，为的是不断监控图片链接数组是否更新
            global pic_links
            # 上锁
            g_lock.acquire()
            if len(pic_links) == 0:  # 如果没有图片了，就解锁
                # 不管什么情况，都要释放锁
                g_lock.release()
                continue
            else:
                pic = pic_links.pop()
                g_lock.release()
                # 遍历字典列表
                for key, values in pic.items():
                    path = key.rstrip("\\")
                    is_exists = os.path.exists(path)
                    # 判断结果
                    if not is_exists:
                        # 如果不存在则创建目录
                        # 创建目录操作函数
                        os.makedirs(path)

                        print(path+'目录创建成功')

                    else:
                        # 如果目录存在则不创建，并提示目录已存在
                        print(path+' 目录已存在')
                    for pic in values:
                        filename = path+"/"+pic.split('/')[-1]
                        if os.path.exists(filename):
                            continue
                        else:
                            try:
                                response = requests.get(pic, headers=headers)
                                with open(filename, 'wb') as f:
                                    f.write(response.content)
                            except Exception as e:
                                print(e)
                                pass


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'HOST': 'home.fang.com'
    }
    # 图片集和列表规则
    target_url = 'https://home.fang.com/album/s24/%d/'

    spider = Spider(target_url, headers)
    # 先测试 5 页数据
    spider.getUrls(1, 5)
    # print(all_urls)
    threads = []
    # 开启两个线程去访问
    for x in range(2):
        t = Producer()
        t.start()
        threads.append(t)

    for tt in threads:
        tt.join()

    print("进行到我这里了")

    # 开启10个线程去获取链接
    for x in range(10):
        ta = Consumer()
        ta.start()

    # 开启10个线程保存图片
    for x in range(10):
        down = DownPic()
        down.start()
