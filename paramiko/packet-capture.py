import paramiko
from io import StringIO
import time
import re
import routeros_api
import datetime


class Capture:
    def __init__(self):
        self.name = None
        self.src = None
        self.destination = None
        self.num = None
        self.interface = None
        self.direction = None
        self.l = None
        self.cli = None
        self.end_mark_cisco = None
        self.end_mark_Huawei = None
        self.result = None
        self.acl_name = None
        self.acl_src = None
        self.acl_des = None
        self.cap_num = None
        self.cap_dir = None
        self.cap_interface = None
        self.cap_name = None
        self.cap_time = None
        self.host = None
        self.interface = None
        self.ip_add = None
        self.protocol = None
        self.port = None
        self.mikrotik_yes_or_no = None

    @classmethod
    def device_choice(self):
        self.mikrotik_yes_or_no = input('是否是对Microtik进行抓包,回答Yes / No:')

    @classmethod
    def login_mikrotik(self):
        if self.mikrotik_yes_or_no == 'Yes' or self.mikrotik_yes_or_no == 'yes' or self.mikrotik_yes_or_no == 'y':
            while True:
                self.host = input('请输入需要访问的设备管理地址：')
                host_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
                host_find = host_com.findall(self.host)
                if host_find:
                    break
                else:
                    print('IP地址格式错误，请重输！')
            self.connection = routeros_api.RouterOsApiPool(self.host, username='admin_esun21', password='Esun21#_Spoke',plaintext_login=True)
            self.api = self.connection.get_api()

    @classmethod
    def login(self):
        if self.mikrotik_yes_or_no == 'No' or self.mikrotik_yes_or_no == 'no' or self.mikrotik_yes_or_no == 'n':
            key = paramiko.RSAKey.from_private_key_file(filename="wippe.pem", password='gMz0qFGOvvauS_ql')
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname='10.0.90.85', port=22, username='wippe', compress=True, allow_agent=False,look_for_keys=False, pkey=key)

            self.cli = ssh_client.invoke_shell(width=999, height=9999)
            self.cli.send("\n")
            time.sleep(1)
            self.end_mark_cisco = '#'
            self.end_mark_Huawei = '<'
            self.result = self.cli.recv(65535).decode()
            # print(result)
            hostname = input('请输入设备hostname：')

            self.cli.send(hostname + '\n')
            time.sleep(2)
            self.result = self.cli.recv(65535).decode()
            red = re.sub(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)', r'\033[91m\1\033[0m', self.result)
            print(red)
            while True:
                if '输入ID或者其它帮助信息>:' in self.result:
                    hostname = input('请输入设备hostname/id：')
                    self.cli.send(hostname + '\n')
                    time.sleep(2)
                    self.result = self.cli.recv(65535).decode()
                    red = re.sub(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)', r'\033[91m\1\033[0m', self.result)
                    print(red)
                else:
                    break
            self.cli.send('wippe\n')
            time.sleep(1)
            self.cli.send('z010808\n')
            time.sleep(1)
            self.cli.send("\n")
            time.sleep(8)
            self.result = self.cli.recv(65535).decode()
            # print(result)


    @classmethod
    def device_get_interface(self):
        if self.mikrotik_yes_or_no == 'No' or self.mikrotik_yes_or_no == 'no' or self.mikrotik_yes_or_no == 'n':
            if self.end_mark_cisco in self.result:
                self.cli.send(b"terminal length 0\n")
                time.sleep(1)
                self.cli.send("show int des\n")
                time.sleep(3)
                result_int = self.cli.recv(65535).decode()
                # print(result)
                res = result_int.split('\n')
                for l in res:
                    print(l)
            if self.end_mark_Huawei in self.result:
                self.cli.send("display interface description | no-more\n")
                time.sleep(3)
                hw_result = self.cli.recv(65535).decode()
                # print(result)
                res = hw_result.split('\n')
                for l1 in res:
                    print(l1)


    @classmethod
    def cisco_get_input(self):
        if self.mikrotik_yes_or_no == 'No' or self.mikrotik_yes_or_no == 'no' or self.mikrotik_yes_or_no == 'n':
            if self.end_mark_cisco in self.result:
                while True:
                    self.name = input('请输入想要抓包的文件名称(less than or equal to 8 characters and only (_))：')
                    if len(self.name) > 8:
                        print('文件名称长度大于8,请重新输入：')
                    elif len(self.name) == 0:
                        print('文件名称不可为空，请重输！')
                    elif '!' in self.name or '@' in self.name or '#' in self.name or '$' in self.name or '%' in self.name or '^' in self.name or '&' in self.name or '*' in self.name or '(' in self.name or ')' in self.name or '-' in self.name or '+' in self.name or '=' in self.name:
                        print("只能使用'_'这一种特殊字符，请重新输入：")
                    else:
                        break
                self.interface = input('请输入想要抓包的接口：')
                self.direction = input('请输入想要抓的流量方向<both/in/out>：')
                while True:
                    self.num = input('请输入想要抓包的数量<1-10000>：')
                    if re.match('\D+', self.num):
                        print('只能使用数字，请再次输入：')
                    elif int(self.num) > 10000:
                        print('数量过大，请重输！')
                    elif int(self.num) == 0:
                        print('数量不可为0，请重输！')
                    else:
                        break
                while True:
                    self.src = input('请输入源IP<A.B.C.D/nn or any>：')
                    src_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\/)(?:[0-9]|[1-2][0-9]|3[0-2])$")
                    src_find = src_com.findall(self.src)
                    if src_find:
                        break
                    elif 'any' in self.src:
                        break
                    else:
                        print('IP格式错误，重新输入：')
                while True:
                    self.destination = input('请输入目的IP<A.B.C.D/nn or any>：')
                    des_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\/)(?:[0-9]|[1-2][0-9]|3[0-2])$")
                    des_find = des_com.findall(self.destination)
                    if des_find:
                        break
                    elif 'any' in self.destination:
                        break
                    else:
                        print('IP格式错误，重新输入：')

    @classmethod
    def cisco_capture(self):
        if self.mikrotik_yes_or_no == 'No' or self.mikrotik_yes_or_no == 'no' or self.mikrotik_yes_or_no == 'n':
            if self.end_mark_cisco in self.result and '-sw-' in self.result:
                if self.name is not None and self.interface is not None and self.direction is not None and self.num is not None and self.src is not None and self.src is not None and self.destination is not None:
                    now = datetime.datetime.now()
                    ciscotime = now.strftime("%Y%m%d_%H%M%S")
                    self.cli.send('monitor capture ' + self.name + ' interface ' + self.interface + ' ' + self.direction + ' limit packet-len 1518 packets ' + self.num + '\n')
                    time.sleep(1)
                    self.cli.send('monitor capture ' + self.name + ' match ipv4 ' + self.src + ' ' + self.destination + '\n')
                    time.sleep(1)
                    self.cli.send('monitor capture ' + self.name + ' file location flash:' + self.name + '.pcap buffer-size 10\n')
                    time.sleep(1)
                    self.cli.send('monitor capture ' + self.name + ' start' + '\n')
                    time.sleep(15)
                    self.cli.send('monitor capture ' + self.name + ' stop' + '\n')
                    time.sleep(1)
                    self.cli.send('copy flash:' + self.name + '.pcap ftp://admin_esun21@10.200.2.250/capture/' + self.name + '_' + ciscotime + '.pcap\n')
                    time.sleep(5)
                    self.cli.send('\n')
                    time.sleep(1)
                    self.cli.send('\n')
                    time.sleep(1)
                    self.cli.send('no monitor capture ' + self.name + '\n')
                    time.sleep(1)
                    self.cli.send('delete flash:' + self.name + '.cap\n')
                    time.sleep(1)
                    self.cli.send('\n')
                    time.sleep(1)
                    self.cli.send('\n')
                    time.sleep(1)
                    result1 = self.cli.recv(65535).decode()
                    # print(result)
                    res1 = result1.split('\n')
                    for l1 in res1:
                        print(l1)
                    self.cli.close()
            elif self.end_mark_cisco in self.result:
                now = datetime.datetime.now()
                ciscotime = now.strftime("%Y%m%d_%H%M%S")
                self.cli.send('monitor capture ' + self.name + ' interface ' + self.interface + ' ' + self.direction + ' limit packet-len 1518 packets ' + self.num + '\n')
                time.sleep(1)
                self.cli.send('monitor capture ' + self.name + ' match ipv4 ' + self.src + ' ' + self.destination + '\n')
                time.sleep(1)
                self.cli.send('monitor capture ' + self.name + ' start' + '\n')
                time.sleep(15)
                self.cli.send('monitor capture ' + self.name + ' stop' + '\n')
                time.sleep(1)
                self.cli.send('monitor capture ' + self.name + ' export ftp://admin_esun21@10.200.2.250/capture/' + self.name + '_' + ciscotime + '.pcap' + '\n')
                time.sleep(5)
                self.cli.send('no monitor capture ' + self.name + '\n')
                time.sleep(1)
                result1 = self.cli.recv(65535).decode()
                # print(result)
                res1 = result1.split('\n')
                for l1 in res1:
                    print(l1)
                self.cli.close()

    @classmethod
    def huawei_get_input(self):
        if self.mikrotik_yes_or_no == 'No' or self.mikrotik_yes_or_no == 'no' or self.mikrotik_yes_or_no == 'n':
            if self.end_mark_Huawei in self.result:
                while True:
                    self.acl_name = input('请输入抓包所用acl的名称STRING<1-64>：')
                    if len(self.acl_name) > 64:
                        print('acl名称长度超过64，请重输！')
                    elif len(self.acl_name) == 0:
                        print('名称长度不可为空，请重输！')
                    else:
                        break
                while True:
                    self.acl_src = input('请输入源IP<x.x.x.x xx / any>：')
                    acl_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\s)(?:[0-9]|[1-2][0-9]|3[0-2])$")
                    acl_find = acl_com.findall(self.acl_src)
                    if acl_find:
                        break
                    elif 'any' in self.acl_src:
                        break
                    else:
                        print('IP格式错误，请重输!')
                while True:
                    self.acl_des = input('请输入目的IP<x.x.x.x xx / any>：')
                    acl_des_com = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\s)(?:[0-9]|[1-2][0-9]|3[0-2])$")
                    acl_des_find = acl_des_com.findall(self.acl_des)
                    if acl_des_find:
                        break
                    elif 'any' in self.acl_des:
                        break
                    else:
                        print('IP格式错误，请重输！')
                self.cap_interface = input('请输入捕获的接口(支持直接输入HGC/HKIX/NTT/GTT)：')
                if self.cap_interface == 'cn2' or self.cap_interface == 'CN2' or self.cap_interface == 'Cn2':
                    self.cap_interface = 'g0/3/7'
                elif self.cap_interface == 'HGC' or self.cap_interface == 'hgc' or self.cap_interface == 'Hgc':
                    self.cap_interface = 'g0/3/4'
                elif self.cap_interface == 'HKIX' or self.cap_interface == 'hkix' or self.cap_interface == 'Hkix':
                    self.cap_interface = 'g0/3/12'
                elif self.cap_interface == 'NTT' or self.cap_interface == 'ntt' or self.cap_interface == 'Ntt':
                    self.cap_interface = 'g0/3/7'
                elif self.cap_interface == 'GTT' or self.cap_interface == 'gtt' or self.cap_interface == 'Gtt':
                    self.cap_interface = 'g0/3/4'
                while True:
                    self.cap_dir = input('请输入捕获的方向<in or out>：')
                    if self.cap_dir == 'i' or self.cap_dir == 'in':
                        self.cap_dir = 'inbound'
                        break
                    elif self.cap_dir == 'o' or self.cap_dir == 'ou' or self.cap_dir == 'out':
                        self.cap_dir = 'outbound'
                        break
                    else:
                        print('方向填写错误，请重输！')
                while True:
                    self.cap_num = input('请输入包的数量<1-1000>：')
                    if re.match('\D+', self.cap_num):
                        print('只能使用数字，请重输！')
                    elif int(self.cap_num) > 1000:
                        print('数量过大，请重输！')
                    elif int(self.cap_num) == 0:
                        print('数量不可以等于0，请重输！')
                    else:
                        break
                while True:
                    self.cap_time = input('请输入抓包时间<1-86400>：')
                    if re.match('\D+', self.cap_time):
                        print('只能使用数字，请重输！')
                    elif int(self.cap_time) == 0:
                        print('时间不可等于0，请重输！')
                    elif int(self.cap_time) > 86400:
                        print('时间过大，请重输！')
                    else:
                        break
                while True:
                    self.cap_name = input('请输入抓包文件名称STRING<5-64>：')
                    if 5 <= len(self.cap_name) <= 64:
                        break
                    else:
                        print('名称不符合规范，请重输！')


    @classmethod
    def huawei_capture(self):
        if self.mikrotik_yes_or_no == 'No' or self.mikrotik_yes_or_no == 'no' or self.mikrotik_yes_or_no == 'n':
            if self.end_mark_Huawei in self.result:
                if self.acl_name is not None and self.acl_src is not None and self.acl_des is not None and self.cap_interface is not None and self.cap_dir is not None and self.cap_num is not None and self.cap_time is not None and self.cap_name is not None:
                    now = datetime.datetime.now()
                    huaweitime = now.strftime("%Y%m%d_%H%M%S")
                    self.cli.send('sys\n')
                    time.sleep(1)
                    self.cli.send('acl name ' + self.acl_name + ' advance'+'\n')
                    time.sleep(1)
                    self.cli.send('rule permit ip source ' + self.acl_src + ' destination ' + self.acl_des + '\n')
                    time.sleep(1)
                    self.cli.send('commit' + '\n')
                    time.sleep(3)
                    self.cli.send('quit' + '\n')
                    time.sleep(1)
                    self.cli.send('capture-packet forwarding interface ' + self.cap_interface + ' ' + self.cap_dir + ' acl name ' + self.acl_name + ' packet-len 64 ' + 'packet-num ' + self.cap_num + ' time-out ' + self.cap_time + ' file ' + self.cap_name + '.cap' + '\n')
                    time.sleep(int(self.cap_time))
                    self.cli.send('quit' + '\n')
                    time.sleep(1)
                    self.cli.send('ftp 10.200.2.250 vpn-instance Mgmt-intf'+'\n')
                    time.sleep(3)
                    self.cli.send('admin_esun21' + '\n')
                    time.sleep(1)
                    self.cli.send('Esun@1sh_LocalAdmin' + '\n')
                    time.sleep(1)
                    self.cli.send('put /logfile/' + self.cap_name + '.cap ' + 'capture/' + self.cap_name + '_' + huaweitime + '.pcap' + '\n')
                    time.sleep(3)
                    self.cli.send('quit' + '\n')
                    time.sleep(1)
                    self.cli.send('delete /logfile/' + self.cap_name + '.pcap' + '\n')
                    time.sleep(2)
                    self.cli.send('y' + '\n')
                    time.sleep(3)
                    self.cli.send('sys' + '\n')
                    time.sleep(1)
                    self.cli.send('undo acl name ' + self.acl_name + '\n')
                    time.sleep(1)
                    self.cli.send('commit' + '\n')
                    time.sleep(3)
                    hw_result1 = self.cli.recv(65535).decode()
                    # print(result)
                    res1 = hw_result1.split('\n')
                    for l1 in res1:
                        print(l1)
                    self.cli.close()


    @classmethod
    def mikrotik_get_input(self):
        if self.mikrotik_yes_or_no == 'Yes' or self.mikrotik_yes_or_no == 'yes' or self.mikrotik_yes_or_no == 'y':
            list_interface = self.api.get_resource('/interface')
            int_list = []
            for i in list_interface.get():
                if i.get('running') == 'true':
                    print(i['name'], 'comment:', i.get('comment'))
                    int_list.append(i['name'])

            list_hostname = self.api.get_resource('/system/identity')
            for h in list_hostname.get():
                self.device_hostname = (h['name'])
                # print(device_hostname)

            list_date = self.api.get_resource('/system/clock')
            for d in list_date.get():
                self.device_date = d['date']
                # print(d['date'])
                month_com = re.compile('(\D+)\/')
                date_com = re.compile('\D+\/(\d+)')
                self.month_findall = month_com.findall(self.device_date)
                self.date_findall = date_com.findall(self.device_date)
                # print(month_findall[0])
                # print(date_findall[0])
            print('-------------------------------------------------------------------------')
            print('填写规则：直接回车置为空，直接写为单个值，若需要多个值中间请以[,]作为间隔')
            while True:
                self.interface = input('请输入接口：')
                if self.interface in int_list:
                    break
                elif self.interface == '':
                    break
                else:
                    print('接口填写错误，请重输！')

            while True:
                self.ip_add = input('请输入需要抓的ip地址：')
                ip_add_com = re.compile("^(?:\!?)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\/)(?:[0-9]|[1-2][0-9]|3[0-2])$")
                ip_add_findall = ip_add_com.findall(self.ip_add)
                if ip_add_findall:
                    break
                elif self.ip_add == '':
                    break
                else:
                    print('请输入正确的ip地址！')

            while True:
                self.protocol = input('请输入需要抓的协议<icmp/igmp/ggp/ip-encap/tcp/egp/pup/udp/ipsec/ospf>：')
                if self.protocol == '!':
                    print('不允许只写!,请重输！')
                elif '!' in self.protocol or 'icmp' in self.protocol or 'igmp' in self.protocol or 'ggp' in self.protocol or 'ip-encap' in self.protocol or 'tcp' in self.protocol or 'egp' in self.protocol or 'pup' in self.protocol or 'udp' in self.protocol or 'ipsec' in self.protocol or 'ospf' in self.protocol:
                    break
                elif self.protocol == '':
                    break
                else:
                    print('协议不支持，请重输！')

            port_list = ['', 'acap', 'epmap', 'liquidaudio', 'pcanywheredata', 'sql-net', 'activision', 'eppc', 'lotusnote',
                         'pcanywherestat', 'squid', 'afpovertcp', 'esro-emsdp', 'lpr', 'pdap-np', 'ssh', 'agentx',
                         'esro-gen', 'mac-srvr-admin', 'pgp5-key', 'statsrv', 'aol', 'etftp', 'madcap', 'photuris',
                         'sunrpc', 'apple-licman', 'fcp-addr-srvr1', 'matip-type-a', 'pop2', 'supdup', 'appleqtc',
                         'fcp-addr-srvr2', 'matip-type-b', 'pop3', 'swat', 'appleqtcsrvr', 'fcp-cics-gw1', 'mc-ftp',
                         'pop3s', 'syslog', 'appleugcontrol', 'fcp-srvr-inst1', 'mgcp-callagent', 'poppassd', 'systat',
                         'arcp', 'fcp-srvr-inst2', 'mgcp-gateway', 'pptp', 't.120', 'asia', 'finger', 'microcom-sbp',
                         'prospero-np', 'tacacs', 'asip-webadmin', 'ftp', 'mobileip', 'pwdgen', 'talk', 'asipregistry',
                         'ftp-data', 'mountd', 'qotd', 'tcp-id-port', 'aurp', 'glimpse', 'mpp', 'quake', 'tcpmux', 'auth',
                         'gopher', 'ms-rpc', 'quake-world', 'telnet', 'avt-profile-1', 'h323gatestat', 'ms-sql-m', 'quake3',
                         'tftp', 'avt-profile-2', 'h323hostcall', 'ms-sql-s', 'radius', 'tftp-mcast', 'bdp', 'half-life',
                         'ms-streaming', 'radius-acct', 'timbuktu', 'bftp', 'hbci', 'ms-wbt-server', 'rap', 'timbuktu-srv1',
                         'bgp', 'hostname', 'msbd', 're-mail-ck', 'timbuktu-srv2', 'biff', 'hotsync-1', 'msg-auth',
                         'realsecure', 'timbuktu-srv3', 'bootpc', 'hotsync-2', 'msg-icp', 'reftek', 'timbuktu-srv4',
                         'bootps', 'hsrp', 'msql', 'rip', 'time', 'btserv', 'htcp', 'mtp', 'ripng', 'tinc', 'buddyphone',
                         'http', 'mysql', 'rje', 'tlisrv', 'ccmail', 'http-alt', 'mzap', 'rlogin', 'uls', 'cfdptkt',
                         'https', 'name', 'rlp', 'unreal', 'chargen', 'ica', 'napster', 'rrp', 'uucp-path', 'cops',
                         'icabrowser', 'napster-2', 'rsvp-tunnel', 'vemmi', 'cpq-wbem', 'icpv2', 'napster-3', 'rtp',
                         'veracity', 'csnet-ns', 'icq', 'net-assistant', 'rtsp', 'virtualuser', 'daytime', 'imail-www',
                         'netbios-dgm', 'rwhois', 'vmnet', 'dict', 'imap3', 'netbios-ns', 'rwp', 'vnc-1', 'discard',
                         'imaps', 'netbios-ssn', 'secureid', 'vnc-2', 'discovery', 'ipp', 'netrek', 'sftp', 'webobjects',
                         'distributed-net', 'irc', 'netstat', 'sgmp', 'whois++', 'dixie', 'ircu', 'nextstep', 'sift-uft',
                         'winbox', 'dlsrap', 'isakmp', 'nfile', 'sip', 'winbox-old', 'dlsrpn', 'iso-tsap', 'nfs', 'slmail',
                         'winbox-old-tls', 'dlswpn', 'kerberos', 'nicname', 'smb', 'wingate', 'dns', 'klogin', 'nntp',
                         'smtp', 'wlbs', 'dns2go', 'l2tp', 'nntps', 'smux', 'x11', 'doom', 'ldap', 'ntp', 'snmp', 'xdmcp',
                         'dsp', 'ldaps', 'odette-ftp', 'snpp', 'yahoo', 'dtspcd', 'link', 'odmr', 'socks', 'z39.50', 'echo',
                         'linuxconf', 'oracle-sql', 'sql*net', '!']
            while True:
                self.port = input('请输入需要抓的端口:')
                if self.port == '!':
                    print('不允许只写!,请重输！')
                elif self.port in port_list:
                    break
                elif re.match('(?:^(\!)(\w+)$)|(?:^(\d+)(\,)(\d+)$)|(?:(\w+)(\,)(\w+)$)|(?:(\w+\-\w+)(\,)(\w+)$)|(?:(\w+)(\,)(\w+\-\w+)$)|(?:(\w+\-\w+)(\,)(\w+\-\w+)$)|(?:(\w+)(\,)(\w+\.\w+)$)|(?:(\w+)(\,)(\w+\.\w+)$)|(?:(\w+\.\w+)(\,)(\w+)$)|(?:(\w+\.\w+)(\,)(\w+\-\w+)$)|(?:(\w+\-\w+)(\,)(\w+\.\w+)$)|(?:(\w+\.\w+)(\,)(\w+\.\w+)$)', self.port):
                    break
                elif 0 < int(self.port) < 65536:
                    break
                else:
                    print('不支持的端口/格式错误，请重输！')

    @classmethod
    def mikrotik_capture(self):
        if self.mikrotik_yes_or_no == 'Yes' or self.mikrotik_yes_or_no == 'yes' or self.mikrotik_yes_or_no == 'y':
            filter_interface = self.api.get_resource('/').call('tool/sniffer/set', {'filter-interface': self.interface})
            filter_ip_add = self.api.get_resource('/').call('tool/sniffer/set', {'filter-ip-address': self.ip_add})
            filter_ip_protocol = self.api.get_resource('/').call('tool/sniffer/set', {'filter-ip-protocol': self.protocol})
            filter_ip_port = self.api.get_resource('/').call('tool/sniffer/set', {'filter-port': self.port})
            sniffer_start = self.api.get_resource('/').call('tool/sniffer/start')
            time.sleep(0.5)
            sniffer_stop = self.api.get_resource('/').call('tool/sniffer/stop')
            time.sleep(1)
            sniffer_save = self.api.get_resource('/').call('tool/sniffer/save', {'file-name': self.device_hostname + '_' + self.date_findall[0] + self.month_findall[0] + '.pcap'})

            scripts = self.api.get_resource("/system/script")
            try:
                scripts.add(name='ftp-up-api', source='{/tool/fetch address=10.200.2.237 src-path=' + self.device_hostname + '_' + self.date_findall[0] + self.month_findall[0] + '.pcap' + ' user=sdwan_ftp mode=ftp password=Esun@sdwan_ftp dst-path=' + 'datahub' + '/' + self.device_hostname + '_' + self.date_findall[0] + self.month_findall[0] + '.pcap' + ' upload=yes' + '}')
            except routeros_api.exceptions.RouterOsApiCommunicationError:
                print('脚本已存在！请手动删除！')
            scripts.get(name='ftp-up-api')
            script_to_run = scripts.get(name="ftp-up-api")[0]
            print(script_to_run)
            scripts.run = self.api.get_resource('/').call('system/script/run', {'number': script_to_run['id']})
            time.sleep(8)
            scripts.run = self.api.get_resource('/').call('system/script/remove', {'number': script_to_run['id']})
            time.sleep(1)

            self.connection.disconnect()


Capture.device_choice()
Capture.login_mikrotik()
Capture.login()
Capture.device_get_interface()
Capture.cisco_get_input()
Capture.cisco_capture()
Capture.huawei_get_input()
Capture.huawei_capture()
Capture.mikrotik_get_input()
Capture.mikrotik_capture()
print('5秒后自动关闭窗口')
time.sleep(5)
