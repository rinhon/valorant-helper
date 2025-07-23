import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QPixmap,QColor
from PyQt5.QtWidgets import QStackedWidget, QLabel
from qfluentwidgets import CardWidget, ImageLabel, CaptionLabel, FluentIcon, TransparentToolButton
# from qfluentwidgets import *




class Home(QWidget):
    """主页组件"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置主布局
        # 创建一个水平布局
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        # 添加跳转查询点位页面按钮
        self.jumpQueryPageCard = CardWidget()
        self.jumpQueryPage = TransparentToolButton()
        self.jumpQueryPage.setIcon(FluentIcon.SEARCH.colored(QColor(255, 70, 84), QColor(0, 0, 0)))
        self.jumpQueryPage.setIconSize(QSize(150, 150))
        self.jumpQueryPage.setFixedSize(200, 200)  # 固定宽度 100，高度 40
        # 点击跳转页面
        self.jumpQueryPage.clicked.connect(lambda: parent.switchToInterface("query"))
        

        # 添加新增点位页面按钮
        self.jumpAddPage = TransparentToolButton()
        self.jumpAddPage.setIcon(FluentIcon.ADD.colored(QColor(255, 70, 84), QColor(0, 0, 0)))
        self.jumpAddPage.setIconSize(QSize(150, 150))
        self.jumpAddPage.setFixedSize(200, 200)  # 固定宽度 200，高度 200
        self.jumpAddPage.clicked.connect(lambda: parent.switchToInterface("add"))

        # self.jumpAddPage.setMinimumSize(50, 50)  # 最小尺寸
        # self.jumpAddPage.setMaximumSize(400, 400)  # 最大尺寸

        self.layout.addStretch(4)
        self.layout.addWidget(self.jumpQueryPage)
        self.layout.addStretch(1)
        self.layout.addWidget(self.jumpAddPage)
        self.layout.addStretch(4)