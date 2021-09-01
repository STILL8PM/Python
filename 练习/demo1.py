import requests
import json
import pandas as pd
url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&_t=0.5759220376658807'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

resp=requests.get(url,headers=headers)
resps=resp.json()
resps=resps["data"]
dataw=json.loads(resps)
datas=dataw["areaTree"][0]['children']
   
datas_list=[]
for i in datas:
    datas_dict={}
    datas_dict['地区名称']=i['name']
    datas_dict['新增确诊']=i['total']['nowConfirm']
    datas_dict['累计确诊']=i['total']['confirm']
    datas_dict['死亡人数']=i['total']['dead']
    datas_dict['治愈人数']=i['total']['heal']
    datas_dict['死亡率']=i['total']['deadRate']
    datas_dict['治愈率']=i['total']['healRate']
    datas_list.append(datas_dict)

df=pd.DataFrame(datas_list)
print(df)
                                                   