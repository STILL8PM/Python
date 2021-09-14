import requests
from bs4 import BeautifulSoup

URL="https://www.biqiuge.com/paihangbang/"
req=requests.get(url=URL)
req_txt=req.text
bs = BeautifulSoup(req_txt,"html.parser")
for  i in bs.find_all("div",class_="block bd"):
    print(i.text)