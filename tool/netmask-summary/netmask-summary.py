import ipaddress


def read_subnets_from_file(filename):
    """从TXT文件中读取子网列表"""
    with open(filename, "r") as file:
        subnets = [line.strip() for line in file if line.strip()]
    return subnets


def summarize_subnets(subnets):
    """精确汇总子网，不引入额外的路由"""
    subnet_objects = [ipaddress.ip_network(subnet, strict=False) for subnet in subnets]
    subnet_objects.sort(key=lambda x: (x.network_address, x.prefixlen))

    summarized = []

    for subnet in subnet_objects:
        if not summarized:
            summarized.append(subnet)
            continue

        last_subnet = summarized[-1]

        # 检查是否可以合并
        if last_subnet.supernet().prefixlen == last_subnet.prefixlen - 1 and last_subnet.supernet() == subnet.supernet():
            summarized[-1] = last_subnet.supernet()  # 合并到更大的子网
        else:
            summarized.append(subnet)  # 不能合并，单独存储

    return [str(subnet) for subnet in summarized]


# 运行脚本
filename = "AWS-IP.txt"
subnets = read_subnets_from_file(filename)
result = summarize_subnets(subnets)

print("精确汇总后的子网:")
for subnet in result:
    print(subnet)
