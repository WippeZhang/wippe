import re
import requests

# for ip in range(281):
#     url = "https://en.greatfire.org/search/ip-addresses?page="+str(ip)
#
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             # 打印网页内容
#             i = response.text
#             # print(i)
#         else:
#             print(f"请求失败，状态码：{response.status_code}")
#     except Exception as e:
#         print(f"发生错误：{e}")
#
#     ip_com_2023_9_12 = re.compile('(?:<td class="first"><a href=)(?:.*)(?:>)(?:http)?(?:s)?(?::\/\/)?(\d+\.\d+\.\d+\.\d+)(?:</a>)(?:.*)(Sep\s2023|Oct\s2023|Nov\s2023|Dec\s2023)(?:.*)(100%)(?:</td>)')
#     ip_com_2024_1_2 = re.compile('(?:<td class="first"><a href=)(?:.*)(?:>)(?:http)?(?:s)?(?::\/\/)?(\d+\.\d+\.\d+\.\d+)(?:</a>)(?:.*)(Jan\s2024|Feb\s2024)(?:.*)(100%)(?:</td>)')
#     ip_find = ip_com_2024_1_2.findall(i)
#     for j in ip_find:
#         print(j)


for n in range(1647):
    url = "https://en.greatfire.org/search/domains?page="+str(n)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 打印网页内容
            i = response.text
            # print(i)
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{e}")

    ip_com_2023_9_12 = re.compile('(?:<td class="first"><a href=)(?:.*)(?:>)(?:http)?(?:s)?(?::\/\/)?(.*)(?:</a>)(?:.*)(Sep\s2023|Oct\s2023|Nov\s2023|Dec\s2023)(?:.*)(100%)(?:</td>)')
    ip_com_2024_1_2 = re.compile('(?:<td class="first"><a href=)(?:.*)(?:>)(?:http)?(?:s)?(?::\/\/)?(.*)(?:</a>)(?:.*)(Jan\s2024|Feb\s2024)(?:.*)(100%)(?:</td>)')
    ip_find = ip_com_2024_1_2.findall(i)
    for j in ip_find:
        print(j)

