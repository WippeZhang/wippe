import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QLabel, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
from PyQt5.QtCore import Qt, QRectF
import pyshark


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PCAP Summary")
        self.setGeometry(100, 100, 1024, 768)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 记录鼠标按下的位置和窗口位置
        self.old_pos = None
        self.old_frame_pos = None

        # 添加标题栏
        self.title_bar = QWidget()
        layout.addWidget(self.title_bar)
        title_layout = QHBoxLayout()
        self.title_bar.setLayout(title_layout)

        # 添加标题
        self.title_label = QLabel("PCAP Analysis")
        font = QFont()
        font.setPointSize(12)  # 设置标题字体大小
        font.setFamily("Microsoft YaHei")
        self.title_label.setFont(font)
        title_layout.addWidget(self.title_label)

        # 添加关闭按钮
        self.close_button = QPushButton("×")
        self.close_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 100, 100, 0);
                        border: none;
                        border-radius: 10px;
                        width: 20px; /* 设置按钮宽度 */
                        height: 20px;
                        font-size: 20px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 80, 70, 160);
                    }
        """)
        self.close_button.clicked.connect(self.close)
        title_layout.addWidget(self.close_button, alignment=Qt.AlignRight)

        self.text_box = QTextEdit()
        font = QFont()
        font.setPointSize(11)  # 设置文本框字体大小
        self.text_box.setFont(font)
        layout.addWidget(self.text_box)

        self.scrollbar = self.text_box.verticalScrollBar()

        self.process_button = QPushButton("选择 PCAP 文件")
        self.process_button.clicked.connect(self.process_pcap)
        self.process_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(165, 205, 255,255);
                    border:1px outset rgb(255, 255, 255);
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 20px;
                    font: bold italic 18px "Microsoft YaHei";
                    font-weight: bold;
                    font-size: 16px;
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
        layout.addWidget(self.process_button)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
            self.old_frame_pos = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.old_frame_pos + delta)

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        self.old_frame_pos = None

    def paintEvent(self, event):
        # 绘制圆角边框
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.setPen(QPen(QColor(165, 205, 255), 1, Qt.SolidLine))
        painter.setPen(QPen(QColor(50, 50, 50), 0.2, Qt.SolidLine))
        painter.setBrush(QColor(255, 255, 255, 255))
        rect = QRectF(1, 1, self.width() - 2, self.height() - 2)
        painter.drawRoundedRect(rect, 10, 10)
        # painter.setPen(Qt.NoPen)  # 无边框

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("PCAP files (*.pcap);;All files (*.*)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            return file_paths[0]  # return the first selected file path

    def display_output(self, output):
        self.text_box.setPlainText(output)

    def process_pcap(self):
        pcap_file = self.select_file()
        if pcap_file:
            cap = pyshark.FileCapture(pcap_file)

            try:
                src_dst_ips = []
                for packet in cap:
                    try:
                        if 'IP' in packet:
                            source_ip = packet.ip.src
                            dest_ip = packet.ip.dst
                            src_dst_ip = (packet.ip.src, packet.ip.dst)
                            src_dst_ips.append(src_dst_ip)

                    except:
                        pass

                last_list = []
                for i in src_dst_ips:
                    if i in last_list:
                        pass
                    else:
                        last_list.append(i)

                sorted_data = sorted(last_list, key=lambda x: x[0])

                summary_dict = {}
                for first, second in sorted_data:
                    if first not in summary_dict:
                        summary_dict[first] = set()
                    summary_dict[first].add(second)

                sec_sum = {}
                list_sum = list(summary_dict.items())

                summary_dict = {}
                for ip, ip_set in list_sum:
                    ip_set_tuple = tuple(ip_set)
                    if ip_set_tuple not in summary_dict:
                        summary_dict[ip_set_tuple] = set()
                    summary_dict[ip_set_tuple].add(ip)

                output = ""
                for ip_set_tuple, ips in summary_dict.items():
                    output += f"源IP: {', '.join(ips)}, 目的IP: {', '.join(ip_set_tuple)}\n\n"

                self.display_output(output)
            finally:
                cap.close()  # Close the FileCapture object


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())