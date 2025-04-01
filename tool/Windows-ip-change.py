import re
import subprocess
import os
import sys


def change_ip(interface_name, new_ip, subnet_mask, gateway=None, dns=None):
    try:
        # 构建命令字符串
        if gateway:
            command = f"netsh interface ipv4 set address name=\"{interface_name}\" static {new_ip} {subnet_mask} {gateway} 1"
        elif dns:
            command = f"netsh interface ipv4 set dnsservers name=\"{interface_name}\" static {dns} primary"
        else:
            command = f"netsh interface ipv4 set address name=\"{interface_name}\" static {new_ip} {subnet_mask}"
        # 执行命令
        os.system(command)
        print(f"{interface_name} 的IP地址已更改成功！")
    except Exception as e:
        print(f"发生错误：{e}")

def set_dhcp(interface_name):
    try:
        command1 = f"netsh interface ipv4 set address name=\"{interface_name}\" source=dhcp"
        command2 = f"netsh interface ipv4 set dns name=\"{interface_name}\" source=dhcp"
        # 执行命令
        os.system(command1)
        os.system(command2)
        print(f"成功将 {interface_name} 设置为使用 DHCP。")

    except subprocess.CalledProcessError as e:
        print(f"无法将 {interface_name} 设置为使用 DHCP：", e)

# 以管理员权限运行脚本
if sys.platform == 'win32':
    try:
        import ctypes
        # 尝试以管理员身份运行脚本
        if ctypes.windll.shell32.IsUserAnAdmin():
            print("当前已以管理员权限运行脚本。")
        else:
            print("当前未以管理员权限运行脚本。尝试重新以管理员权限运行脚本...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()
    except Exception as e:
        print(f"发生错误：{e}")

try:
    # 执行命令获取网卡信息
    result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
    # 解析输出，提取网卡名称和类型
    lines = result.stdout.split('\n')
    current_interface_name = None
    interface_name = []
    interface_desc = []
    for line in lines:
        if "适配器" in line:
            current_interface_name = line.split(':')[0].strip()
            com = re.compile('(?:(?:以太网适配器 )|(?:无线局域网适配器 ))(.*)')
            findname = com.findall(current_interface_name)
            for i in findname:
                interface_name.append(i)

        elif "描述" in line:
            interface_type = line.split(':')[1].strip()
            interface_desc.append(interface_type)

    print("可用的网卡列表：")
    for index, (name, desc) in enumerate(zip(interface_name, interface_desc), start=1):
        print(f"{index}. {name} - {desc}")

    # 选择要更改的网卡
    selected_index = int(input("\n请输入要更改IP地址的网卡序号: ")) - 1
    if selected_index < 0 or selected_index >= len(interface_name):
        print("输入无效的网卡序号。")
    else:
        selected_interface_name = interface_name[selected_index]

        # 选择IP地址设置方式
        option = int(input("\n请选择要更改的IP地址来源：\n1. 连接MT的88网段\n2. 使用 DHCP\n3. 自定义IP地址\n选择："))

        if option == 1:
            # 定义预定义的IP地址
            predefined_ip = "192.168.88.139"  # 此处更改为您的预定义IP地址
            subnet_mask = "255.255.255.0"
            gateway = ""  # 此处更改为您的网关地址
            dns = ""  # 此处更改为您的DNS地址
            change_ip(selected_interface_name, predefined_ip, subnet_mask, gateway, dns)

        elif option == 2:
            set_dhcp(selected_interface_name)

        elif option == 3:
            # 输入要更改的IP地址
            while True:
                new_ip = input("请输入新的IP地址: ")
                ip_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
                ip_find = ip_com.findall(new_ip)
                if ip_find:
                    break
                else:
                    print('IP格式错误，请重输!')
            subnet_mask = input("请输入子网掩码: ")
            while True:
                gateway = input("请输入网关地址（可选，直接按回车跳过）: ")
                gw_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
                gw_find = gw_com.findall(gateway)
                if gw_find:
                    break
                elif gateway == '':
                    break
                else:
                    print('Gateway 格式错误，请重输!')
            while True:
                dns = input("请输入DNS地址（可选，直接按回车跳过）: ")
                dns_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
                dns_find = dns_com.findall(dns)
                if dns_find:
                    break
                elif dns == '':
                    break
                else:
                    print('DNS 格式错误，请重输!')
            if gateway == "" and dns == "":
                change_ip(selected_interface_name, new_ip, subnet_mask)
            elif dns == "":
                change_ip(selected_interface_name, new_ip, subnet_mask, gateway)
            else:
                change_ip(selected_interface_name, new_ip, subnet_mask, gateway, dns)

        else:
            print("无效的选择。")

except Exception as e:
    print(f"发生错误：{e}")
Done = input('输入回车结束脚本')
