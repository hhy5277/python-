# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/7 0007

goods = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998}
]
customer_name=''
salary=0
# 存放购买的商品
shopping_cart = []
#保存用户信息
# user_info = {}
# 登录次数
count =0


# 假设用户信息为 {'aaa': ['bbb', '1977'], 'bbb': ['bbb', '8873'], 'a': ['a', '2']}
# user_info={'a': ['a', '2']}
user_info={}
with open('my_customer_info', 'r', encoding='utf-8') as c_info:  # 取出文件中的老用户信息
    print(type(c_info),"??")
    for i in c_info:

        i = i.strip().split(',')
        user_info[i[0]] = i[1:]

while count <3:
    customer_name=input("输入用户名：").strip()
    password = input('输入密码：').strip()
    if customer_name in user_info.keys(): #判断用户是否为老用户
        # pass 如果为老用户取出余额
        # 首先判断密码是否正确
        if user_info[customer_name][0] == password:
            salary =int(user_info[customer_name][1])
            print('您的余额为   \033[1;32m   {}   \033[0m   元'.format(salary))
            break
        else: #密码不正确
            if count<2:
                print("重新输入密码")
            else:
                print("最多输入三次密码")
            count+=1
    else: #新用户
        salary = input('你是新用户，输入工资：').strip()
        if salary.isdigit():
            salary = int(salary)
            user_info[customer_name]=[password,salary]
            #print(user_info)
            break
        else:
            print('工资必须是数字')



while count != 3:  #count 不等于3 表示登录成功了
    for idx, item in enumerate(goods):  #enumerate化
        print(idx + 1, item['name'], item['price'])

    id_of_buy = input('请输入您想购买商品的序号（c:查账单，q:退出）：')
    if id_of_buy.isdigit() and int(id_of_buy) <= len(goods): #如果是序号 且小于商品长度
        if goods[int(id_of_buy) - 1 ].get("price")<salary :
            salary -=goods[int(id_of_buy) - 1 ].get("price")
            shopping_cart.append(goods[int(id_of_buy) - 1])
            buy_history_info="#" + customer_name + '购买' + goods[int(id_of_buy) - 1][
                'name'] + '花费' + str(goods[int(id_of_buy) - 1]['price'])
            # a 打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
            with open('my_buying_history', 'a', encoding='utf-8') as buy_info:  # 记录消费记录
                buy_info.write(buy_history_info + '\n')
            print('商品 ：\033[1;32m  {}  \033[0m   已加入到购物车！'.format(goods[int(id_of_buy) - 1]['name']))
        else:
            print("余额不够")

    elif id_of_buy == 'q': #退出
        print('您的余额为  \033[1;31m  {}  \033[0m  '.format(salary))
        if len(shopping_cart) > 0:  # 购买商品才会打印购买信息
            print('您本次已购买商品：')
            for idx, item in enumerate(shopping_cart):
                print(idx + 1, item['name'], item['price'])
        else:
            print('未购买商品！')
        user_info[customer_name][1] = str(salary)  #更新用户余额
        # w 打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
        with open('my_customer_info', 'w', encoding='utf-8') as w_info:  # 退出时更新用户信息
            for i in user_info.keys():
                w_info.write(i + "," + ','.join(user_info[i]) + '\n')
        break
    elif id_of_buy == 'c': #查看账单
        # r 只读模式
        with open('my_buying_history', 'r', encoding='utf-8') as f_buy:
            for k in f_buy: #按行读
                if customer_name in k:
                    print(k.strip())
    else:
        print('请输入正确的商品编号！')
