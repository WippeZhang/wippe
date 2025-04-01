import re

# test = {
#     "r1" :{
#         "host" : "cisco",
#         "password" : "123",
#         "port": 22
#     }
# }
# for i in test:
#     hostname = test[i]["host"]
#     password = test[i]["password"]
#     port = test[i]["port"]
#     print(hostname,password,port)

# text = """
# [ID ] 主机名              IP               端口
# [0  ] cn-met-shangh-ce-01 10.210.30.1      22
# [1  ] cn-met-shangh-ce-02 10.210.30.2      22
# [2  ] cn-met-beijin-ce-01 10.210.30.3      22
# [3  ] cn-met-hongko-ce-01 10.210.30.4      22
# """
#
# ip_com = re.compile('\d+\.\d+\.\d+\.\d+')
# ip_findall = ip_com.findall(text)
# ret = re.sub(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)',r'\033[91m\1\033[0m', text)
# print(ret)

import openpyxl
import pprint

def group_and_extract_from_excel(file_path, sheet_name, column_name):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]

    # 获取指定列的数据
    column_data = sheet[column_name]

    data = {}
    for cell in column_data[0:]:
        value = cell.value
        if value and '[' in str(value):
            num, content = str(value).split('[')
            content = content.rstrip(']')

            if content not in data:
                data[content] = [int(num)]
            else:
                data[content].append(int(num))
        if str(value) in str(value) and '[' not in str(value):
            num = int(value)
            if 'Null' not in data:
                data['Null'] = [num]
            else:
                data['Null'].append(num)


    return data

# 文件路径、工作表名称和列名需要根据实际情况修改
file_path = 'aspath-new.xlsx'
sheet_name = 'Sheet1'
column_name = 'A'

result = group_and_extract_from_excel(file_path, sheet_name, column_name)
# print(result)



for key, values in result.items():
    jz = key
    data = values  # 将 data 定义在循环外
    classified_data = {}
    for num in data:
       #  print(key + ":" + str(num))

        ln = len(str(num)) - 1
        key = str(num)[:ln]  # 取除了个位数之外的数字作为字典键
        value = num % 10  # 取个位数作为字典值
        if key in classified_data:
            classified_data[key].append(value)
        else:
            classified_data[key] = [value]

    classified_data_list = []


    for key, values in sorted(classified_data.items()):
        classified_data_list.append({key: values})


    for xx in classified_data_list:
        print(str(xx) + '[' + str(jz) + ']')

    # print(len(classified_data_list))
    # print('[' + jz + ']')
    # print()
    # print()