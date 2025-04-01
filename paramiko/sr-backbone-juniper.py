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
end_mark_cisco = '#'
end_mark_Juniper = '>'
result = cli.recv(65535).decode()
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
if end_mark_Juniper in result:
    cli.send(b"terminal length 0\n")
    time.sleep(1)
    cli.send("show interfaces terse | no-more \n")
    time.sleep(4)
    result3 = cli.recv(65535).decode()
    #print(result3)
    a2 = re.compile(
        '(?:((?:\w+-(?:\d+/)+\d+|\w+)\.?(?:\d+)?)\s+(?:up\s+down|up\s+up)\s+inet)?\s+(\d+\.\d+\.\d+\.\d+)(?:/\d+\s+|\s+--> .*?)\n'
        '(?:\s+iso\s+\n)?(?:\s+inet6\s+((?:\w{1,4}:{1,2})+\w{1,4})/\d+\n)?(?:\s{44}((?:\w{1,4}:{1,2})+\w{1,4})/\d+\n)?')
    result = a2.findall(result3)

    pprint.pprint(result)