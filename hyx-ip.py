import netaddr

# ip1=netaddr.IPNetwork('2.144.0.0/14')
# ip2=netaddr.IPNetwork('2.176.0.0/12')
# print(ip1.hostmask)
# print(ip2.hostmask)

# ip_list = [netaddr.IPNetwork("2.144.0.0/16"), netaddr.IPNetwork("2.145.0.0/16")
#     , netaddr.IPNetwork("2.146.0.0/16"), netaddr.IPNetwork("2.147.0.0/16")]
# print(netaddr.cidr_merge(ip_list))

# ip = netaddr.iprange_to_cidrs("2.144.0.0", "2.147.255.255")
# print(ip)

from netaddr import IPNetwork

from ipaddress import ip_network


def summarize_networks(networks):
    """
    网段汇总函数
    :param networks: 网段列表，例如 ['192.168.1.0/24', '192.168.2.0/24']
    :return: 汇总后的网段列表
    """
    networks = [ip_network(net) for net in networks]
    # 将网段转换为集合，并进行汇总
    summarized_networks = [
        ip_network('/'.join(sum([list(net.supernet(i).explode()[1:3]) for i in range(net.supernet(1).prefixlen)], [])))
        for net in networks]
    return summarized_networks


# 示例使用
network_list = ['192.168.1.0/24', '192.168.2.0/24', '192.168.3.0/24', '192.168.0.0/16']
summarized_networks = summarize_networks(network_list)
for net in summarized_networks:
    print(net)




