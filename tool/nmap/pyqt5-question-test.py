import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, \
    QComboBox, QLabel, QMessageBox, QDialog, QInputDialog
from PyQt5.QtGui import QFont
import nmap
import random

# 问题列表
questions = {
    "天空是什么颜色?": "蓝色",
    "2 + 2?": "4",
    "72 + 16?": "88",
    "8 x 3 + 3?": "27",
    "Esun最帅的男人是谁?": "张智翔"
}

class CustomInputDialog(QDialog):
    def __init__(self, question, parent=None):
        super().__init__(parent)
        self.setWindowTitle("问题验证")
        layout = QVBoxLayout(self)

        # 设置问题标签并调整字体大小
        self.label = QLabel(question)
        self.label.setFont(QFont("Arial", 12))  # 设置字体大小
        layout.addWidget(self.label)

        # 设置输入框并调整字体大小
        self.input_text = QLineEdit()
        self.input_text.setFont(QFont("Arial", 11))  # 设置字体大小
        layout.addWidget(self.input_text)

        # 设置确认按钮并调整字体大小
        self.submit_button = QPushButton("确定")
        self.submit_button.setFont(QFont("Arial", 11))  # 设置字体大小
        self.submit_button.clicked.connect(self.accept)
        layout.addWidget(self.submit_button)

    def getText(self):
        return self.input_text.text()

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录")
        self.setFixedSize(666, 444)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('用户名:')
        # self.username_input.setFixedWidth(150)
        self.username_input.setFixedHeight(50)
        self.username_input.setFont(QFont("Arial", 13))  # 设置字体大小为10号
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('密码:')
        self.password_input.setFixedHeight(50)
        self.password_input.setFont(QFont("Arial", 13))  # 设置字体大小为10号
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
                                QPushButton {
                                    background-color: rgba(42, 187, 168,255);
                                    border:1px outset rgb(255, 255, 255);
                                    color: white;
                                    padding: 15px 32px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    margin: 4px 2px;
                                    cursor: pointer;
                                    border-radius: 7px;
                                    font: bold italic 12px "Microsoft YaHei";
                                    font-weight: bold;
                                    font-size: 12px;
                                }

                                QPushButton:hover {
                                    background-color: rgba(165, 205, 255,90%);
                                    border:2px outset rgba(36, 36, 36,0);
                                }

                                QPushButton:pressed {
                                    background-color: rgba(165, 205, 255,100%);
                                    border:2px outset rgba(36, 36, 36,0);
                                }
                            """)
        self.login_button.setEnabled(False)  # 默认禁用登录按钮
        self.login_button.clicked.connect(self.verify_credentials)
        self.human_check_button = QPushButton("我是人类")
        self.human_check_button.clicked.connect(self.verify_human)
        self.human_check_button.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(42, 205, 255,255);
                            border:1px outset rgb(255, 255, 255);
                            color: white;
                            padding: 15px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 7px;
                            font: bold italic 12px "Microsoft YaHei";
                            font-weight: bold;
                            font-size: 12px;
                        }

                        QPushButton:hover {
                            background-color: rgba(165, 205, 255,90%);
                            border:2px outset rgba(36, 36, 36,0);
                        }

                        QPushButton:pressed {
                            background-color: rgba(165, 205, 255,100%);
                            border:2px outset rgba(36, 36, 36,0);
                        }
                    """)
        layout = QVBoxLayout()
        layout.setSpacing(1)  # 设置布局中的间距为10像素
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.human_check_button)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def verify_credentials(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if username == "vas" and password == "Esun@1sh":
            self.accept()
        else:
            QMessageBox.warning(self, '登录失败', '用户名或密码错误，请重试！')

    def verify_human(self):
        # 这里是验证人类的逻辑
        question, answer = random.choice(list(questions.items()))

        # 创建自定义对话框并设置字体大小
        dialog = CustomInputDialog(question, self)

        # 显示对话框并获取用户输入
        if dialog.exec_() == QDialog.Accepted:
            user_answer = dialog.getText()
            if user_answer.strip().lower() == answer.lower():
                QMessageBox.information(self, '验证成功', '您是人类！')
                # 启用登录按钮
                self.login_button.setEnabled(True)
            else:
                QMessageBox.warning(self, '验证失败', '回答错误，请重试！')

class PortScannerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.login_dialog = LoginDialog()
        if self.login_dialog.exec_() == QDialog.Accepted:
            self.initUI()
        else:
            sys.exit()  # 如果用户关闭登录对话框，则直接退出程序

    def initUI(self):
        self.setWindowTitle('Port Scanner')
        screen_width = QApplication.desktop().width()
        screen_height = QApplication.desktop().height()
        desired_width = int(0.2 * screen_width)
        desired_height = int(0.4 * screen_height)
        self.resize(desired_width, desired_height)

        # 输入框和按钮布局
        input_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText('请输入IP(用空格分割)')
        self.ip_input.setFont(QFont("Arial", 10))  # 设置字体大小为10号
        input_layout.addWidget(self.ip_input)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText('请输入端口号(例：53,80,2000-65535')
        self.port_input.setFont(QFont("Arial", 10))  # 设置字体大小为10号
        input_layout.addWidget(self.port_input)

        self.scan_button = QPushButton('扫描')
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setFont(QFont("Arial", 10))
        input_layout.addWidget(self.scan_button)

        # 下拉框布局
        combo_layout = QHBoxLayout()
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItem("TCP")
        self.protocol_combo.addItem("UDP")
        self.protocol_combo.setFont(QFont("Arial", 10))
        combo_layout.addWidget(QLabel('选择协议: ', font=QFont("Arial", 10)))
        combo_layout.addWidget(self.protocol_combo)

        # 扫描结果显示框
        self.result_text = QTextEdit()
        self.result_text.setFont(QFont("Arial", 11))  # 设置字体大小为10号
        self.result_text.setStyleSheet("QTextEdit {color: black;}")

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(combo_layout)
        main_layout.addWidget(self.result_text)

        self.setLayout(main_layout)

    def start_scan(self):
        target_network = self.ip_input.text().strip()
        if not target_network:
            self.result_text.append('请输入有效的IP地址')
            return

        protocol = self.protocol_combo.currentText()
        target_ports = self.port_input.text().strip()

        self.result_text.clear()
        self.result_text.append(f'正在扫描 {target_network} 的 {protocol} 端口...')

        nm = nmap.PortScanner()

        if protocol == "TCP":
            nm.scan(hosts=target_network, arguments=f'-p {target_ports}')
            for host in nm.all_hosts():
                host_open = False
                for port in nm[host]['tcp']:
                    state = nm[host]['tcp'][port]['state']
                    if state == "open":
                        host_open = True
                        # 使用字符串格式化来保证字段长度一致
                        self.result_text.append("{:<20}\tTCP Port: {:<10}\tState: {}".format(host, port, state))
        elif protocol == "UDP":
            nm.scan(hosts=target_network, arguments=f'-sU -p {target_ports}')
            for host in nm.all_hosts():
                host_open = False
                for port in nm[host]['udp']:
                    state = nm[host]['udp'][port]['state']
                    if state == "open":
                        host_open = True
                        # 使用字符串格式化来保证字段长度一致
                        self.result_text.append("{:<20}\tUDP Port: {:<10}\tState: {}".format(host, port, state))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    port_scanner_gui = PortScannerGUI()
    port_scanner_gui.show()
    sys.exit(app.exec_())