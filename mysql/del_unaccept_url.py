import mysql.connector

# 建立连接
conn = mysql.connector.connect(
        host="localhost",
        user="wippe",
        password="z010808",
        database="ip-address"
)
cursor = conn.cursor()

# 删除以 .xyz 结尾的域名
sql = "DELETE FROM fire_domain_copy1 WHERE domain LIKE '%.xyz' or domain like '%.icu' or domain like '%.news' or domain like '%.app' or domain like '%.fun' or domain like '%.top' or domain like '%.rip' or domain like '%.vip' or domain like '%.link' or domain like '%.cat' or domain like '%.work';"
cursor.execute(sql)
conn.commit()

print(f"已删除 {cursor.rowcount} 条记录")

# 关闭连接
cursor.close()
conn.close()
