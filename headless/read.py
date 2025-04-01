file_path = "Outlook-ip.txt"

# 打开文件并逐行读取内容
with open(file_path, 'r') as file:
    lines = file.readlines()

# 打印提取到的每一行内容
for line in lines:
    # print(line.strip())  # 使用 strip() 方法去除行尾的换行符
    print("ip firewall address-list add address=" + line.strip() + " list=Outlook")