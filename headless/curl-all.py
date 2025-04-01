import subprocess
import re

url = "https://sdwan.esun21.cn/esun/admin.php/backend_ensdwbcus/saasregionlist#"

# 使用 subprocess.run 执行 curl 命令，将输出保存到文件
with open('output.txt', 'wb') as output_file:
    subprocess.run(['curl', url], stdout=output_file, stderr=subprocess.PIPE)

# 打开文件并读取内容
with open('output.txt', 'rb') as output_file:
    output = output_file.read().decode('utf-8')  # 解码为文本


# 打印输出
# print(output)
print('区域：')
print('1.google_gstatic 2.Cloudflare 3.zooms 4.Akamai')
print('5.Zscaler-Asia&Pacific 6.Zscaler-America 7.Zscaler-Europe and Africa 8.Zscaler 9.Cisco WebEx')
print('10.Skype and Microsoft Teams-America 11.Skype and Microsoft Teams-Europe 12.Skype&Teams')
print('13.CM 14.CT 15.CU')
print('16.China')
print('17.Salesforce-Asia&Pacific 18.Salesforce-America 19.Salesforce-Europe 20.Salesforce')
print('21.Office365-America 22.Office365-Europe 23.Office365 24.Office_online 25.Sharepoint&Onedrive 26.Outlook&Exchange 27.office365-teams')
print('28.Azure-Asia&Pacific 29.Azure-America 30.Azure-Europe 31.Azure')
print('32.AWS-Asia&Pacific 33.AWS-America 34.AWS-Europe 35.AWS')
print('')
while True:
    area_name = input('Input Num of area:')
    if re.match('\D+', area_name):
        print('只能使用数字，请重输！')
    elif area_name == '1':
        area_name = 'google_gstatic'
        break
    elif area_name == '2':
        area_name = 'Cloudflare'
        break
    elif area_name == '3':
        area_name = 'zooms'
        break
    elif area_name == '4':
        area_name = 'Akamai-global'
        break
    elif area_name == '5':
        area_name = 'Zscaler-Asia&Pacific'
        break
    elif area_name == '6':
        area_name = 'Zscaler-America'
        break
    elif area_name == '7':
        area_name = 'Zscaler-Europe and Africa'
        break
    elif area_name == '8':
        area_name = 'Zscaler'
        break
    elif area_name == '9':
        area_name = 'Cisco WebEx'
        break
    elif area_name == '11':
        area_name = 'Skype and Microsoft Teams-Europe'
        break
    elif area_name == '12':
        area_name = 'Skype&Teams'
        break
    elif area_name == '13':
        area_name = 'CM'
        break
    elif area_name == '14':
        area_name = 'CT'
        break
    elif area_name == '15':
        area_name = 'CU'
        break
    elif area_name == '16':
        area_name = 'China'
        break
    elif area_name == '17':
        area_name = 'Salesforce-Asia&Pacific'
        break
    elif area_name == '18':
        area_name = 'Salesforce-America'
        break
    elif area_name == '19':
        area_name = 'Salesforce-Europe'
        break
    elif area_name == '20':
        area_name = 'Salesforce'
        break
    elif area_name == '21':
        area_name = 'Office365-America'
        break
    elif area_name == '22':
        area_name = 'Office365-Europe'
        break
    elif area_name == '23':
        area_name = 'Office365'
        break
    elif area_name == '24':
        area_name = 'Office_online'
        break
    elif area_name == '25':
        area_name = 'Sharepoint&Onedrive'
        break
    elif area_name == '26':
        area_name = 'Outlook&Exchange'
        break
    elif area_name == '27':
        area_name = 'office365-teams'
        break
    elif area_name == '28':
        area_name = 'Azure-Asia&Pacific'
        break
    elif area_name == '29':
        area_name = 'Azure-America'
        break
    elif area_name == '30':
        area_name = 'Azure-Europe'
        break
    elif area_name == '31':
        area_name = 'Azure'
        break
    elif area_name == '32':
        area_name = 'AWS-Asia&Pacific'
        break
    elif area_name == '33':
        area_name = 'AWS-America'
        break
    elif area_name == '34':
        area_name = 'AWS-Europe'
        break
    elif area_name == '35':
        area_name = 'AWS'
        break
    else:
        break
print(area_name + ':')
ip_com = re.compile(rf'{re.escape(area_name)}</td><td><a mesg=\[(.*?)\]\s', re.DOTALL)
# ip_com = re.compile((area_name)+('</td><td><a mesg=\[')+('.*')+('\]'))
ip_find = ip_com.findall(str(output))
for i in ip_find:
    # print(i)
    ip = i
    ip_without_quotes = ip.replace('"', '')
    # 将逗号改为换行符
    result = ip_without_quotes.replace(',', '\n')
    print(result)

    # 指定输出文件路径
    output_file_path = area_name + ".txt"
    # 打开文件并写入变量内容
    with open(output_file_path, 'w') as file:
        file.write(result)
    FinallyTxT = input("Data has been written to " + output_file_path)
