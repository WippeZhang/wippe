import re
# print(re.findall("\d","!@#@#FEWHFUYO12343215"))
# print(re.findall("\D","123qwe!@#"))


# i = "Gateway of last resort is 10.0.19.254 to network 0.0.0.0"
# # com1 = re.compile("this (cat)")
# com2 = re.compile("(\d+\.\d+\.\d+\.\d+/*\d*)")
# r = com2.findall(i)
# print(r)



# l = [1,2,3,4,5,6,7]
# print(l.index(6))

# ipv4 = []
# vrf = '''  1                                1:1                 ipv4        Lo0
#   2                                2:2                 ipv4 '''
# print(vrf)
# vrfline = vrf.split("\n")
# print(vrfline)
# for i in vrfline:
#     r = i.split()
#     print(r)
#     if "2" in r:
#         ipv4.append(r[0])
#     else:
#         continue
# print(ipv4)

# username_command = None
# while True:
#     userfilter = input('是否需要筛选用户？1.yes 2.no\n')
#     if '1' in userfilter:
#         username_command = input('请输入用户：')
#         break
#     elif '2' in userfilter:
#         break
#     else:
#         print('输入错误,请重输！')
# if username_command != None:
#     print(username_command)
# else:
#     print('null')
#
#
# while True:
#     name = input('请输入想要抓包的文件名称(less than or equal to 8 characters and only (_))：')
#     if len(name) > 8:
#         print('文件名称长度大于8,请重新输入：')
#     elif len(name) == 0:
#         print('文件名称不可为空，请重输！')
#     elif '!' in name or '@' in name or '#' in name or '$' in name or '%' in name or '^' in name or '&' in name or '*' in name or '(' in name or ')' in name or '-' in name or '+' in name or '=' in name:
#         print("只能使用'_'这一种特殊字符，请重新输入：")
#     else:
#         break


# import datetime
#
# now = datetime.datetime.now()
# time = now.strftime("%Y%m%d_%H%M%S")
# print(time)
# Y = now.strftime("%Y")
# M = now.strftime("%m")
# D = now.strftime("%d")
# print(Y+M+D)

url1 = '<td class="first"><a href="/http/www.test.com">http://www.test.com</a>=$0</td><td>Oct 2023</td><td class="xxx" 0%;">100%</td>'
url2 = '<td class="first"><a href="/www.test2.com">http://www.test2.com</a>=$0</td><td>Oct 2023</td><td class="xxx" 0%;">100%</td>'
url3 = '<td class="first"><a href="/https/www.test3.com">https://www.test2.com</a>=$0</td><td>Oct 2023</td><td class="xxx" 0%;">100%</td>'
url4 = '<td class="first"><a href="/url/232323com">https://www.test2.com</a>=$0</td><td>Oct 2023</td><td class="xxx" 0%;">100%</td>'

ip_com = re.compile('(?:<td class="first"><a href=)(?:.*)(?:>)(?:http)?(?:s)?(?::\/\/)?(.*)(?:</a>)(?:.*)(Sep\s2023|Oct\s2023|Nov\s2023|Dec\s2023)(?:.*)(100%)(?:</td>)')
ip_find = ip_com.findall(url1)
for j in ip_find:
    print(j)