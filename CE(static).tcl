puts "Enter device id"
set id [gets stdin]
puts "Enter customer name"
set hostname [gets stdin]
puts "Enter device city"
set city [gets stdin]
puts "Enter Mgmt ip"
set lo0 [gets stdin]
puts "Enter tunnel id"
set tid [gets stdin]
puts "Enter tunnel IP"
set tip [gets stdin]
set tipfir [string rang $tip 0 [string last "." $tip]]
set tipend [expr [ string range $tip [expr [string last "." $tip]+1] end]-1]
set tdip $tipfir$tipend
puts "Is there an interconnected address? \n 1.yes 2.no"
set connect [gets stdin]
if {$connect == 1} {
puts "Enter connected IP"
set connectip [gets stdin]
puts "Enter connected gw"
set connectgw [gets stdin]
puts "Enter customer ip"
set customerip [gets stdin]
set customerfir [string rang $customerip 0 [string last "." $customerip]]
set customerend [expr [ string range $customerip [expr [string last "." $customerip]+1] end]+1]
set customergw $customerfir$customerend
puts "Enter customer netmask"
set mask [gets stdin]
ios_config "interface g0/0/0" "ip address $connectip 255.255.255.252" "no shutdown"
ios_config "ip route 0.0.0.0 0.0.0.0 $connectgw"
ios_config "interface vlan 10" "ip address $customergw $mask"
ios_config "interface range gigabitEthernet 0/1/0-3" "swi mode acce" "swi acc vlan 10" "no shutdown"
} else {
puts "Enter ISP GW"
set gw [gets stdin]
puts "Enter netmask"
set netmask [gets stdin]
ios_config "ip route 0.0.0.0 0.0.0.0 $gw"
set gwfir [string rang $gw 0 [string last "." $gw]]
set gwend_1 [expr [ string range $gw [expr [string last "." $gw]+1] end]+1]
set gwend_2 [expr [ string range $gw [expr [string last "." $gw]+1] end]+2]
set gwend_3 [expr [ string range $gw [expr [string last "." $gw]+1] end]+3]
set gwend_4 [expr [ string range $gw [expr [string last "." $gw]+1] end]+4]
set gwend_5 [expr [ string range $gw [expr [string last "." $gw]+1] end]+5]
set cgw $gwfir$gwend_1
set cip_1 $gwfir$gwend_2
set cip_2 $gwfir$gwend_3
set cip_3 $gwfir$gwend_4
set cip_4 $gwfir$gwend_5
ios_config "int g0/0/0" "ip address $cgw $netmask" "no shutdown"
ios_config "int vlan 10" "ip unnumbered GigabitEthernet0/0/0" "no shutdown"
ios_config "interface range gigabitEthernet 0/1/0-3" "swi mode acce" "swi acc vlan 10" "no shutdown"
ios_config "ip route $cip_1 255.255.255.255 vlan 10"
ios_config "ip route $cip_2 255.255.255.255 vlan 10"
ios_config "ip route $cip_3 255.255.255.255 vlan 10"
ios_config "ip route $cip_4 255.255.255.255 vlan 10"
}
puts "Internet configuration completion"
ios_config "ip vrf Mgmt" "exit"
ios_config "hostname cn-$hostname-$city-ce-$id"
ios_config "int loo 0" "ip vrf forwarding Mgmt" "ip address $lo0 255.255.255.255" "description Mgmt"
ios_config "no ip domain-lookup"
ios_config "aaa new-model"
ios_config "aaa group server tacacs+ Esun_TAC" "server-private 10.200.0.246 key 7 05080F1C2243" "server-private 10.200.2.246 key 7 05080F1C2243" "ip vrf forwarding Mgmt" "ip tacacs source-interface loo0"
ios_config "aaa authentication password-prompt \"Tacacs no reachable - Enter local password:\""
ios_config "aaa authentication username-prompt \"Tacacs no reachable - Enter local username:\""
ios_config "aaa authentication login default group Esun_TAC local-case"
ios_config "aaa authentication enable default group Esun_TAC enable"
ios_config "aaa authorization exec default group Esun_TAC local"
ios_config "aaa authorization commands 15 default group Esun_TAC local"
ios_config "aaa accounting exec default" "action-type start-stop" "group Esun_TAC"
ios_config "aaa accounting commands 15 default" "action-type stop-only" "group Esun_TAC"
ios_config "aaa session-id common"
puts "AAA configuration Complete"
ios_config "interface tunnel $tid" "description *** Connected cn-esu-shangh-gw-05 For Mgmt ***" "ip vrf forwarding Mgmt" "ip address $tip 255.255.255.252" "tunnel source gigabitEthernet 0/0/0" "tunnel destination 103.204.72.53"
ios_config "ip route vrf Mgmt 10.200.0.224 255.255.255.224 $tdip name ***To-Esun-Monitoring-Server01***"
ios_config "ip route vrf Mgmt 10.200.2.224 255.255.255.224 $tdip name ***To-Esun-Monitoring-Server02***"
puts "Tunnel configuration Complete"
ios_config "ip domain-name cn-$hostname-$city-ce-$id"
ios_config "crypto key generate rsa modulus 1024"
ios_config "username esunadmin privilege 15 password 7 01361511552B571C29"
ios_config "enable password 7 002100130A7B5A1507"
puts "SSH configuration Complete"
ios_config "archive" "path ftp://admin_esun21@10.200.2.250/Esun_INTERNET_Config/$\h-" "write-memory"
ios_config "ip ftp source-interface Loopback0"
ios_config "ip ftp username admin_esun21"
ios_config "ip ftp password Esun@1sh_LocalAdmin"
ios_config "ip ftp source-interface loopback 0"
puts "Ftp configuration Complete"
ios_config "logging trap debugging"
ios_config "logging source-interface Loopback0"
ios_config "logging 10.200.2.238"
ios_config "logging 10.200.0.238"
ios_config "logging 10.200.0.250"
ios_config "login on-success log"
puts "Syslog configuration complete"
ios_config "snmp-server community esun-esu-cn RW 60:"
ios_config "snmp-server trap-source Loopback0"
ios_config "snmp-server contact 1st Level Service Desk Shanghai (freecall:  86 21 23135955)"
ios_config "snmp-server host 10.200.0.254 255.255.255.248"
ios_config "snmp-server host 10.200.2.254 255.255.255.248"
puts "Snmp configuration complete"
ios_config "line vty 0 15" "access-class 63 in vrf-also" "exec-timeout 5 10" "logging synchronous" "transport input ssh"
puts "Vty configuration complete"
ios_config "ntp logging"
ios_config "ntp source Loopback0"
ios_config "ntp server 10.200.2.238"
ios_config "ntp server 10.200.0.238"
ios_config "clock timezone GTM 8"
puts "NTP configuration complete"
ios_config "access-list 60 permit 10.200.0.242"
ios_config "access-list 60 permit 10.200.2.250"
ios_config "access-list 60 permit 10.200.0.254"
ios_config "access-list 60 permit 10.200.2.254"
ios_config "access-list 63 permit 10.200.0.224 0.0.0.31"
ios_config "access-list 63 permit 10.200.2.224 0.0.0.31"
ios_config "access-list 63 permit $tip 0.0.0.3"
exec "wr"
puts "ACL configuration complete"

