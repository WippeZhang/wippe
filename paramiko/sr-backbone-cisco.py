import paramiko
import time
import re

client_devices = {
    "R1": {
        "host": "192.168.38.132",
        "username": "test",
        "password": "test",
        "port": 22,
    }
    # "Juniper-r1": {
    #     "host": "10.0.20.139",
    #     "username": "test",
    #     "password": "Esun@1sh",
    #     "port": 22,
    # }
}
for i in client_devices:
    print(i)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=client_devices[i]["host"], username=client_devices[i]["username"],
                       password=client_devices[i]["password"], port=client_devices[i]["port"])
    cli = ssh_client.invoke_shell()
    cli.send(b"terminal length 0\n")
    time.sleep(1)
    cli.send("show ip int br\n")
    time.sleep(1)
    result = cli.recv(65535).decode()
    # print(result)
    # ssh_client.close()
    res = result.split('\n')
    list = []
    for l in res:
        # print(l)
        r = l.split()
        # print(r)
        if "Ethernet" in l:
            list.append(r[0])
    # print(list)
    for interface in list:
        # print(interface)
        cli.send(b"terminal length 0\n")
        cli.send('show int '+interface+'\n')
        time.sleep(1)
        result2 = cli.recv(65535).decode()
        # print(result2)
        com1 = re.compile('(MTU \d+) bytes')
        find1 = com1.findall(result2)
        for last in find1:
            print(interface+':'+last)
    ssh_client.close()