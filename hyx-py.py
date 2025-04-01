from netmiko import ConnectHandler
import re
from pprint import pprint

# 设备连接信息
device = {
    "device_type": "fortinet",
    "host": "10.0.2.233",  # 替换为你的 FortiGate 设备 IP
    "username": "admin_esun21",
    "password": "Esun@1sh_Local",
}

# 连接 FortiGate 设备
with ConnectHandler(**device) as conn:
    # 进入全局模式
    conn.send_command("config global", expect_string=r"\(global\)\s#")

    # 获取 Internet Service Database (ISDB) ID 列表
    output = conn.send_command("diagnose internet-service id-summary")

    # 提取 ID（匹配 id: <数字>）
    ids = re.findall(r"id:\s*(\d+)", output)

    # 存储最终解析后的数据
    id_results = []

    # 实时查询并解析存储
    for id_ in ids:
        print(f"正在查询 ID: {id_}...", flush=True)

        cmd = f"diagnose internet-service id {id_}"
        result = conn.send_command(cmd, expect_string=r"\(global\)\s#", read_timeout=10)

        # 解析 IP 及其他信息
        entry_list = []
        for line in result.splitlines():
            match = re.match(
                r"([\d\.]+-[\d\.]+)\s+country\((\d+)\)\s+region\((\d+)\)\s+city\((\d+)\)\s+blocklist\((0x\d+)\)\s+"
                r"reputation\((\d+)\),\s+popularity\((\d+)\)\s+domain\((\d+)\)\s+botnet\((\d+)\)\s+proto\((\d+)\)\s+port\(([\d\s]+)\)",
                line
            )
            if match:
                entry = {
                    "ip_range": match.group(1),
                    "country": match.group(2),
                    "region": match.group(3),
                    "city": match.group(4),
                    "blocklist": match.group(5),
                    "reputation": match.group(6),
                    "popularity": match.group(7),
                    "domain": match.group(8),
                    "botnet": match.group(9),
                    "protocol": match.group(10),
                    "ports": match.group(11).split()  # 端口以列表存储
                }
                entry_list.append(entry)

        # 存入 ID 解析结果
        id_results.append({"id": id_, "entries": entry_list})

        # 实时输出解析后的数据
        print(f"ID: {id_} 解析完成，共 {len(entry_list)} 条记录\n{'-'*50}", flush=True)

print(f"所有 ID 解析完成，共 {len(id_results)} 个 ID.", flush=True)

print("所有 IP 信息(原始数据，列表形式)：")
pprint(entry_list)

print("\n处理后IP信息（字典格式）：")
pprint(id_results)