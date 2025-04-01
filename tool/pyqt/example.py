import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QCoreApplication, QPoint
from PyQt5.QtGui import QPainter, QColor


class CircularWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口无边框和透明背景
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置窗口初始位置和大小
        self.setGeometry(100, 100, 1024, 768)

        # 创建一个关闭按钮
        self.close_button = QPushButton('X', self)
        self.close_button.setGeometry(974, 10, 40, 40)
        self.close_button.setStyleSheet('background-color: red; border-radius: 20px; color: white; font-size: 20px;')

        # 连接关闭按钮的点击事件
        self.close_button.clicked.connect(QCoreApplication.instance().quit)

    def mousePressEvent(self, event):
        # 记录鼠标按下的初始位置
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        # 移动窗口
        self.move(self.pos() + event.pos() - self.offset)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        painter.setBrush(QColor(255, 255, 255, 255))  # 设置画刷颜色和透明度
        painter.setPen(Qt.NoPen)  # 无边框

        rect = self.rect()
        rect.adjust(2, 2, -2, -2)  # 缩小矩形范围，使得圆角能够完全覆盖
        painter.drawRoundedRect(rect, 10, 10)  # 绘制圆角矩形


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CircularWindow()
    window.show()
    sys.exit(app.exec_())
