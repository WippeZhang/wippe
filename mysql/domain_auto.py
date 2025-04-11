import json
import time
import requests
from pyquery import PyQuery as pq
import mysql.connector
import re
from datetime import datetime, timedelta
from tqdm import tqdm

# ========== 自动获取上个季度的时间戳 ==========
def get_last_quarter_timestamps():
    current_month = datetime.now().month
    current_year = datetime.now().year

    if current_month in [1, 2, 3]:
        quarter_start_month = 10
        year = current_year - 1
    elif current_month in [4, 5, 6]:
        quarter_start_month = 1
        year = current_year
    elif current_month in [7, 8, 9]:
        quarter_start_month = 4
        year = current_year
    else:
        quarter_start_month = 7
        year = current_year

    start_time = datetime(year, quarter_start_month, 1)
    if quarter_start_month == 10:
        end_time = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_time = datetime(year, quarter_start_month + 3, 1) - timedelta(seconds=1)

    start_ts = int(time.mktime(start_time.timetuple()))
    end_ts = int(time.mktime(end_time.timetuple()))

    print(f"\n本次运行抓取时间范围：{start_time.strftime('%Y-%m')} → {end_time.strftime('%Y-%m')}（时间戳：{start_ts} - {end_ts}）")
    return start_ts, end_ts

# ========== 获取总页数 ==========
def get_last_page():
    url = "https://en.greatfire.org/search/domains?page=0"
    response = requests.get(url)
    context = response.text
    page = re.compile(r'<li class="pager-last last">.*page=(\d+)">')
    context_find = page.findall(context)
    return int(context_find[0]) if context_find else 0

# ========== 主逻辑 ==========
def get_greatfire_domain(start, end, start_ts, end_ts):
    conn = mysql.connector.connect(
        host="localhost",
        user="wippe",
        password="z010808",
        database="ip-address"
    )

    # ✅ 清空表
    print("正在清空 fire_domain 表...")
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE fire_domain")
    conn.commit()
    cursor.close()
    print("已清空 fire_domain 表。")

    err = []
    succ = []
    all_domains = set()

    for j in tqdm(range(start, end + 1), desc="Fetching Domain Pages"):
        url = f'https://en.greatfire.org/search/domains?page={j}'
        try:
            response = requests.get(url)
            response.raise_for_status()

            d = pq(response.text)
            rows = d('tbody tr')

            for row in rows.items():
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
                    pos = domain.find('/')
                    if pos != -1:
                        domain = domain[:pos]

                    if domain in all_domains:
                        continue
                    else:
                        all_domains.add(domain)
                else:
                    continue

                if time_elem:
                    time_str = time_elem.text()
                    time_arr = time_str.split(' ')
                    formatted_time_str = time_arr[1] + '-' + time_arr[0]
                    timestamp = int(time.mktime(time.strptime(formatted_time_str, '%Y-%b')))
                    if not (start_ts <= timestamp <= end_ts):
                        continue
                    time_str_mysql = time.strftime('%Y-%m-%d', time.strptime(formatted_time_str, '%Y-%b'))
                else:
                    continue

                if censored_elem:
                    censored = censored_elem.text().strip('%')
                    censored = int(censored)
                    if censored < 100:
                        continue
                else:
                    continue

                insert = {
                    'json': json.dumps({
                        'ip': ip,
                        'time': time_str,
                        'censored': censored_elem.text(),
                    }),
                    'domain': domain,
                    'time_str': time_str_mysql,
                    'time': timestamp,
                    'censored': censored,
                    'type': 2,
                    'page': j,
                }

                cursor = conn.cursor()
                insert_query = """
                    INSERT INTO fire_domain (json, domain, time_str, time, censored, type, page)
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

        except Exception as e:
            err.append({'info': str(e), 'page': j, 'domain': ip, 'censored': censored})

    print("抓取完成，失败页面如下：")
    print(err)
    conn.close()

# ========== 启动入口 ==========
if __name__ == "__main__":
    start_ts, end_ts = get_last_quarter_timestamps()
    last_page = get_last_page()
    get_greatfire_domain(0, last_page, start_ts, end_ts)
