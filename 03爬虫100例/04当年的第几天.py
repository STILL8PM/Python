str=input('请输入年-月-日： ')
year=int(str[0:4])
month=int(str[5:7])
day=int(str[7:9])
months=(0,31,59,90,120,151,181,212,243,273,304,334)
days=0
days=months[month-1]+day
if(year%4==0 and month>=2):
    days=days+1
print(days)