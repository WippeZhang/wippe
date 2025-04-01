import re


a = "port(3478-3481 40000-65535)"
#print(a)
com1 = re.compile('\S+')
find1 = com1.findall(a)
for i in find1:
    print(i)
