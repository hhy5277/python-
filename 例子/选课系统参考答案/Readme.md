#作业: 选课系统

### 作者介绍：
- author：何坤祥
- 码云地址：https://gitee.com/henson01/projects

作业需求:
角色:学校、学员、课程、讲师
要求:
1. 创建北京、上海 2 所学校
2. 创建linux , python , go 3个课程 ， linux\py 在北京开， go 在上海开
3. 课程包含，周期，价格，通过学校创建课程
4. 通过学校创建班级， 班级关联课程、讲师
5. 创建学员时，选择学校，关联班级
5. 创建讲师角色时要关联学校，
6. 提供两个角色接口
6.1 学员视图， 可以注册， 交学费， 选择班级，
6.2 讲师视图， 讲师可管理自己的班级， 上课时选择班级， 查看班级学员列表 ， 修改所管理的学员的成绩
6.3 管理视图，创建讲师， 创建班级，创建课程
7. 上面的操作产生的数据都通过pickle序列化保存到文件里

--------------------------

运行说明：
先安装：
pip install termcolor

python版本： python3.6

选课信息已经建好如：
    1、管理员：admin/admin
    2、课程python , linux, go，地址：北京， 上海
    3、讲师分别：alex, henson, ken  密码：123
    4、学生：小明/123


目录结构：
    ├── bin
    │   ├── __init__.py
    │   └── run.py                    # 启动文件
    ├── conf
    │   ├── __init__.py
    │   └── settings.py               # 全局配置文件
    ├── core
    │   ├── __init__.py
    │   ├── common.py                 # 公共库文件
    │   ├── CourseClass.py            # 课程库
    │   ├── GradesClass.py            # 班级库
    │   ├── main.py                   # 主逻辑交互文件
    │   ├── Baseclass.py              # 数据读写库
    │   ├── SchoolClass.py            # 学校类库
    │   ├── SchoolPeople.py           # 基类库
    │   ├── StudentClass.py           # 学生类库
    │   └── TeacherClass.py           # 老师类库
    └── db                            # 数据文件
        ├── course.txt
        ├── grade.txt
        ├── school.txt
        ├── student.txt
        └── teacher.txt

选课本系统共分为3大环节
    在系统首次启动之后，给了一个超级管理员：admin/admin，才会打印相关信息
    1. 管理员系统
        【1】  创建/删除 学校
        【2】  创建 讲师
        【3】  创建课程
        【4】  创建班级
        【5】  查看学校
        【6】  查看讲师
        【7】  查看课程
        【8】  查看学生
    2. 教师系统
        登录
            【1】  查询个人信息
            【2】  查询所管班级
            【3】  选择班级上课

    2. 学生系统
        【1】  注册
        【2】  登录系统
                【1】  查询个人详情
                【2】  交学费

