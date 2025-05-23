import re
import time

device_id = input('Enter device id:')
customer = input('Enter customer name:')
while True:
    city = input('Enter device city:')
    if len(city) > 6:
        print('Length greater than 6 bytes，Plz re-enter!')
    elif len(city) == 0:
        print('Cannot be empty,Plz re-enter!')
    else:
        break
while True:
    Mgmt = input('Enter Mgmt ip:')
    Mgmt_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    Mgmt_find = Mgmt_com.findall(Mgmt)
    if Mgmt_find:
        break
    else:
        print('IP address format error,Please re-enter!')
tunnel_id = input('Enter tunnel id:')
while True:
    tunnel_ip = input('Enter tunnel ip:')
    tunnel_ip_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    tunnel_ip_find = tunnel_ip_com.findall(tunnel_ip)
    if tunnel_ip_find:
        break
    else:
        print('IP address format error,Please re-enter!')
tunnelip_fir = re.compile('(\d+\.\d+\.\d+\.)\d+')
tunnelip_end = re.compile('\d+\.\d+\.\d+\.(\d+)')
tunnelip_fir_find = tunnelip_fir.findall(tunnel_ip)
for tu_content in tunnelip_fir_find:
    tufir = tu_content
tunnelip_end_find = tunnelip_end.findall(tunnel_ip)
for tulast_content in tunnelip_end_find:
    tuend = tulast_content
tuend_1 = int(tuend)-1
tuip = str(tufir)+str(tuend_1)
connected = input('Is there an interconnected address? 1.yes 2.no\n')
if connected == '1':
    while True:
        con_ip = input('Enter connected IP:')
        con_ip_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        con_ip_find = con_ip_com.findall(con_ip)
        if con_ip_find:
            break
        else:
            print('IP address format error,Please re-enter!')
    con_gw = input('Enter connected gw:')
    cust_gw = input('Enter customer gw:')
    cust_netmask = input('Enter customer netmask:')
    print('')
    print('')
    print('CE配置如下：')
    print('ip address ' + con_ip + ' 255.255.255.252')
    print('no shutdown')
    print('exit')
    print('ip route 0.0.0.0 0.0.0.0 ' + con_gw)
    print('interface vlan 10')
    print('ip address ' + cust_gw + ' ' + cust_netmask)
    print('interface range gigabitEthernet 0/1/0-3')
    print('swi mode acce')
    print('swi acc vlan 10')
    print('no shutdown')
    print('exit')
    print('!')
else:
    while True:
        gw = input('Enter ISP GW:')
        gw_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        gw_find = gw_com.findall(gw)
        if gw_find:
            break
        else:
            print('IP address format error,Please re-enter!')
    netmask = input('Enter netmask:')
    print('ip route 0.0.0.0 0.0.0.0 ' + gw)
    gw_fir = re.compile('(\d+\.\d+\.\d+\.)\d+')
    gw_end = re.compile('\d+\.\d+\.\d+\.(\d+)')
    gw_fir_find = gw_fir.findall(gw)
    for i_content in gw_fir_find:
        i = i_content
    gw_end_find = gw_end.findall(gw)
    for j_content in gw_end_find:
        j = j_content
    gwend_1 = int(j)+1
    gwend_2 = int(j)+2
    gwend_3 = int(j)+3
    gwend_4 = int(j)+4
    gwend_5 = int(j)+5
    print('')
    print('')
    print('CE配置如下：')
    print('int g0/0/0')
    print('ip address ' + i + str(gwend_1) + ' ' + netmask)
    print('no shutdown')
    print('int vlan 10')
    print('ip unnumbered GigabitEthernet0/0/0')
    print('no shutdown')
    print('interface range gigabitEthernet 0/1/0-3')
    print('swi mode acce')
    print('swi acc vlan 10')
    print('no shutdown')
    print('exit')
    print('!')
    print('ip route ' + i + str(gwend_2) + ' ' + '255.255.255.255 ' + 'vlan 10')
    print('ip route ' + i + str(gwend_3) + ' ' + '255.255.255.255 ' + 'vlan 10')
    print('ip route ' + i + str(gwend_4) + ' ' + '255.255.255.255 ' + 'vlan 10')
    print('ip route ' + i + str(gwend_5) + ' ' + '255.255.255.255 ' + 'vlan 10')
    print('!')
print('ip vrf Mgmt')
print('exit')
print('hostname cn-' + customer + '-' + city + '-ce-' + device_id)
print('int loo 0')
print('ip vrf forwarding Mgmt')
print('ip address ' + Mgmt + ' 255.255.255.255')
print('description *** to null null null ps:Mgmt ***')
print('exit')
print('!')
print('no ip domain-lookup')
print('!')
print('aaa new-model')
print('aaa group server tacacs+ Esun_TAC')
print('server-private 10.200.0.246 key 7 05080F1C2243')
print('server-private 10.200.2.246 key 7 05080F1C2243')
print('ip vrf forwarding Mgmt')
print('ip tacacs source-interface loo0')
print('aaa authentication password-prompt "Tacacs no reachable - Enter local password:"')
print('aaa authentication username-prompt "Tacacs no reachable - Enter local username:"')
print('aaa authentication login default group Esun_TAC local-case')
print('aaa authentication enable default group Esun_TAC enable')
print('aaa authorization exec default group Esun_TAC local')
print('aaa authorization commands 15 default group Esun_TAC local')
print('aaa accounting exec default')
print('action-type start-stop')
print('group Esun_TAC')
print('aaa accounting commands 15 default')
print('action-type stop-only')
print('group Esun_TAC')
print('aaa session-id common')
print('!')
print('interface tunnel ' + tunnel_id)
print('description *** to cn-esu-shangh-gw-05 null null ps:Mgmt ***')
print('ip vrf forwarding Mgmt')
print('ip address ' + tunnel_ip + ' 255.255.255.252')
print('tunnel source gigabitEthernet 0/0/0')
print('tunnel destination 103.204.72.53')
print('exit')
print('!')
print('ip route vrf Mgmt 10.200.0.224 255.255.255.224 ' + tuip + ' name ***To-Esun-Monitoring-Server01***')
print('ip route vrf Mgmt 10.200.2.224 255.255.255.224 ' + tuip + ' name ***To-Esun-Monitoring-Server02***')
print('!')
print('ip domain-name cn-' + customer + '-' + city + '-ce-' + device_id)
print('!')
print('crypto key generate rsa modulus 1024')
print('username esunadmin privilege 15 password 7 01361511552B571C29')
print('enable password 7 002100130A7B5A1507')
print('!')
print('archive')
print('path ftp://admin_esun21@10.200.2.250/Esun_INTERNET_Config/$\h-')
print('write-memory')
print('exit')
print('!')
print('ip ftp source-interface Loopback0')
print('ip ftp username admin_esun21')
print('ip ftp password Esun@1sh_LocalAdmin')
print('ip ftp source-interface loopback 0')
print('!')
print('logging trap debugging')
print('logging source-interface Loopback0')
print('logging 10.200.2.238')
print('logging 10.200.0.238')
print('logging 10.200.0.250')
print('login on-success log')
print('!')
print('snmp-server community esun-esu-cn RW 60')
print('snmp-server trap-source Loopback0')
print('snmp-server contact 1st Level Service Desk Shanghai (freecall:  86 21 23135955)')
print('snmp-server host 10.200.0.254 255.255.255.248')
print('snmp-server host 10.200.2.254 255.255.255.248')
print('!')
print('line vty 0 15')
print('access-class 63 in vrf-also')
print('exec-timeout 5 10')
print('logging synchronous')
print('transport input ssh')
print('exit')
print('!')
print('ntp logging')
print('ntp source Loopback0')
print('ntp server 10.200.2.238')
print('ntp server 10.200.0.238')
print('clock timezone GTM 8')
print('!')
print('access-list 60 permit 10.200.0.242')
print('access-list 60 permit 10.200.2.250')
print('access-list 60 permit 10.200.0.254')
print('access-list 60 permit 10.200.2.254')
print('access-list 63 permit 10.200.0.224 0.0.0.31')
print('access-list 63 permit 10.200.2.224 0.0.0.31')
print('access-list 63 permit ' + tuip + ' 0.0.0.3')
print('exit')
print('!')
print('write')
input('Enter any to exit!')