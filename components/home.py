import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QPixmap,QColor
from PyQt5.QtWidgets import QStackedWidget, QLabel
from qfluentwidgets import TitleLabel, BodyLabel, CardWidget, FluentIcon, ToolButton
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
        self.jumpQueryPage = ToolButton()
        self.jumpQueryPage.setIcon(FluentIcon.SEARCH.colored(QColor(255, 255, 255), QColor(0, 0, 0)))
        self.jumpQueryPage.setIconSize(QSize(150, 150))
        self.jumpQueryPage.setFixedSize(200, 200)  # 固定宽度 100，高度 40
        self.jumpQueryPage.setStyleSheet("""
                QPushButton {
                    border: 2px solid transparent;  /* 默认透明边框 */
                }
                QPushButton:hover {
                    border: 2px solid #0078D4;      /* 悬停时蓝色边框 */
                }
            """)
 

        # 添加新增点位页面按钮
        self.jumpAddPage = ToolButton()
        self.jumpAddPage.setIcon(FluentIcon.ADD)
        self.jumpAddPage.setIconSize(QSize(150, 150))
        self.jumpAddPage.setFixedSize(200, 200)  # 固定宽度 200，高度 200

        # self.jumpAddPage.setMinimumSize(50, 50)  # 最小尺寸
        # self.jumpAddPage.setMaximumSize(400, 400)  # 最大尺寸

        self.layout.addStretch(4)
        self.layout.addWidget(self.jumpQueryPage)
        self.layout.addStretch(1)
        self.layout.addWidget(self.jumpAddPage)
        self.layout.addStretch(4)