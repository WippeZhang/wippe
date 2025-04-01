
mac_red = input('请输入mac地址：')            # 使用input输入实参mac-red
def mac_add(mac):          #定义形参mac
    mac = mac.upper()      #把输入的实参改为大写字母
    if "-" in mac:         #匹配实参内的-，如果有的话继续循环往下执行
        mac = mac.split('-')       #以实参内的-符号进行分割，取出每一个2位字符
        new_mac = []                 #定义一个空列表存放修改后的mac地址
        for i in mac:                  #在分割好的实参内进行循环匹配
            if len(i) < 2:           #如果长度小余2位
                i = i.zfill(2)       #补全到2位，在头部填0
            new_mac.append(i)        #把结果添加到空列表中存储
    elif "." in mac:
        mac = mac.split('.')         #把实参以.进行分割元素
        new_mac = []                 #定义一个空列表存放元素
        for i in mac:                #在分割好的实参内进行循环匹配
            if len(i) < 4:           #如果长度小余4位
                i = i.zfill(4)       #补全到4位，在头部填0
            new_mac.append(i[:2])    #把元素前2位添加到列表
            new_mac.append(i[2:])    #把元素从第3位（从0位开始）开始添加到列表

    return ':'.join(new_mac)         #在返回的结果中的每一位成员之间添加：
print('转换后的mac地址为：',mac_add(mac_red))
while True:
    omt = input('是否还需要转换？1.Yes 2.No\n')
    if 'N' in omt or 'No' in omt or 'no' in omt or '2' in omt:
        break
    else:
        mac_red = input('请输入mac地址：')  # 使用input输入实参mac-red
        def mac_add(mac):  # 定义形参mac
            mac = mac.upper()  # 把输入的实参改为大写字母
            if "-" in mac:  # 匹配实参内的-，如果有的话继续循环往下执行
                mac = mac.split('-')  # 以实参内的-符号进行分割，取出每一个2位字符
                new_mac = []  # 定义一个空列表存放修改后的mac地址
                for i in mac:  # 在分割好的实参内进行循环匹配
                    if len(i) < 2:  # 如果长度小余2位
                        i = i.zfill(2)  # 补全到2位，在头部填0
                    new_mac.append(i)  # 把结果添加到空列表中存储
            elif "." in mac:
                mac = mac.split('.')  # 把实参以.进行分割元素
                new_mac = []  # 定义一个空列表存放元素
                for i in mac:  # 在分割好的实参内进行循环匹配
                    if len(i) < 4:  # 如果长度小余4位
                        i = i.zfill(4)  # 补全到4位，在头部填0
                    new_mac.append(i[:2])  # 把元素前2位添加到列表
                    new_mac.append(i[2:])  # 把元素从第3位（从0位开始）开始添加到列表

            return ':'.join(new_mac)  # 在返回的结果中的每一位成员之间添加：
        print('转换后的mac地址为：', mac_add(mac_red))