import pyautogui

# 获取当前鼠标坐标
# currentMouseX, currentMouseY = pyautogui.position()
# print('当前鼠标坐标为：', currentMouseX, currentMouseY)


# 点击指定坐标
def click_at(x, y):
    pyautogui.click(x, y)

# 按住后移动鼠标再松开
def drag_from_to(x1, y1, x2, y2, duration=1):
    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown()  # 按住鼠标左键
    pyautogui.moveTo(x2, y2, duration=duration)
    pyautogui.mouseUp()    # 松开鼠标左键

# 测试点击指定坐标
click_at(100, 100)

# 延迟 2 秒以便切换窗口
time.sleep(2)

# 测试按住后移动鼠标再松开
drag_from_to(200, 200, 300, 300)
