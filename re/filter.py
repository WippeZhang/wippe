import re

txt = ['''[0  ] cn-esu-shangh-pe-01 10.200.0.1
[1  ] cn-esu-guangz-pe-01 10.200.0.2
[2  ] cn-esu-beijin-pe-01 10.200.0.3
[3  ] cn-esu-shangh-nms-01 10.200.0.4
[4  ] cn-esu-shangh-pe-02 10.200.0.5
[5  ] cn-esu-shangh-nms-02 10.200.0.6
[6  ] cn-esu-hongko-pe-01 10.200.0.7
[7  ] cn-esu-chengd-pe-01 10.200.0.9
[8  ] cn-esu-hangzh-pe-01 10.200.0.10
[9  ] cn-esu-suzhou-pe-02 10.200.0.13
[10 ] cn-esu-tianji-pe-01 10.200.0.14
[11 ] cn-esu-jinan-pe-01 10.200.0.15
[12 ] cn-esu-hefei-pe-01 10.200.0.16
[13 ] cn-esu-langfa-pe-01 10.200.0.17
[14 ] cn-esu-wuhan-pe-01 10.200.0.18
[15 ] cn-esu-wuxi-pe-01 10.200.0.19
[16 ] cn-esu-shenzh-pe-02 10.200.0.20
[17 ] cn-esu-xian-pe-01 10.200.0.21
[18 ] cn-esu-changz-pe-01 10.200.0.22
[19 ] cn-esu-beijin-pe-02 10.200.0.23
[20 ] cn-esu-guangz-pe-02 10.200.0.24
[21 ] cn-esu-hongko-pe-02 10.200.0.25
[22 ] sw-esu-stockh-pe-01 10.200.0.26
[23 ] cn-esu-shangh-ipe-01 10.200.0.27
[24 ] cn-esu-shangh-sw-02 10.200.1.4
[25 ] cn-esu-shangh-sw-03 10.200.1.5
[26 ] cn-esu-shangh-sw-04 10.200.1.6
[27 ] cn-esu-shangh-sw-05 10.200.1.7
[28 ] cn-esu-shangh-sw-07 10.200.1.9
[29 ] cn-esu-shangh-sw-08 10.200.1.10
[30 ] cn-esu-shangh-sw-09 10.200.1.11
[31 ] cn-esu-shangh-sw-10 10.200.1.12
[32 ] cn-esu-shangh-sw-11 10.200.1.13
[33 ] cn-esu-shangh-sw-12 10.200.1.14
[34 ] cn-esu-shangh-sw-13 10.200.1.15
[35 ] cn-esu-shangh-sw-14 10.200.1.16
[36 ] cn-esu-shangh-sw-15 10.200.1.17
[37 ] cn-esu-shangh-sw-16 10.200.1.18
[38 ] cn-esu-shangh-sw-17 10.200.1.19
[39 ] cn-esu-shangh-sw-18 10.200.1.20
[40 ] cn-esu-shangh-gw-03 10.200.2.1
[41 ] cn-esu-shangh-gw-04 10.200.2.2
[42 ] cn-esu-hongko-gw-03 10.200.2.192
[43 ] cn-esu-guangz-gw-01 10.200.2.193
[44 ] sw-esu-stockh-gw-01 10.200.2.194
[45 ] cn-esu-shangh-gw-02 10.200.2.195
[46 ] cn-esu-shangh-gw-01 10.200.2.196
[47 ] cn-esu-hongko-gw-02 10.200.2.197
[48 ] cn-esu-hongko-gw-01 10.200.2.198
[49 ] cn-esu-shangh-gw-05 10.200.2.200
[50 ] cn-esu-Ford-GateWay 10.200.2.202
[51 ] cn-esu-shangh-gw-08 10.200.2.203
[52 ] cn-esu-shangh-gw-10 10.200.2.205
[53 ] cn-esu-shangh-gw-11 10.200.2.206
[54 ] cn-esu-shangh-gw-14 10.200.2.209
[55 ] cn-esu-shangh-gw-15 10.200.2.210
[56 ] cn-esu-shangh-gw-16 10.200.2.211
[57 ] cn-esu-shangh-gw-17 10.200.2.212
[58 ] cn-esu-shangh-ts-01 10.200.2.213
[59 ] cn-esu-shangh-cgw-18 10.200.2.214
[60 ] cn-esu-shangh-cgw-20 10.200.2.216
[61 ] cn-esu-hangzh-cgw-01 10.200.2.217
[62 ] cn-wir-langfa-ce-01 10.210.12.1
[63 ] cn-wir-taican-ce-01 10.210.12.2
[64 ] cn-wir-guangz-ce-01 10.210.12.3
[65 ] cn-wir-foshan-ce-01 10.210.12.4
[66 ] cn-luf-shangh-ce-01 10.210.18.1
[67 ] cn-luf-hongko-ce-02 10.210.18.2
[68 ] cn-luf-beijin-ce-01 10.210.18.3
[69 ] cn-adi-shangh-ce-03 10.220.1.3
[70 ] cn-adi-shangh-ce-04 10.220.1.4
[71 ] cn-adi-shangh-ce-05 10.220.1.5
[72 ] cn-adi-shangh-ce-02 10.220.1.6
[73 ] cn-thy-shangh-ce-02 10.220.2.3
[74 ] cn-air-shangh-ce-01 10.220.2.6
[75 ] cn-air-shangh-ce-02 10.220.2.7
[76 ] cn-lvm-shangh-ce-02 10.220.2.9
[77 ] cn-gtt-shangh-vpn-01 10.220.2.10
[78 ] uk-hua-swales-ce-01 10.220.2.13
[79 ] cn-lvm-shangh-ce-03 10.220.2.15
[80 ] cn-frd-shangh-ce-01 10.220.2.18
[81 ] cn-frd-shangh-ce-02 10.220.2.19
[82 ] cn-fnz-shangh-ce-03 10.220.2.38
[83 ] cn-fnz-shangh-ce-02 10.220.2.39
[84 ] cn-fnz-shangh-ce-01 10.220.2.40
[85 ] cn-log-shangh-ce-01 10.220.2.43
[86 ] cn-mkc-shangh-ce-02 10.220.2.46
[87 ] cn-mkc-shangh-ce-03 10.220.2.47
[88 ] cn-bkt-shangh-ce-01 10.220.2.48
[89 ] cn-bkt-beijin-ce-01 10.220.2.49
[90 ] cn-bkt-guangz-ce-01 10.220.2.50
[91 ] cn-bkt-suzhou-ce-01 10.220.2.51
[92 ] cn-bkt-suzhou-ce-02 10.220.2.52
[93 ] cn-bkt-hangzh-ce-01 10.220.2.53
[94 ] cn-bkt-shenya-ce-01 10.220.2.54
[95 ] cn-bkt-chengd-ce-01 10.220.2.56
[96 ] cn-bkt-qingda-ce-01 10.220.2.57
[97 ] cn-bkt-wuhan-ce-01 10.220.2.58
[98 ] cn-mkc-shangh-ce-04 10.220.2.60
[99 ] cn-cst-chongq-ce-01 10.220.2.62
[100] cn-cmc-shangh-sdw-cpe-1 10.220.2.63
[101] cn-cst-suzhou-ce-01 10.220.2.64
[102] cn-cst-suzhou-ce-02 10.220.2.65
[103] cn-cst-suzhou-ce-03 10.220.2.66
[104] cn-cst-suzhou-ce-04 10.220.2.67
[105] cn-cst-shangh-ce-01 10.220.2.68
[106] cn-cst-shangh-ce-02 10.220.2.69
[107] cn-cst-shangh-ce-03 10.220.2.70
[108] cn-bkt-suzhou-ce-03 10.220.2.71
[109] cn-blt-shangh-sdw-cpe-1 10.220.2.72
[110] cn-vor-shangh-ce-02 10.220.2.73
[111] cn-cst-shangh-ce-04 10.220.2.74
[112] cn-cst-jiaxin-ce-01 10.220.2.75''']

for i in txt:
    context = re.compile('.* .* (.*)')
    find = context.findall(i)
    for x in find:
        print(x)
