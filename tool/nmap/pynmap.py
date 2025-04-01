import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, \
    QComboBox, QLabel
from PyQt5.QtGui import QFont
import nmap


class PortScannerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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

        self.result_text.append("\n扫描已结束")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    port_scanner_gui = PortScannerGUI()
    port_scanner_gui.show()
    sys.exit(app.exec_())
