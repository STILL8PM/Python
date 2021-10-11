import requests
from bs4 import BeautifulSoup
import urllib
from lxml import etree
r=requests.get("https://creator.douyin.com/creator-micro/content/manage")
r.encoding=r.apparent_encoding
text=r.text                                                                                     
print(text)