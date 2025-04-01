from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 设置Chrome无头模式
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# 创建Chrome浏览器实例
driver = webdriver.Chrome(options=chrome_options)

# 打开网页
url = "https://sdwan.esun21.cn/esun/admin.php/backend_ensdwbcus/saasregionlist#"
driver.get(url)

# 获取网页内容
page_content = driver.page_source

# 打印网页内容
print(page_content)

# 关闭浏览器
driver.quit()