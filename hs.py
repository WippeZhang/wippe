import re

ip = 'https://1.1.1.1'
com = re.compile('(?:https://)|(?:http://)(\d+\.\d+\.\d+\.\d+)')
find = com.findall(ip)
for i in find:
    print(i)