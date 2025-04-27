import ipaddress

def convert_cidr_to_netmask(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            cidr = line.strip()
            try:
                # 创建一个IPv4接口对象
                interface = ipaddress.ip_interface(cidr)
                # 获取IP地址和子网掩码
                ip_address = interface.ip
                netmask = interface.netmask
                print("ios_config " + '''"ip route ''' + f"{ip_address} {netmask}" + ''' 10.0.39.254"''')
            except ValueError as e:
                print(f"无效的CIDR表示法 '{cidr}': {e}")

# 示例用法
file_path = 'AWS-IP.txt'  # 替换为您的文件路径
convert_cidr_to_netmask(file_path)
