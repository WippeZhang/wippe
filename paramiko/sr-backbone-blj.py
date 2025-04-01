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
time.sleep(1)
end_mark_cisco = '#'
end_mark_Juniper = '>'
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
if end_mark_cisco in result:
    cli.send(b"terminal length 0\n")
    time.sleep(1)
    cli.send("show int des\n")
    time.sleep(3)
    result = cli.recv(65535).decode()
    # print(result)
    res = result.split('\n')
    list = []
    for l in res:
       # print(l)
       #  com_all = re.compile("((?:\w+\d+/\d+/\d+(?:\.\d+|\(10G\)|\.\d+\(10G\))?|Tunel\d+|Loop(?:back)?\d+|VT\d+|\w+\d+/\d+|Vl(?:an)?\d+|(?:E|e)ther\d+))\s+(\w+)\s+(\w+)\s+(.*\*)*")
       #  re_all = com_all.findall(l)
       #  for test_all in re_all:
       #      print(test_all)
        r = l.split()
        #print(r)
        if "-pe-" in l:
            list.append(r[0])
        # if "Gi" in l:
        #     list.append(r[0])
    # print(list)
    for interface in list:
        #print(interface)
        cli.send(b"terminal length 0\n")
        cli.send('show int ' + interface + '\n')
        time.sleep(1)
        result2 = cli.recv(65535).decode()
        # print(result2)
        com1 = re.compile('(MTU \d+) bytes')
        find1 = com1.findall(result2)
        for last in find1:
            print(interface + ':' + last)
if end_mark_Juniper in result:
    cli.send(b"terminal length 0\n")
    time.sleep(1)
    cli.send("show interfaces descriptions \n")
    time.sleep(4)
    result3 = cli.recv(65535).decode()
    # print(result3)
    res = result3.split('\n')
    list2 = []
    for l2 in res:
        # print(l2)
        r2 = l2.split()
        # print(r2)
        if "-pe-" in l2:
            list2.append(r2[0])
    for interface in list2:
        # print(interface)
        cli.send('show int ' + interface + '\n')
        time.sleep(1)
        result4 = cli.recv(65535).decode()
        # print(result4)
        if '.' in interface:
            com2 = re.compile('inet, (MTU: \d+)')
            find2 = com2.findall(result4)
            for last2 in find2:
                print(interface + ':' + last2 + '(+22)')
        else:
            com2 = re.compile('(MTU: \d+), Speed')
            find2 = com2.findall(result4)
            for last2 in find2:
                print(interface + ':' + last2)
ssh_client.close()
