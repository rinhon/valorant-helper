from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QPushButton
from PyQt5.QtCore import Qt, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QEnterEvent, QMouseEvent, QDragLeaveEvent
from qfluentwidgets import LineEdit, PrimaryPushButton, ElevatedCardWidget, CaptionLabel, ImageLabel, ScrollArea, FlowLayout

# from step_base import BaseStep
import json
from dataclasses import dataclass
from typing import List


class MapCard(ElevatedCardWidget):
    """
    地图卡片组件，继承自ElevatedCardWidget
    用于显示一个图标和标签的卡片式组件，并支持鼠标交互
    """
    # 定义一个信号，当卡片被点击时发出，并携带卡片信息（例如：名称和图标路径）
    clicked = pyqtSignal(str, str)

    def __init__(self, iconPath: str, name: str, parent=None):
        """
        初始化地图卡片

        参数:
            iconPath (str): 图标文件路径
            name (str): 卡片标签文本
            parent: 父组件，默认为None
        """
        super().__init__(parent)
        self.iconPath = iconPath  # 存储图标路径
        self.name = name         # 存储卡片名称

        # 设置卡片默认样式
        self.setStyleSheet(
            # 初始边框透明
            "MapCard { border: 2px solid transparent; }")

        # 创建图标组件，传入图标路径和父组件
        self.imageLabel = ImageLabel(iconPath, self)

        # 如果需要圆角
        self.imageLabel.setBorderRadius(8, 8, 8, 8)
        self.setBorderRadius(8)
        # 创建标签组件，显示卡片名称
        self.label = CaptionLabel(name, self)
        self.label.setAlignment(Qt.AlignCenter)

        # 创建垂直布局管理器
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.imageLabel, 0, Qt.AlignCenter)
        self.vBoxLayout.addStretch(2)
        self.vBoxLayout.addWidget(
            self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

        self.imageLabel.scaledToHeight(155)
        self.setFixedSize(300, 180)

    # --- 鼠标事件处理方法 ---

    def enterEvent(self, event: QEnterEvent):
        """ 鼠标进入事件 """
        self.setStyleSheet(
            # 鼠标进入时边框变红
            "MapCard { border: 4px solid red;border-radius: 8px; }")
        super().enterEvent(event)

    def leaveEvent(self, event: QDragLeaveEvent):
        """ 鼠标离开事件 """
        self.setStyleSheet(
            # 鼠标离开时边框恢复透明
            "MapCard { border: 4px solid transparent; border-radius: 8px;}")
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """ 鼠标按下事件 """
        if event.button() == Qt.LeftButton:  # 检查是否是左键点击
            # 鼠标点击时边框可以瞬间变蓝或其他颜色，提供视觉反馈
            self.setStyleSheet(
                "MapCard { border: 4px solid blue; border-radius: 8px;}")
            # 发出 clicked 信号，并传递当前卡片的信息
            self.clicked.emit(self.name, self.iconPath)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ 鼠标释放事件 """
        # 鼠标释放时，如果仍在卡片上，恢复红色边框；如果离开了，则会由 leaveEvent 处理为透明
        if self.rect().contains(event.pos()):
            self.setStyleSheet("MapCard { border: 4px solid red; }")
        else:
            self.setStyleSheet("MapCard { border: 4px solid transparent; }")
        super().mouseReleaseEvent(event)


class MapSelect(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)


        # FlowLayout的父级是container
        self.flowLayout = FlowLayout(self, needAni=False)

        
        # 自定义动画参数
        # self.layout.setAnimation(250, QEasingCurve.OutQuad)
        self.flowLayout .setContentsMargins(30, 30, 30, 30)
        self.flowLayout .setVerticalSpacing(20)
        self.flowLayout .setHorizontalSpacing(10)

        

        # 读取地图数据
        self.map_data = json.loads(
            open("./resource/maps/maps.json", "r", encoding="utf-8").read())

        # 创建地图选择卡片
        self.map_cards = []
        for map_item in self.map_data['maps']:
            # 创建卡片，父组件依然是 self，这是为了方便管理信号槽等，
            # 但关键是把它添加到 FlowLayout 中
            card = MapCard(map_item['url'],
                           map_item['chinese_name'], self)
            self.map_cards.append(card)  # 可以把卡片存储起来方便后续操作

            # 关键修改：将卡片添加到 FlowLayout 中
            self.flowLayout.addWidget(card)


if __name__ == '__main__':
    # 启用高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    import sys
    # 创建并运行应用
    app = QApplication(sys.argv)
    w = MapSelect()  # 创建主窗口
    w.setFixedSize(1200, 800)
    w.show()  # 显示窗口
    app.exec_()  # 进入事件循环
