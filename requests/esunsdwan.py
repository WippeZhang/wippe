import os
from selenium import webdriver

# 设置 Chromedriver 的路径
driver_path = r"C:\Users\Wippe.zhang\.cache\selenium\chromedriver\win64\122.0.6261.94\chromedriver.exe"

# 将 Chromedriver 的路径添加到系统的 PATH 环境变量中
os.environ["PATH"] += os.pathsep + os.path.dirname(driver_path)

# 创建 Chrome 浏览器实例
driver = webdriver.Chrome()

# 打开网页
url = "http://10.0.90.173/websocket/loginmt/mtlogin/page/winboxlogin/ipaddr/10.221.0.24"
driver.get(url)

# 输入用户名和密码
username = "wippe.zhang"
password = "Esun@1sh"

# 找到用户名和密码的输入框并输入值
username_input = driver.find_element_by_name("username")
password_input = driver.find_element_by_name("password")

username_input.send_keys(username)
password_input.send_keys(password)

# 提交登录表单
login_button = driver.find_element_by_xpath("//input[@type='submit']")
login_button.click()

# 在这之后继续操作登录后的页面内容
