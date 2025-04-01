import requests
import re

list = [138421,
133118,
134542,
140886,
137539,
140726,
140717,
140716,
139007,
140707,
140979,
152120
]
for as_number in list:
    url = "https://bgp.he.net/AS" + str(as_number)
    # print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 打印网页内容
            i = response.text
            com = re.compile('.*<title>(.*) - bgp.he.net</title>')
            i_find = com.findall(i)
            for x in i_find:
                print(x)
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{e}")

