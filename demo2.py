products = [['iphone',6888],['MacPro',14800],['小米6',2499],
            ['office',31],['book',60],['nike',699]]
i=0
n=5
print('------商品列表------')
for product in products:
    if i <=n:
        print(i,product[0],product[1],end='\n')
    i+=1
index =True
shopping=[]

while index:
    choice = input('请输入要购买的商品编号:')
    if choice.isdigit():
        choice = int(choice)
        if choice>=0 and choice<len(products):
            shopping.append(products[choice])
            print('您已经添加了%s号商品到购物车'%products[choice])
        else :
            print('该商品不存在')

    elif choice == 'q':
        if len(shopping)>0:
            print('-----您已经购买以下商品-----')
            for k,shop in enumerate(shopping):
                print('%s %s %s'%(k,shop[0],shop[1]))
        index =False        
