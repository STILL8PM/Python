# # 第一个爬虫示例,爬取百度页面
# import requests #导入爬虫的库，不然调用不了爬虫的函数
# response = requests.get("http://www.baidu.com") #生成一个response对象
# response.encoding = response.apparent_encoding #设置编码格式
# print("状态码:"+ str( response.status_code ) ) #打印状态码
# print(response.text)#输出爬取的信息


# # 第二个get方法实例
# import requests #先导入爬虫的库，不然调用不了爬虫的函数
# response = requests.get("http://httpbin.org/get") #get方法
# print( response.status_code ) #状态码
# print( response.text )


# # 第三个 post方法实例
# import requests #先导入爬虫的库，不然调用不了爬虫的函数
# response = requests.post("http://httpbin.org/post") #post方法访问
# print( response.status_code ) #状态码
# print( response.text )

# # 第四个 put方法实例
# import requests #先导入爬虫的库，不然调用不了爬虫的函数
# response = requests.put("http://httpbin.org/put") # put方法访问
# print( response.status_code ) #状态码
# print( response.text )

# # 第五个 get传参方法实例
# import requests #先导入爬虫的库，不然调用不了爬虫的函数
# response = requests.get("http://httpbin.org/get?name=hezhi&age=20") # get传参
# print( response.status_code ) #状态码
# print( response.text )

# # 第六个 get传参方法实例
# import requests #先导入爬虫的库，不然调用不了爬虫的函数
# data = { "name":"hezhi", "age":20}response = requests.get( "http://httpbin.org/get" , params=data ) # get传参
# print( response.status_code ) #状态码
# print( response.text )

# # 第七个 post传参方法实例
# import requests #先导入爬虫的库，不然调用不了爬虫的函数
# data = { "name":"hezhi", "age":20}response = requests.post( "http://httpbin.org/post" , params=data ) # post传参
# print( response.status_code ) #状态码
# print( response.text )

# # 第好几个方法实例
# import requests #先导入爬虫的库，不然调用不了爬虫的函数
# response = requests.get( "http://www.zhihu.com") #第一次访问知乎，不设置头部信息
# print( "第一次,不设头部信息,状态码:"+response.status_code )# 没写headers，不能正常爬取，状态码不是 200
# #下面是可以正常爬取的区别，更改了User-Agent字段
# headers = {
# "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
# }#设置头部信息,伪装浏览器
# response = requests.get( "http://www.zhihu.com" , headers=headers ) #get方法访问,传入headers参数，
# print( response.status_code ) # 200！访问成功的状态码
# print( response.text )

# # 爬取一个html并保存
# from io import FileIO
# import requests
# url = "http://www.baidu.com"
# response = requests.get( url )
# response.encoding = "utf-8" #设置接收编码格式
# print("\nr的类型" + str( type(response) ) )
# print("\n状态码是:" + str( response.status_code ) )
# print("\n头部信息:" + str( response.headers ) )
# print( "\n响应内容:" )
# print( response.text )
# #保存文件
# file = open("G:\\Gitee\\Python\\练习\\baid.html","w",encoding="utf") #打开一个文件，w是文件不存在则新建一个文件，这里不用wb是因为不用保存成二进制
# file.write( response.text )
# file.close()

# #保存百度图片到本地
# import requests #先导入爬虫的库，不然调用不了爬虫的函数
# response = requests.get("https://www.baidu.com/img/baidu_jgylogo3.gif") #get方法的到图片响应
# file = open("G:\\Gitee\\Python\\练习\\baid.gif","wb") #打开一个文件,wb表示以二进制格式打开一个文件只用于写入
# file.write(response.content) #写入文件
# file.close()#关闭操作，运行完毕后去你的目录看一眼有没有保存成功