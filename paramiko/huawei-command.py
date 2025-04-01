import paramiko
from io import StringIO
import time
import re


key = paramiko.RSAKey.from_private_key_file(filename="wippe.pem",password='gMz0qFGOvvauS_ql')
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='10.0.90.85',port=22,username='wippe',compress=True,allow_agent=False,look_for_keys=False,pkey=key)

cli = ssh_client.invoke_shell(width=999, height=9999)
cli.send("\n")
time.sleep(2)
end_mark_Huawei = '<'
result = cli.recv(65535).decode()
# print(result)
hostname = input('请输入设备hostname：')
cli.send(hostname + '\n')
time.sleep(2)
cli.send('wippe\n')
time.sleep(1)
cli.send('z010808\n')
time.sleep(1)
cli.send("\n")
time.sleep(8)
result = cli.recv(65535).decode()
# print(result)
if end_mark_Huawei in result:
    username_command = None
    while True:
        userfilter = input('是否需要筛选用户？1.yes 2.no\n')
        if '1' in userfilter or 'yes' in userfilter or 'y' in userfilter or 'Yes' in userfilter or 'YES' in userfilter:
            username_command = input('请输入用户：')
            break
        elif '2' in userfilter or 'no' in userfilter or 'n' in userfilter or 'No' in userfilter or 'NO' in userfilter:
            break
        else:
            print('输入错误,请重输！')
    if username_command != None:
        cli.send('display logfile logfile/log.log | in command | in '+username_command+' | no-more\n')
    else:
        cli.send('display logfile logfile/log.log | in command | no-more\n')
    time.sleep(8)
    hw_result1 = cli.recv(65535).decode()
    res1 = hw_result1.split('\n')
    for i in res1:
        # print(i)
        # command_com1 = re.compile('(.*) cn')
        command_com = re.compile("(.*) cn.*User=(.*)\,\sA.*Command=(.*)\.")
        l_findall = command_com.findall(i)
        for last_result in l_findall:
            print(last_result)
    cli.close()
