from qfluentwidgets import TitleLabel, BodyLabel, LineEdit, PrimaryPushButton, ElevatedCardWidget, CaptionLabel, ImageLabel, ScrollArea, FlowLayout
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QPushButton
from PyQt5.QtCore import Qt,QEasingCurve

# from step_base import BaseStep
import json
from dataclasses import dataclass
from typing import List


class MapCard(ElevatedCardWidget):
    """
    表情卡片组件，继承自ElevatedCardWidget
    用于显示一个图标和标签的卡片式组件
    """

    def __init__(self, iconPath: str, name: str, parent=None):
        """
        初始化表情卡片

        参数:
            iconPath (str): 图标文件路径
            name (str): 卡片标签文本
            parent: 父组件，默认为None
        """
        # 调用父类构造函数
        super().__init__(parent)

        # 创建图标组件，传入图标路径和父组件
        self.iconWidget = ImageLabel(iconPath, self)

        # 如果需要圆角
        self.iconWidget.setBorderRadius(8, 8, 8, 8)

        # 创建标签组件，显示卡片名称
        self.label = CaptionLabel(name, self)

        # 创建垂直布局管理器
        self.vBoxLayout = QHBoxLayout(self)

        # 设置布局对齐方式为居中
        self.vBoxLayout.setAlignment(Qt.AlignCenter)

        # 添加上方弹性空间，用于垂直居中
        self.vBoxLayout.addStretch(1)

        # 添加图标组件到布局中，水平居中对齐
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)

        # 添加中间弹性空间，分隔图标和标签
        self.vBoxLayout.addStretch(1)

        # 添加标签组件到布局中，水平居中且垂直底部对齐
        self.vBoxLayout.addWidget(
            self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)
        # 设置图标高度为200像素（宽度按比例缩放）
        self.iconWidget.scaledToHeight(150)
        # 设置卡片固定尺寸为400x400像素
        self.setFixedSize(300, 180)


class StepWidget(QMainWindow):
    def setup_ui(self):
        # super().__init__()
        # 欢迎标题
        self.title = TitleLabel("选择地图", self)

        # 创建滚动区域
        # # scroll_area = ScrollArea()
        # # # 设置滚动区域的样式
        # # scroll_area.setWidgetResizable(True)
        # # # 设置滚动条策略
        # # scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # # # 创建滚动内容容器
        # # scroll_content = QWidget()
        # # scroll_layout = QVBoxLayout(scroll_content)
        # # scroll_layout.setSpacing(10)  # 设置卡片间距
        # # scroll_layout.setContentsMargins(10, 10, 10, 10)  # 设置边距

        # # 读取地图数据
        # self.map_data = json.loads(
        #     open("./resource/maps/maps.json", "r", encoding="utf-8").read())
        # layout = FlowLayout(self, needAni=True)

        # # 设置动画效果
        # layout.setAnimation(250, QEasingCurve.OutQuad)
        # # 设置布局属性
        # layout.setContentsMargins(30, 30, 30, 30)
        # # 设置布局间距
        # layout.setVerticalSpacing(20)
        # layout.setHorizontalSpacing(10)

        # # 创建地图选择卡片
        # self.map_cards = []
        # for map_item in self.map_data['maps']:
        #     card = MapCard(map_item['url'], map_item['chinese_name'], self)
        #     # self.map_cards.append(card)
        #     layout.addWidget(card)
        
        # # 添加伸缩因子使卡片顶部对齐
        # scroll_layout.addStretch(1)
        
        # scroll_area.setWidget(scroll_content)
        # self.content_layout.addWidget(scroll_area)
        
if __name__ == "__main__":
    app = QApplication([])
    window = StepWidget()
    window.resize(800, 600)
    window.show()
    app.exec_()