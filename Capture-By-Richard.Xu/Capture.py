from scapy.all import rdpcap, DNS, DNSQR, DNSRR, IP

def extract_dns_info(pcap_file, target_ip):
    packets = rdpcap(pcap_file)
    dns_info = []

    for packet in packets:
        if packet.haslayer(IP) and packet[IP].dst == target_ip:
            if packet.haslayer(DNS):
                dns_layer = packet.getlayer(DNS)

                if dns_layer.qr == 0 and dns_layer.qd:  # This is a DNS query and qd is present
                    query_name = dns_layer.qd.qname.decode('utf-8')
                    dns_info.append({'Type': 'Query', 'Domain': query_name, 'Source IP': packet[IP].src, 'Destination IP': packet[IP].dst})

                elif dns_layer.qr == 1 and dns_layer.qd:  # This is a DNS response and qd is present
                    response_name = dns_layer.qd.qname.decode('utf-8')
                    if dns_layer.an:
                        for i in range(dns_layer.ancount):
                            answer = dns_layer.an[i]
                            if answer.type == 1:  # A record
                                dns_info.append({'Type': 'Response', 'Domain': response_name, 'Address': answer.rdata, 'Source IP': packet[IP].src, 'Destination IP': packet[IP].dst})
                            # elif answer.type == 5:  # CNAME record
                            #     dns_info.append({'Type': 'Response', 'Domain': response_name, 'CNAME': answer.rdata, 'Source IP': packet[IP].src, 'Destination IP': packet[IP].dst})

    return dns_info

# 示例使用
pcap_file = 'cu01.pcapng'
target_ip = '192.168.139.198'
dns_info = extract_dns_info(pcap_file, target_ip)
for info in dns_info:
    print(info)