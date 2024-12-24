from aifc import Error

import pymysql
import csv
#from mysql.connector import Error, FieldType

# 连接到MySQL数据库
def connect_to_database(host, database, user, password):
    try:
        connection = pymysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        return connection
    except Error as e:
        print(f"Error: {e}")

# 创建表（如果不存在）
def create_table_if_not_exists(cursor, table_name, data_header):
    table_exists = cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    if not table_exists:
        query = "CREATE TABLE " + table_name + " ("
        for i, column_name in enumerate(data_header, 1):
            query += column_name + " VARCHAR(255),"
        query = query.rstrip(',') + ')'
        cursor.execute(query)

# 写入数据到MySQL
def write_data_to_mysql(cursor, table_name, data_header, data_list):
    placeholders = ', '.join(['%s'] * len(data_header))
    print(placeholders)
    query = "INSERT INTO " + table_name + " (" + ', '.join(data_header) + ") VALUES (" + placeholders + ")"
    print(query)
    for data in data_list:
        print(query, data)
        cursor.execute(query, data)


# 读取TXT文件并写入MySQL
def txt_to_mysql(txt_file_path, table_name, host, database, user, password):

    host = "172.16.31.67"  # 数据库主机地址
    user = "root"  # 数据库用户名
    password = "123@qq.com"  # 数据库密码
    database = "test1"  # 数据库名称
    table = "sys_job1"  # 数据库表名


    connection = pymysql.connect(
        host=host,  # 数据库主机地址
        user=user,  # 数据库用户名
        password=password,  # 数据库密码
        database=database,  # 数据库名称
        port=3306
    )
    print(1)
    print(txt_file_path)

    #connection = connect_to_database(host, database, user, password)
    cursor = connection.cursor()

    with open(txt_file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        data_header = next(reader)
        print(data_header)
        #create_table_if_not_exists(cursor, table_name, data_header)

        data_list = [row for row in reader]
        print(data_list)
        print(111)
        print(cursor, table_name, data_header, data_list)
    write_data_to_mysql(cursor, table_name, data_header, data_list)



    connection.commit()
    cursor.close()
    connection.close()

# 使用示例

if __name__ == '__main__':
    # 需要输入的参数
    #filename = r'/root/python01/output.xlsx'  # Excel文件路径
    filename = 'C:\\Users\\EDY\\Desktop\\sys_job.txt'
    host = "172.16.31.67"  # 数据库主机地址
    myuser = "root"  # 数据库用户名
    mypassword = "123@qq.com"  # 数据库密码
    mydatabase = "test1"  # 数据库名称
    my_table = "sys_job1"  # 数据库表名

    # 调用函数，将Excel数据插入到MySQL数据库中(Excel中第一行是表中的字段名称，第二行开始为数据)
    #insert_excel_data_to_mysql(filename, host, user, password, database, table)
    txt_to_mysql(filename, my_table, host, mydatabase, myuser, mypassword)