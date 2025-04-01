import requests
import re



url = "https://en.greatfire.org/search/ip-addresses?page=0"
# print(url)
try:
    response = requests.get(url)
    # if response.status_code == 200:
    #     # 打印网页内容
    #     i = response.text
    #     com = re.compile('.*<title>(.*) - bgp.he.net</title>')
    #     i_find = com.findall(i)
    #     for x in i_find:
    #         print(x)
    # print(response.text)
    context = response.text
    page = re.compile('<li class="pager-last last">.*page=(\d+)">')
    context_find = page.findall(context)
    print(context_find[0])
    # else:
    #     print(f"请求失败，状态码：{response.status_code}")
except Exception as e:
    print(f"发生错误：{e}")

