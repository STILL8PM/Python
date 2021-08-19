import requests
url="https://item.jd.com/100019888212.html"
try:
    kv = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "cookie": "8ipiu591lktf4so07w5be3rp730lxbs6" #cookie信息每个人都不同，需登录到京东网站，通过浏览器查看cookie信息
    }
    r = requests.get(url, headers = kv) 
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text[:1000])
except:
    print("爬取失败")


