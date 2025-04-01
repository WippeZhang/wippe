# $language = "Python"
# $interface = "1.0"

def main():

	crt.Screen.Synchronous = True
	
	#==================================自动输入证书密钥=================================#
	#result返回数值，1对应Enter Passphrase for；2对应正常登入后的提示
	#之所以用这种方式写，原因是crt.Screen.WaitForString是先后顺序执行，无法并列乱序执行。导致第一个WaitForString的字符串没有找到，后面的都不执行
	result = crt.Screen.WaitForStrings(["Enter Passphrase for : ", "wangxing"])
	if (result == 1):
		######################替换自己的密钥##########################
		crt.Screen.Send("gMz0qFGOvvauS_ql")
		crt.Screen.Send("\r\n")

	#==================================自动SecureCRT的标题改成登入设备Hostname=================================#
	#设置变量ckEquipment，1对应Juniper提示@; 2对应Huawei提示<; 3对应Cisco提示#
	#当出现以上提示，说明可以开始抓取了。
	#由于@符号在成功登入堡垒机后，提示中有@，已经让王行更改登入提示信息，去掉@和#
	############################这里暂时用frank@替代########################
	while 1:
		ckinfo = crt.Screen.WaitForString("输入ID或者其它帮助信息")
		crt.Screen.Send("\n")
		crt.GetActiveTab().Caption = "堡垒机"
  		########################自动登入，用户名和密码#############################
  		crtScreen = crt.Screen.WaitForStrings(["Login>:"])

  		if (crtScreen == 1):
  			crt.Screen.Send("wippe\r\n")
			crt.Screen.WaitForString("Password>:")
			crt.Screen.Send("z010808\r\n")


		ckEquipment = crt.Screen.WaitForStrings(["@","<","#"])
		#抓取到上述字符后自动按一下回车为了让当前行字符显示完整
		crt.Screen.Send("\n")
		#抓取回车符作为最后光标所在的行数
		crt.Screen.WaitForString("\n")
		
		
		#初始化参数
		strRow = (crt.Screen.CurrentRow - 1)
		getStr = crt.Screen.Get(strRow,1,strRow,100)

		#Get Juniper & Vyos Hostname
		if (ckEquipment == 1):
			strF = getStr.find('@')+1
			if "$" in getStr:
				strL = getStr.find(':')
				crt.Screen.Send("configure\r\n")
			else:
				strL = getStr.find('>')
				crt.Screen.Send("configure\r\n")
		
		#Get Huawei Hostname
		if (ckEquipment == 2):
			strF = getStr.find('<')+1
			strL = getStr.find('>')
			crt.Screen.Send("syst\r\n")
		
		#Get Cisco Hostname
		if (ckEquipment == 3):
			strL = getStr.find('#')
			strF = strL - 19

		#变量tabStr为取得的设备Hostname
		tabStr = getStr[strF:strL] 
		#str是强制将数字转成字符串，这样MessageBox才能显示
		#crt.Dialog.MessageBox(str(strL))
		
		#改变SecureCRT的Tab标题
		crt.GetActiveTab().Caption = tabStr
	


main()
