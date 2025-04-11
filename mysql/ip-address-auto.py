import json
import time
import requests
import mysql.connector
import re
from datetime import datetime, timedelta
from pyquery import PyQuery as pq
from tqdm import tqdm


def get_last_quarter_timestamp_range():
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # 当前季度
    current_quarter = (current_month - 1) // 3 + 1

    # 上一季度
    if current_quarter == 1:
        last_quarter = 4
        last_quarter_year = current_year - 1
    else:
        last_quarter = current_quarter - 1
        last_quarter_year = current_year

    start_month = (last_quarter - 1) * 3 + 1
    start_date = datetime(last_quarter_year, start_month, 1)

    if last_quarter == 4:
        end_date = datetime(last_quarter_year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_date = datetime(last_quarter_year, start_month + 3, 1) - timedelta(seconds=1)

    return int(start_date.timestamp()), int(end_date.timestamp()), start_date.strftime('%Y-%m'), end_date.strftime('%Y-%m')


def get_total_pages():
    last_url = "https://en.greatfire.org/search/ip-addresses?page=0"
    response = requests.get(last_url)
    context = response.text
    page = re.compile('<li class="pager-last last">.*page=(\d+)">')
    context_find = page.findall(context)
    return int(context_find[0])


def get_greatfire_ip(start, end, start_timestamp, end_timestamp):
    err = []
    succ = []
    all_domains = set()

    # MySQL连接
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

    for j in tqdm(range(start, end + 1), desc="Fetching Pages"):
        url = f'https://en.greatfire.org/search/ip-addresses?page={j}'
        try:
            response = requests.get(url)
            response.raise_for_status()

            d = pq(response.text)
            rows = d('tbody tr')

            for row in rows.items():
                ip_elem = row.find('a').eq(0)
                time_elem = row.find('td').eq(1)
                censored_elem = row.find('td').eq(2)

                if not (ip_elem and time_elem and censored_elem):
                    continue

                # 处理 IP
                ip_raw = ip_elem.attr('href')
                ip_unquoted = requests.utils.unquote(ip_raw).lstrip('/')
                domain = ip_unquoted.replace('https/', '').replace('http/', '').split(":")[0]
                domain = domain.split("/")[0]

                if domain in all_domains:
                    continue
                all_domains.add(domain)

                # 处理时间
                time_str = time_elem.text()
                time_arr = time_str.split(' ')
                formatted_time_str = f"{time_arr[1]}-{time_arr[0]}"
                timestamp = int(time.mktime(time.strptime(formatted_time_str, '%Y-%b')))
                if not (start_timestamp <= timestamp <= end_timestamp):
                    continue
                time_str_mysql = time.strftime('%Y-%m-%d', time.strptime(formatted_time_str, '%Y-%b'))

                # 处理 censored 百分比
                censored = int(censored_elem.text().strip('%'))
                if censored < 100:
                    continue

                # 准备插入
                insert = {
                    'json': json.dumps({
                        'ip': ip_raw,
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

                # 插入 MySQL
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

        except Exception as e:
            err.append({'info': str(e), 'page': j, 'domain': domain, 'censored': censored})

    conn.close()
    print("抓取完成，失败页面如下：")
    print(err)


if __name__ == "__main__":
    # 自动计算上季度时间范围
    start_ts, end_ts, start_str, end_str = get_last_quarter_timestamp_range()
    print(f"本次运行抓取时间范围：{start_str} → {end_str}（时间戳：{start_ts} - {end_ts}）")

    # 自动获取总页数并开始抓取
    total_pages = get_total_pages()
    get_greatfire_ip(0, total_pages, start_ts, end_ts)
