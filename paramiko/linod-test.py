import paramiko
from io import StringIO
import time
import re
import pprint


key = paramiko.RSAKey.from_private_key_file(filename="wippe.pem",password='gMz0qFGOvvauS_ql')
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='10.0.90.85',port=22,username='wippe',compress=True,allow_agent=False,look_for_keys=False,pkey=key)

cli = ssh_client.invoke_shell(width=999, height=9999)
cli.send("\n")
time.sleep(1)
result = cli.recv(65535).decode()
# print(result)
hostname = input('请输入设备hostname：')

cli.send(hostname + '\n')
time.sleep(1)
cli.send('wippe\n')
time.sleep(1)
cli.send('z010808\n')
time.sleep(1)
cli.send("\n")
time.sleep(1)
result = cli.recv(65535).decode()
# print(result)
cli.send('sys\n')
time.sleep(1)
cli.send('dis ip int bri | no-more \n')
time.sleep(3)
result = cli.recv(65535).decode()
# print(result)
res = result.split('\n')
print('可用ip为：')
list = []
for l in res:
    r = l.split()
    # print(r)
    if '103.204.72.' in l:
        list.append(r[1])
    elif '103.204.73.' in l:
        list.append(r[1])
    elif '202.160.142.' in l:
        list.append(r[1])
    elif '45.114.239.' in l:
        list.append(r[1])
    elif '45.114.236.' in l:
        list.append(r[1])
    elif '103.71.24.' in l:
        list.append(r[1])
    elif '118.143.233.' in l:
        list.append(r[1])
    elif '203.131.253.' in l:
        list.append(r[1])
    elif '45.114.238.' in l:
        list.append(r[1])
    elif '80.239.202.' in l:
        list.append(r[1])
    elif '217.243.18.' in l:
        list.append(r[1])
    elif '172.105.210.' in l:
        list.append(r[1])
print(list)

# list2 = []
# for l2 in res:
#     r2 = l2.split()
#     # print(r2)
#     if '103.204.73.' in l2:
#         list2.append(r2[1])
# print(list2)
#
# list3 = []
# for l3 in res:
#     r3 = l3.split()
#     # print(r3)
#     if '202.160.142.' in l3:
#         list2.append(r3[1])
# print(list3)
#
# list4 = []
# for l4 in res:
#     r4 = l4.split()
#     # print(r4)
#     if '45.114.239.' in l4:
#         list2.append(r4[1])
# print(list4)

ip_add = input('请选择一个ip作为源地址：')
mtu_choice = input('请选择64/1500作为mtu：')
des_ip = input('目的ip：')
cli.send('ping -s '+mtu_choice+' -a '+ip_add+' '+des_ip+' \n')
time.sleep(10)
result = cli.recv(65535).decode()
# print(result)
com1 = re.compile('\d+.*loss')
com2 = re.compile('min.*ms')
find1 = com1.findall(result)
find2 = com2.findall(result)
for last in find1:
    print('丢包率为：'+last)
for last2 in find2:
    print('延迟为：'+last2)
ssh_client.close()