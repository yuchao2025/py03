import io

import pymysql


def get_data(file_path,target_date):
    """
    file_path:数据文件路径, txt格式
    target_date：数据日期
    """
    data = []
    with io.open(file_path,'r',encoding='utf-8') as f:
        delimiter = ','    # txt文件格式的固定分隔符
        line = f.readline()    # 按行读取
        while line:
            content = line.split(delimiter)    # 数据分割
            content[-1] = content[-1].strip('\n')    # 要去掉数据结尾的'\n'
            data.append(content)
            line = f.readline()
    return data[0], data[1:]  # 返回第一行列名，和去掉第一行的数据


def insert_data_to_mysql(conn,table_name,col_name,data,targetDate):
    """
    conn: mysql连接
    table_name: 要插入mysql中的表名
    col_name: 读取的txt文件中的第一行列名
    data: 读取的txt文件中的数据
    targetDate: 账期
    """
    # 生成插入数据语句 insert into table_name(col_name1, col_name2, ...) values(%s, %s, ...)
    column_name = ''
    for name in col_name:
        column_name = column_name + name + ','
    column_name = column_name[:-1]    # 去掉最后的逗号
    print(column_name)

    n_col = len(col_name)
    print(n_col)
    column_value = '%s,'*n_col

    print(column_value)
    column_value = column_value[:-1]    # 去掉最后的逗号

    # 建立游标
    cur = conn.cursor()
    # 执行插入数据
    try:
        # 生成完整的插入数据语句
        sql_insert = 'INSERT INTO ' + table_name + '(' + column_name + ')' + ' VALUES(' + column_value + ')'
        print(sql_insert)
        cur.executemany(sql_insert,data)
        # 提交任务
        conn.commit()
    except Exception as e:    # 失败回滚
        print(str(e))
        conn.rollback()


def run_file_to_mysql(table_name,target_date):
    """
    table_name：要插入mysql的表名，同时也是数据文件名
    target_date: 目标账期
    """
    ## 目标文件名
    base_path = 'C:\\Users\\EDY\\Desktop\\'  # 目标文件路径
    file_path = base_path + table_name + '_' + target_date + '.txt'    # 目标文件名：为方便，采用要插入的表名+账期
    print(4)
    # 获取数据
    try:
        col_name,data = get_data(file_path,target_date)

    except Exception as e:
        print('获取数据失败：', str(e))
        return 1

    # 建立连接
    try:
        print("2")
        #filename = r'D:\Downloads\output.xlsx'
        host = "172.16.31.67"  # 数据库主机地址
        user = "root"  # 数据库用户名
        password = "123@qq.com"  # 数据库密码
        database = "test1"  # 数据库名称
        table = "sys_job1"  # 数据库表名


        conn = pymysql.connect(
            host=host,  # 数据库主机地址
            user=user,  # 数据库用户名
            password=password,  # 数据库密码
            database=database,  # 数据库名称
            port=3306
        )


        #config = {'host':'172.16.31.67','port':'3306','user':'root','passwd':'123@qq.com','db':'test1'}
        #conn = pymysql.connect(config)
        print("3")
        # 插入数据
        try:
            insert_data_to_mysql(conn,table_name,col_name,data,target_date)
        except Exception as e:
            print('插入数据失败：', str(e))
            return 1
        finally:
            # 关闭连接
            conn.close()
    except Exception as e:
        print('连接数据库失败：', str(e))
        return 1
    return 0


def main():
    # 导入日期
    print("ok")
    targetDate = '2024-12-10'
    # 导入表名
    tableName = 'sys_job1'
    # 执行任务
    code = run_file_to_mysql(tableName,targetDate)
    if code == 0:
        print('success!')
    else:
        print('error')



if __name__ == '__main__':
    name="John"

    age=25

    formatted_string="My name is%s#"%(name)# and I am%d years old."%(name,age)

    print(formatted_string)
    main()
