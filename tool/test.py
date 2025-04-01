from collections import defaultdict
import ipaddress
import pyshark

# 打开PCAP文件
pcap_file = "tls.pcap"
capture = pyshark.FileCapture(pcap_file)

# 使用字典按目的IP地址分组源IP地址
dest_to_source = defaultdict(list)
for packet in capture:
    try:
        if "IP" in packet:
            source_ip = packet.ip.src
            dest_ip = packet.ip.dst
            dest_to_source[dest_ip].append(source_ip)
    except:
        pass

# 关闭文件捕获
capture.close()

# 对每个目的IP地址的源IP地址列表进行汇总
summarized_networks = {}
for dest_ip, source_ips in dest_to_source.items():
    networks = [ipaddress.IPv4Network(ip) for ip in source_ips]
    summarized_network = ipaddress.collapse_addresses(networks)

    # 将CIDR前缀长度设置为/24
    summarized_network_with_prefix = []
    for net in summarized_network:
        summarized_network_with_prefix.append(net.supernet(new_prefix=24))

    summarized_networks[dest_ip] = summarized_network_with_prefix

# 打印汇总后的网络
print("Summarized networks for source IPs:")
for dest_ip, network in summarized_networks.items():
    print("Destination IP:", dest_ip)
    for net in network:
        print("  Source IP range:", net)
