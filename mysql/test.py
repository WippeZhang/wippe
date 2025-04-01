# import mysql.connector
# import datetime
#
# # 连接数据库
# connection = mysql.connector.connect(host='localhost',
#                              user='wippe',
#                              password='z010808',
#                              database='ip-address')
#
# try:
#     # 使用cursor()方法获取操作游标
#     with connection.cursor() as cursor:
#         # 执行SQL查询获取当前时间戳
#         cursor.execute("SELECT CURRENT_TIMESTAMP")
#
#         # 获取单条数据
#         result = cursor.fetchone()
#         timestamp = result[0]
#
#         # 转换时间戳为Python的datetime对象
#         current_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
#         print(current_time)
#
# finally:
#     connection.close()

from datetime import datetime

# 示例时间戳列表
timestamps = [1721912400, 1722196800]

# 转换时间戳
readable_dates = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]

print(readable_dates)
