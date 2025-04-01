import openpyxl
import pprint
# 打开Excel文件
excel_file_path = 'aspath-px.xlsx'
workbook = openpyxl.load_workbook(excel_file_path)

# 选择第一个工作表
sheet = workbook.active

# 打印表格内容
data = []
for row in sheet.iter_rows():
    for cell in row:
        # print(cell.value, end='\t')
        data.append(cell.value)
    # print()

# 关闭Excel文件
workbook.close()
# pprint.pprint(asps)
# print(len(asps))

classified_data = {}

for num in data:
    ln = len(str(num))-1
    key = str(num)[:ln]  # 取除了个位数之外的数字作为字典键
    value = num % 10  # 取个位数作为字典值
    if key in classified_data:
        classified_data[key].append(value)
    else:
        classified_data[key] = [value]

classified_data_list = []

for key, values in sorted(classified_data.items()):
    classified_data_list.append({key: values})

pprint.pprint(classified_data_list)
print(len(classified_data_list))