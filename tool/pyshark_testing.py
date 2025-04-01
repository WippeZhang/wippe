import pyshark
from tkinter import Tk, filedialog
from pprint import pprint

# 使用 Tkinter 文件对话框处理文件选择的函数
def select_file():
    root = Tk()
    root.withdraw()  # 隐藏主窗口

    file_path = filedialog.askopenfilename(
        title="选择 PCAP 文件", filetypes=[("PCAP 文件", "*.pcap"), ("所有文件", "*.*")]
    )

    return file_path

# 调用 select_file 函数选择 pcap 文件
pcap_file = select_file()

cap = pyshark.FileCapture(pcap_file)

# 遍历每个数据包

# 使用字典按目的IP地址分组源IP地址
dest_to_source = []
# 使用字典按源IP地址分组目的IP地址
source_to_dest = []
src_dst_ips = []

# for packet in cap:
#     try:
#         if 'IP' in packet:
#             # print('源IP：' + packet.ip.src + ' 目的IP：' + packet.ip.dst)
#             source_ip = packet.ip.src
#             dest_ip = packet.ip.dst
#             src_dst_ip = (packet.ip.src, packet.ip.dst)
#             src_dst_ips.append(src_dst_ip)
#
#     except:
#         pass
# for i in src_dst_ips:
#     print(i[0], i[1])
for packet in cap:
    try:
        if 'IP' in packet:
            # print('源IP：' + packet.ip.src + ' 目的IP：' + packet.ip.dst)
            source_ip = packet.ip.src
            dest_ip = packet.ip.dst
            src_dst_ip = (packet.ip.src, packet.ip.dst)
            src_dst_ips.append(src_dst_ip)

    except:
        pass
last_list = []
for i in src_dst_ips:
    if i in last_list:
        pass
    else:
        last_list.append(i)


sorted_data = sorted(last_list, key=lambda x: x[0])
# print(sorted_data)
# 创建字典进行汇总
summary_dict = {}

for first, second in sorted_data:
    if first not in summary_dict:
        summary_dict[first] = set()
    summary_dict[first].add(second)

# 输出汇总结果
sec_sum = {}
list_sum = list(summary_dict.items())


# 创建字典进行汇总
summary_dict = {}

for ip, ip_set in list_sum:
    # 将集合转换为元组
    ip_set_tuple = tuple(ip_set)
    # 将第二个元素作为键，第一个元素作为值，进行汇总
    if ip_set_tuple not in summary_dict:
        summary_dict[ip_set_tuple] = set()
    summary_dict[ip_set_tuple].add(ip)

# 输出汇总结果
for ip_set_tuple, ips in summary_dict.items():
    print(f"源IP: {', '.join(ips)}, 目的IP: {', '.join(ip_set_tuple)}")

