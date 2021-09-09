from datetime import date
#导入时间库
now=date.today()
#取当前时间
print(now)
birthday=date(1998,7,24)
print(birthday)
age=now-birthday
#假设年龄=当前日期-生日日期
print(age)