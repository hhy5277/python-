# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/11 0011


"""
简单的员工信息增删改查程序
表信息
1,Alex Li,22,13651054608,IT,2013‐04‐01
2,Jack Wang,28,13451024608,HR,2015‐01‐07
3,Rain Wang,21,13451054608,IT,2017‐04‐01

增加
add staff_table Alex Li,25,134435344,IT,2015-10-29
以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id需自增

查询支持三种语法
find name,age from staff_table where age > 22
find * from staff_table where dept = "IT"
find * from staff_table where enroll_date like "2013"

删除指定员工信息纪录
del from staff_table where dept = "IT"

更新记录
update staff_table set dept="Market" where dept = "IT"
update staff_table set age=25 where name = "Alex Li"
"""

from tabulate import tabulate
import os

STAFF_DB = "my_staff.db"  # 数据文件的路径名称
COLUMN_ORDERS = ['id', 'name', 'age', 'phone', 'dept', 'enrolled_date']  # 定义数据的位置关系


def load_db():
    """
    加载 STAFF_DB 文件中的数据 转化成我们设计好的数据格式并返回
    :return:
    """

    staff_data = {}
    # 构建字典空列表
    # {'id': [],'name':[],'age': [],'phone':[],'dept':[],'enrolled_date'[]
    for d in COLUMN_ORDERS:
        staff_data[d] = []

    with open(STAFF_DB, 'r', encoding='utf-8') as f:
        for line in f:
            staff_datas = line.split(",")
            # 构建员工信息字典
            for ind, d in enumerate(staff_datas):
                staff_data[COLUMN_ORDERS[ind]].append(d.strip())  # 去掉末尾回车

    return staff_data


def save_db():
    """
    把内存数据保存在数据文件中
    :return:
    """
    with open("%s.new" % (STAFF_DB), "w", encoding="utf-8") as f:
        for index, staff_id in enumerate(STAFF_DATA["id"]):
            row = []
            for col in COLUMN_ORDERS:
                row.append(STAFF_DATA[col][index])
            f.write(",".join(row) + "\n")

    os.remove(STAFF_DB)
    os.rename("%s.new" % (STAFF_DB), STAFF_DB)


def print_log(msg, msg_type='info'):
    if msg_type == 'error':
        print("\033[31;1mError:%s\033[0m" % msg)
    else:
        print("\033[32;1mInfo:%s\033[0m" % msg)


#  ---定义根据find/delete/update/add  语句和返回的数据 处理返回列--
def syntax_find(query_clause, match_data):
    # find name, age from staff_table where age > 22
    """
    :param query_clause:  eg. find age,name from staff_table
    :param match_data:
        内存中STAFF_DATA数据格式z
        {'id': [],'name':[],'age': [],'phone':[],'dept':[],'enrolled_date'[]
        转化成matched_data的格式
        [['3', 'Rain Wang', '21', '13451054608', 'IT', '2017-04-01']]
    :return:
    """

    # 首先过滤出字段
    filter_keys = query_clause.split("find")[1].split("from")[0]
    filter_keys_final = [i.strip() for i in filter_keys.split(",")]

    # 然后判断是否有*
    if "*" in filter_keys_final:
        if len(filter_keys_final) == 1:
            filter_keys_final = COLUMN_ORDERS  # 返回全部字段
        else:
            print_log("*不能同时与其它字段出现", "error")
            return False

    elif len(filter_keys_final) == 1:  # 相当于find  where中间是空字符串 导致filter_keys_final ==[ "  "]
        if not filter_keys_final[0]:  # 如果是空字符串
            print_log("语法错误，find和from之间必须跟字段名或*", "error")
            return False
    elif len(filter_keys_final) >= 1:
        for key in filter_keys_final:
            if key not in COLUMN_ORDERS:
                print_log("语法错误，字段%s错误,可选字段%s" % (key, COLUMN_ORDERS), "error")
                return False

    filtered_data = []

    for row in match_data:
        print(row, "???BBB")
        eachrow = []
        for col in filter_keys_final:
            col_index = COLUMN_ORDERS.index(col)
            eachrow.append(row[col_index])
        filtered_data.append(eachrow)
    print(tabulate(filtered_data, headers=filter_keys_final, tablefmt="grid"))


def syntax_add(query_clause, match_data):
    """

    :param query_clause: eg：add staff_table lxm,25,134435344,IT,2015-10-29
    :param match_data:
        内存中STAFF_DATA数据格式z
        {'id': [],'name':[],'age': [],'phone':[],'dept':[],'enrolled_date'[]
        转化成matched_data的格式
        [['3', 'Rain Wang', '21', '13451054608', 'IT', '2017-04-01']]
    :return:
    """
    # add staff_table lxm,25,134435344,IT,2015-10-29

    # 得到增加的值列表
    add_data = [col.strip() for col in query_clause.split("staff_table")[-1].split(',')]
    phone_ind = COLUMN_ORDERS.index("phone")  # 得到手机所在列
    if (len(COLUMN_ORDERS) - 1 == len(add_data)):
        # 得到最后一行数据，自增长最后一行 数据Id最大
        max_id = match_data[-1][0]  # 最后一行id
        # 自增长ID
        max_id = int(max_id) + 1
        # 把ID插入到第一列
        add_data.insert(0, str(max_id))
        phone_val = add_data[phone_ind]
        # 判断手机号是否重复
        if not (phone_val in STAFF_DATA["phone"]):
            # 把数据插入到STAFF_INFO
            for index, col in enumerate(COLUMN_ORDERS):
                STAFF_DATA[col].append(add_data[index])

            save_db()
            print(tabulate(STAFF_DATA, headers=COLUMN_ORDERS))
            print_log("成功添加1条纪录到staff_table表")
        else:
            print_log("手机号%s重复" % phone_val, 'error')

    else:
        print_log("语法错误，列数不对,必须字段%s：" % COLUMN_ORDERS[1:], "error")


def syntax_update(query_clause, match_data):  # 要求修改一项数据
    """

    :param query_clause: update staff_table set dept = 开发部 where age = 22
    :param match_data:
        内存中STAFF_DATA数据格式
        {'id': [],'name':[],'age': [],'phone':[],'dept':[],'enrolled_date'[]
        转化成matched_data的格式
        [['3', 'Rain Wang', '21', '13451054608', 'IT', '2017-04-01']]
    :return:
    """

    if "set" in query_clause:
        formula_str = query_clause.split("set")
        col_name, new_val = [i.strip() for i in formula_str[-1].strip().split('=')]
        for row in match_data:  # 格式[['3', 'Rain Wang', '21', '13451054608', 'IT', '2017-04-01']]
            staff_id = row[0]  # 得到id值
            staff_index = STAFF_DATA['id'].index(staff_id)  # 得到id值在STAFF_INFO[id]的索引
            STAFF_DATA[col_name][staff_index] = new_val  # 修改col_name值
        save_db()
        print(tabulate(STAFF_DATA, headers=COLUMN_ORDERS))
        print_log("成功修改了%s条数据!" % len(match_data))

    else:
        print_log("语法错误，未检测到set", "error")


def syntax_delete(query_clause, match_data):
    """
     解析删除语句
     del from staff_table where id=3
    :return:
    """
    for row in match_data:
        staff_id = row[0]  # 得到id值
        staff_index = STAFF_DATA['id'].index(staff_id)  # 得到id值在STAFF_INFO[id]的索引
        # print_log(staff_index)
        for col in COLUMN_ORDERS:
            STAFF_DATA[col].remove(STAFF_DATA[col][staff_index])  # 修改col_name值

    save_db()
    print_log("成功删除%s条纪录" % len(match_data))
    print(tabulate(STAFF_DATA, headers=COLUMN_ORDERS))


# def op_gt(key, value):
#     match_data = []
#     for index, val in enumerate(STAFF_DATA[key]):
#         if float(val) > float(value):  # 筛选大于value的数据
#             print(val)
#             match_data_row = []
#             for col in COLUMN_ORDERS:
#                 match_data_row.append(STAFF_DATA[col][index])
#             match_data.append(match_data_row)
#     return match_data
#
#
# def op_lt(key, value):
#     match_data = []
#     for index, val in enumerate(STAFF_DATA[key]):
#         if float(val) < float(value):  # 筛选小于value的数据
#             match_data_row = []
#             for col in COLUMN_ORDERS:
#                 match_data_row.append(STAFF_DATA[col][index])
#             match_data.append(match_data_row)
#     return match_data
#
#
# def op_eq(key, value):
#     match_data = []
#     for index, val in enumerate(STAFF_DATA[key]):
#         if float(val) == float(value):  # 筛选==value的数据
#
#             match_data_row = []
#             for col in COLUMN_ORDERS:
#                 match_data_row.append(STAFF_DATA[col][index])
#             match_data.append(match_data_row)
#
#     return match_data
#
#
# def op_like(key, value):
#     match_data = []
#     for index, val in enumerate(STAFF_DATA[key]):
#         if value in val:  # 筛选大于value 在val中的
#             print(val)
#             match_data_row = []
#             for col in COLUMN_ORDERS:
#                 match_data_row.append(STAFF_DATA[col][index])
#             match_data.append(match_data_row)
#     return match_data


def op_compare(q_key, q_value, compare_str):
    """
    解析where 语句的操作符    q_key, q_value都是字符串
    :return:
    """
    match_data = []
    if compare_str == "=":
        compare_str = "=="
    for ind, val in enumerate(STAFF_DATA[q_key]):  # ind, val也都是字符串
        if compare_str != "like":

            # 字符比较
            exp_str = "%s%s%s" % ("'" + str(val) + "'", compare_str, "'" + str(q_value) + "'")
            # print(exp_str)

        else:  # 是like的情况  用in来判断
            # if compare_str = like then compare_str = ' in  '
            op_str = ' in '

            if q_value.find("'") != -1:
                val = "'" + val + "'"
            elif q_value.find("\"") != -1:
                val = "\"" + val + "\""
            else:
                val = "'" + val + "'"
                q_value = "'" + q_value + "'"

            exp_str = "%s%s%s" % (q_value, op_str, val)
            # print_log("in="+exp_str)

        # print_log(exp_str)
        if eval(exp_str):
            row_data = []
            for col in COLUMN_ORDERS:
                row_data.append(STAFF_DATA[col][ind])
            match_data.append(row_data)
    # print(tabulate(match_data, headers=COLUMN_ORDERS, tablefmt="grid"))
    return match_data


# def syntax_where(clause):
#     """
#     :param clause: where部分的语句
#     :return:返回根据where条件返回的数据
#
#     where查找是所有查询语句都会用到的公共操作
#     """
#     operators = {'>': op_gt, '<': op_lt, '=': op_eq, 'like': op_like}
#     for op_key, op_func in operators.items():
#         if op_key in clause:
#             key, value = clause.split(op_key)
#             return op_func(key.strip(), value.strip())
#     else:
#         print("\033[31;1mError:语句条件%s不支持\033[0m" % clause)
#         return False


def syntax_where(where_clause):
    """
    解析where条件
    where age > 22
    :param where_clause:
    :return:
    """
    # 操作字符
    op_list = [">", "<", "=", "like"]

    for op_key in op_list:
        if op_key in where_clause:
            q_key, q_value = where_clause.split(op_key)
            if q_key.strip() in COLUMN_ORDERS and q_value.strip() != "":
                match_data = op_compare(q_key.strip(), q_value.strip(), op_key)
                return match_data
            else:
                if not q_key.strip() in COLUMN_ORDERS:
                    error_str = "语法错误,字段%s不存在" % q_key
                else:
                    error_str = "条件值为空"

                print_log(error_str, "error")
                return False

    else:
        print_log("语法错误,符号不在[<,>,=,like]中", "error")
        return


def syntax_parser(cmd):
    """
    :param cmd: 输入的查询语句

    find name , age from staff_table where age > 22
    update staff_table set age=20 where name=Alex Li

    :通过判断不同的查询类型执行不同的操作
    :return:无返回
    """

    syntax_list = {
        'find': syntax_find,
        'add': syntax_add,
        'update': syntax_update,
        'del': syntax_delete,
    }

    if cmd.split()[0] in syntax_list.keys() and "staff_table" in cmd:
        if 'where' in cmd:  # add没有where单独处理
            # pass #返回指定数据
            query_cmd, where_clause = cmd.split("where")
            # 修改处：where_clause.strip() 注意要strip()
            matched_data = syntax_where(where_clause.strip())  # 通过where 条件顾虑从符合条件的数据
            # syntax_where(where_clause)
            if matched_data == False:
                return
            input_action = cmd.split()[0]
            syntax_list[input_action](query_cmd.strip(), matched_data)

        else:  # add的情况 返回所有matched_data数据 无过滤
            matched_data = []  # 获取add时的所有数据
            # 内存中STAFF_DATA数据格式z
            # {'id': [],'name':[],'age': [],'phone':[],'dept':[],'enrolled_date'[]
            # 转化成matched_data的格式
            # [['3', 'Rain Wang', '21', '13451054608', 'IT', '2017-04-01']]

            for index, staff_id in enumerate(STAFF_DATA['id']):
                row = []
                for col in COLUMN_ORDERS:  # 是从内存的STAFF_DATA中取出数据放入matched_data
                    row.append(STAFF_DATA[col][index])
                matched_data.append(row)
            # 修改处：add 没有where 关键字 ：所以把cmd当成 query_cmd部分来处理
            syntax_list[cmd.split()[0]](cmd.split()[2], matched_data)

    else:
        print_log('''语法错误!\nsample:[find/add/update/delete] name,age from [staff_table] where [id][>/</=/like][2]''',
                  'error')


def main():
    """"
    程序入口函数
    """
    while True:
        cmd = input("[staff db]:").strip()
        # python 中那些值视为假
        # "spam"/True , ""/False , []/False , {}/False , 1/True , 0.0/False , None/False
        if not cmd: continue
        syntax_parser(cmd)  # 调用解析操作


STAFF_DATA = load_db()
# deletedata("1")
main()

if __name__ == '__main__':
    """
    sql 查询
    
    add:        add staff_table lxm,25,134435344,IT,2015-10-29      
    find        find name , age from staff_table where age > 22
    del:        del from staff_table where id=3
    update：    update staff_table set dept = 开发部 where age = 22
    """
    STAFF_DATA = load_db()
    while True:
        input_str = input("[staff db]   ").strip()
        # python 中那些值视为假
        # "spam"/True , ""/False , []/False , {}/False , 1/True , 0.0/False , None/False
        if not input_str: continue
        syntax_parser(input_str)  # 调用解析操作
