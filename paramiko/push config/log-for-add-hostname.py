import paramiko
from io import StringIO
import time
import re




for i in range(13,21):
    key = paramiko.RSAKey.from_private_key_file(filename="wippe.pem", password='gMz0qFGOvvauS_ql')
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='10.0.90.85', port=22, username='wippe', compress=True, allow_agent=False,
                       look_for_keys=False, pkey=key)

    cli = ssh_client.invoke_shell(width=999, height=9999)
    time.sleep(1)
    cli.send('\n')
    time.sleep(1)
    end_mark_cisco = '#'
    end_mark_Juniper = '>'
    result = cli.recv(999999).decode()
    # print(result)


    cli.send('-pe-\n')
    time.sleep(2)
    # print(i)
    cli.send(str(i))
    cli.send('\n')
    time.sleep(3)
    cli.send('wippe\n')
    time.sleep(1)
    cli.send('z010808\n')
    time.sleep(1)
    cli.send("\n")
    time.sleep(1)
    result = cli.recv(65535).decode()
    # print(result)
    if '#' in result:
        cli.send('config terminal\n')
        time.sleep(1)
        cli.send('logging origin-id hostname\n')
        time.sleep(1)
        cli.send('exit\n')
        time.sleep(1)
        cli.send('wr\n')
        time.sleep(5)
        cli.send('exit\n')
        time.sleep(1)
        print(i, 'okay')

    ssh_client.close()