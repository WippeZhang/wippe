import paramiko
import time
import re


def ip():
    ipaddr = input("请输入IP：")
    return ipaddr



client_devices = {
    "R1": {
        "host": "192.168.20.254",
        "username": "test",
        "password": "test",
        "port": 22,
    }
    # "r2": {
    #     "host": "192.168.38.131",
    #     "username": "wippe",
    #     "password": "Esun@1sh",
    #     "port": 22,
    # },
    # "r3": {
    #     "host": "192.168.38.130",
    #     "username": "wippe",
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
    # a, b, c = ssh_client.exec_command("show ip rou")
    cli = ssh_client.invoke_shell()
    cli.send(b"terminal length 0\n")
    time.sleep(1)
    # cli.send("ping "+ip+" \n")
    # cli.send(b"show version\n")
    # cli.send(b"show ip route vrf 1 ospf\n")
    # cli.send("trace "+ip()+" nu \n")
    # cli.send("show int g0/0\n")
    # cli.send("show ip arp "+ip()+" \n")
    # cli.send("show ip rou \n")
    # cli.send("show cdp nei\n")
    cli.send("show clock\n")
    time.sleep(4)
    result = cli.recv(65535).decode()
    print(result)
    # r = result.split("\n")
    # print("倒数第二跳："+r[-2])
    ssh_client.close()

    test_com1 = re.compile(r"\d+"+r"\."+r"\d+"+r"\."+r"\d+"+r"\."+r"\d+"+r"/"+r"\d+")
    test_com2 = re.compile(("[0-9]?"+"[0-9]?"+"[0-9]?"+"\."))
    test_com3 = re.compile("(?:[0-9]?[0-9]?[0-9]?\.){3}(?:[0-9]?[0-9]?[0-9]?)")
    test_com4 = re.compile("(?:(?:[3-9][0-9]?[0-9]?|[0-2]?[0-9]?[0-9]?)\.){3}(?:[0-9]?[0-9]?[0-9]?)")
    test_com5 = re.compile("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
    test_com6 = re.compile("Processor board ID (\w+)")
    test_com7 = re.compile("min/avg/max = \d+/(\d+)/\d+ ms")
    test_com8 = re.compile("(\d+) Ethernet interfaces")
    test_com9 = re.compile("(?:[^0-9]5\.)(?:(?:\d+)\.){2}(?:\d+)")
    test_com10 = re.compile("\d+ packets input, (\d+) bytes")
    test_com11 = re.compile("uptime is (.* minutes)")
    test_com12 = re.compile("(?:\d+\.\d+\.\d+\.\d+\s+)(?:\d+|-)(?:\s+)(\w+\.\w+\.\w+)")
    test_com13 = re.compile("\**\s{2,}(\d+\.\d+\.\d+\.\d+/*\d*)")
    test_com14 = re.compile("Port ID\s+\w+\s+(\w+\s\d+/\d+)")
    test_com15 = re.compile("Version \d+\.\d+")
    test_com16 = re.compile("\d+\s(\d+\.\d+\.\d+\.\d+)")
    test_com17 = re.compile("\w\**\s+(\d+\.\d+\.\d+\.\d+/*\d*)")
    test_com18 = re.compile("\d{1,}\s\d+\.\d+\.\d+\.\d+")
    test_com19 = re.compile("(4\s\d+\.\d+\.\d+\.\d+)(?:\s\d+\smsec){1,}(?:\r\n\s*)(?:(\d+\.\d+\.\d+\.\d+){0,}(?:\s\d+\smsec){0,}\s*|\n*){0,}")
    test_com20 = re.compile("(4\s\d+\.\d+\.\d+\.\d+)(?:\s\d+\smsec){1,}(\s*|\r*|\n*)(?:(?:\d+\.\d+\.\d+\.\d+)(?:\s\d+\smsec)(?:\s*|\r*|\n*)){0,}")
    test_com21 = re.compile("(?: 4\s)(\d+\.\d+\.\d+\.\d+)(?:\s\d+\smsec){1,}(?:\r\n\s*)(\d+\.\d+\.\d+\.\d+){0,}(?:\s\d+\smsec){0,}(?:\s*){0,}(\d+\.\d+\.\d+\.\d+){0,}(?:\s\d+\smsec){0,}(?:\s*){0,}")
    test_com22 = re.compile("\d+\:\d+\:\d+\.\d+\s\w+\s\w+\s\w+\s\d+\s\d+")
    test_findall = test_com22.findall(result)
    print(test_findall)
    for r in test_findall:
        # for res in r:
            print(r)
            # list1 = []
            # list1.append(res)
            # if list1(0) != '':
            #     print(list1)
    # cli = ssh_client.invoke_shell()
    # cli.send(b"show ip int br\n")
    # # cli.send(b"show ip os nei\n")
    # time.sleep(0.3)
    # result = cli.recv(1000).decode("ascii")
    # print(result)

