import json
import time
import requests
from pyquery import PyQuery as pq
# import psycopg2
import mysql.connector
import re

# 创建 PostgreSQL 数据库连接
# conn = psycopg2.connect(
#     dbname='zabbix',
#     user='zabbix',
#     password='esun21',
#     host='10.0.90.94',
#     port='5432'
# )

last_url = "https://en.greatfire.org/search/ip-addresses?page=0"
response = requests.get(last_url)
context = response.text
page = re.compile('<li class="pager-last last">.*page=(\d+)">')
context_find = page.findall(context)
last_page = context_find[0]

# Mysql 数据库连接
conn = mysql.connector.connect(
    host="localhost",
    user="wippe",
    password="z010808",
    database="ip-address"
)
# 👉 清空 ip_address 表
print("正在清空 ip_address 表...")
cursor = conn.cursor()
cursor.execute("TRUNCATE TABLE ip_address")
conn.commit()
cursor.close()
print("已清空 ip_address 表。")


def get_greatfire_ip(start, end):
    err = []
    succ = []
    all_domains = set()

    for j in range(start, end + 1):
        url = 'https://en.greatfire.org/search/ip-addresses?page={}'.format(j)
        try:
            response = requests.get(url)
            response.raise_for_status()

            d = pq(response.text)
            rows = d('tbody tr')
            
            for row in rows.items():
                # print(11)
                ip = ''
                censored = ''

                ip_elem = row.find('a').eq(0)
                time_elem = row.find('td').eq(1)
                censored_elem = row.find('td').eq(2)

                if ip_elem:
                    ip = ip_elem.attr('href')
                    ip = requests.utils.unquote(ip)
                    t = ip.lstrip('/')
                    domain = t.replace('https/', '').replace('http/', '')
                    domain = domain.split(":")[0]
                    pos = domain.find('/')
                    if pos != -1:
                        domain = domain[:pos]

                    if domain in all_domains:
                        continue
                    else:
                        all_domains.add(domain)

                if time_elem:
                    time_str = time_elem.text()
                    time_arr = time_str.split(' ')
                    formatted_time_str = time_arr[1] + '-' + time_arr[0]
                    timestamp = int(time.mktime(time.strptime(formatted_time_str, '%Y-%b')))
                    # 2024年4月1日到2024年6月30日
                    #timestamp = time.strftime('%Y-%m-%d', time.strptime(formatted_time_str, '%Y-%b'))
                    #starttime = "1711900800"
                    #endtime = "1719763199"
                    start_timestamp = int(time.mktime(time.strptime('2025-01', '%Y-%m')))
                    end_timestamp = int(time.mktime(time.strptime('2025-03', '%Y-%m'))) - 1
                    if not (start_timestamp <= timestamp <= end_timestamp):
                        continue
                    time_str_mysql = time.strftime('%Y-%m-%d', time.strptime(formatted_time_str, '%Y-%b'))


                if censored_elem:
                    censored = censored_elem.text().strip('%')
                    censored = int(censored)
                    if censored < 100:
                        continue

                insert = {
                    'json': json.dumps({
                        'ip': ip,
                        'time': time_str,
                        'censored': censored_elem.text(),
                    }),
                    'domain': domain,
                    'time_str': time_str,
                    'time': timestamp,
                    'censored': censored,
                    'type': 2,
                    'page': j,
                }
                # print(insert)
                # 插入数据到 PostgreSQL 数据库
                cursor = conn.cursor()
                insert_query = """
                    INSERT INTO ip_address (json, ip, time_str, time, censored, type, page)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    insert['json'],
                    insert['domain'],
                    insert['time_str'],
                    insert['time'],
                    insert['censored'],
                    insert['type'],
                    insert['page']
                ))
                conn.commit()
                cursor.close()

                succ.append(j)
                # print('--------------------')
        except Exception as e:
            err.append({'info': str(e), 'page': j, 'domain': ip, 'censored': censored})

    print(err)


# 使用示例
get_greatfire_ip(0, int(last_page))  # 替换成你的起始和结束页码
# get_greatfire_ip(0, 0)  # 替换成你的起始和结束页码

# 关闭数据库连接
conn.close()
