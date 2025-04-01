import paramiko
import time
import pprint
import re

class NtwTools:
    def __init__(self, host, user, psw):
        self.host = host
        self.user = user
        self.psw = psw

    def mtu_scan(self, dstip):
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.connect(hostname=self.host, username=self.user, password=self.psw)
        shell = sshClient.invoke_shell()

        print('登录设备：' + self.host + '\r\n')
        time.sleep(1)

        while True:
            cache = shell.recv(1000).decode()
            print(cache)
            if cache.endswith('#') == True:
                break
            else:
                time.sleep(1)

        lis = []
        for mtu in range(1200, 1501):
            shell.sendall('ping ' + dstip + ' df-bit repeat 5 size ' + str(mtu) + ' \r\n')
            time.sleep(1)

            while True:
                cache = shell.recv(1000).decode()
                print(cache)
                if cache.endswith('#') == True:
                    time.sleep(1)
                    break  # 使用break跳出当前循环
                else:
                    time.sleep(1)

            x = re.compile('\r\nSuccess rate is (\d+) percent')
            result = x.findall(cache)
            if result[0] == '0':
                lis.append(mtu)
                # print(' unreachable mtu: ', mtu)
                print('\033[32;0munreachable mtu: ' + '\033[0m', mtu)
            else:
                print('\033[32;0mmtu=' + str(mtu) + ' ping success !! unreachable mtu: \033[0m', lis)
        # print(lis)  # 打印所有结果
        sshClient.close()
        # 输出参数，所有不可达的mtu
        return lis

    def ping_10000(self, dstip, mtu):
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.connect(hostname=self.host, username=self.user, password=self.psw)
        shell = sshClient.invoke_shell()
        print('登录设备：' + self.host + '\r\n')
        while True:
            cache = shell.recv(1000).decode()
            print(cache)
            if cache.endswith('#') == True:
                time.sleep(1)
                break  # 使用break跳出当前循环
            else:
                time.sleep(1)


        shell.sendall('ping ' + dstip + ' df-bit repeat 5 size ' + mtu + ' \r\n')
        while True:
            cache = shell.recv(1000).decode()
            print(cache)
            if cache.endswith('#') == True:
                time.sleep(1)
                break  # 使用break跳出当前循环
            else:
                time.sleep(1)

        x = re.compile('\r\nSuccess rate is (\d+) percent')
        reachable = x.findall(cache)[0]
        if reachable != '0':
            shell.sendall('ping ' + dstip + ' df-bit repeat 10000 size ' + mtu + ' \r\n')
            time.sleep(1)
            while True:
                cache = shell.recv(1000).decode()
                print(cache)
                if cache.endswith('#') == True:
                    time.sleep(1)
                    break  # 使用break跳出当前循环
                else:
                    time.sleep(1)
                    # print(cache)

            x = re.compile('Success rate is \d+ percent \((\d+/\d+)\), round-trip min/avg/max = \d+/(\d+)/\d+ ms')
            result = x.findall(cache)
            print('\033[32;0m可达率: ', result[0][0], '  平均延迟: ', result[0][1], 'ms\033[0m')
            # print(result)
            sshClient.close()
            # 返回列表，第一个元素为ping包可达率，第2个为平均延迟，单位ms
            return (result[0][0], result[0][1])
        else:
            print('\033[32;0m' + dstip + ', mtu: ', mtu, ' 不可达！\033[0m')
            sshClient.close()
            return('不可达！', dstip, mtu)



    def mtu_max(self, dstip):
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.connect(hostname=self.host, username=self.user, password=self.psw)
        shell = sshClient.invoke_shell()
        print('登录设备：' + self.host + '\r\n')
        time.sleep(1)
        while True:
            cache = shell.recv(1000).decode()
            print(cache)
            if cache.endswith('#') == True:
                time.sleep(1)
                break  # 使用break跳出当前循环
            else:
                time.sleep(1)


        for mtu in range(1200, 1501):
            shell.sendall('ping ' + dstip + ' df-bit repeat 5 size ' + str(mtu) + ' \r\n')
            time.sleep(1)

            while True:
                cache = shell.recv(1000).decode()
                print(cache)
                if cache.endswith('#') == True:
                    time.sleep(1)
                    break  # 使用break跳出当前循环
                else:
                    time.sleep(1)

            x = re.compile('\r\nSuccess rate is (\d+) percent')
            result = x.findall(cache)
            if result[0] == '0':

                # print(' unreachable mtu: ', mtu)
                print('\033[32;0munreachable mtu: ' + '\033[0m', mtu)
            else:
                print('\033[32;0mmtu=' + str(mtu) + ' ping success !! unreachable mtu: \033[0m')



# 使用示例： 声明NtwTools('登录设备管理地址', '用户名', '密码')
ntw_tools = NtwTools('10.0.2.211', 'esun21', 'Esun@1sh')

# 扫描mtu: ntw_tools.ping_mtu('目的地址')
mtu_unreach = ntw_tools.mtu_scan('172.168.194.242')
print(mtu_unreach)

# 扫描mtu: ntw_tools.ping_10000('目的地址'， 'mtu大小')
#p10000 = ntw_tools.ping_10000('172.168.194.242', '1500')
#print(p10000)
