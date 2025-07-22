# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel

from qfluentwidgets import Pivot, setTheme, Theme,CardWidget


class QueryPage(QWidget):
    """主演示窗口，展示Pivot导航控件和StackedWidget多页面切换功能"""

    def __init__(self):
        super().__init__()
        # 设置窗口样式
        self.setStyleSheet("""
            Demo{background: white}  /* 窗口背景设为白色 */
            QLabel{
                font: 20px 'Segoe UI';  /* 标签字体设置 */
                background: rgb(242,242,242);  /* 标签背景设为浅灰色 */
                border-radius: 8px;  /* 圆角边框 */
            }
        """)
        # 不设置固定大小，允许窗口自由调整
        self.setMinimumSize(300, 300)  # 设置最小尺寸限制

        # 初始化控件
        self.pivot = Pivot(self)  # 顶部导航栏控件
        self.stackedWidget = QStackedWidget(self)  # 多页面堆叠容器
        self.vBoxLayout = QVBoxLayout(self)  # 主垂直布局
        card = CardWidget()
        card.setFixedSize(300, 200) # 设置卡片大小

        # 加载图片并设置背景
        pixmap = QPixmap("./resource/maps/abyss_cover.png")
        background = QLabel(card)
        background.setPixmap(pixmap.scaled(card.size()))  # 自适应卡片大小
        background.setGeometry(0, 0, card.width(), card.height()) # 设置背景图片位置
                
                
        # 创建三个页面内容
        self.songInterface = card  
        self.albumInterface = QLabel('第二', self) 
        self.artistInterface = QLabel('第三', self)  

        # 添加子界面到导航和堆叠容器
        self.addSubInterface(self.songInterface, 'songInterface', '选择地图')
        self.addSubInterface(self.albumInterface, 'albumInterface', '选择英雄')
        self.addSubInterface(self.artistInterface, 'artistInterface', '选择攻防')

        # 设置布局
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)  # 导航栏居中
        self.vBoxLayout.addWidget(self.stackedWidget)  # 添加堆叠容器
        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)  # 设置布局边距

        # 设置默认显示页面
        self.stackedWidget.setCurrentWidget(self.songInterface)
        self.pivot.setCurrentItem(self.songInterface.objectName())
        

        # 禁止导航栏点击
        self.pivot.setDisabled(True)
  

    def addSubInterface(self, widget: QLabel, objectName, text):
        """
        添加子界面到导航和堆叠容器
        
        参数:
            widget: 要添加的界面控件
            objectName: 控件对象名称(用于导航标识)
            text: 导航栏显示的文本
        """
        widget.setObjectName(objectName)  # 设置控件对象名
        # widget.setAlignment(Qt.AlignCenter)  # 内容居中
        self.stackedWidget.addWidget(widget)  # 添加到堆叠容器
        self.pivot.addItem(routeKey=objectName, text=text)  # 添加到导航栏

    def nextPivot(self):
        """
        切换到下一个导航项
        """
        # 连接导航栏切换信号
        self.pivot.currentItemChanged.connect(
            lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))

if __name__ == '__main__':
    # 启用高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 创建并运行应用
    app = QApplication(sys.argv)
    w = QueryPage()  # 创建主窗口
    w.show()  # 显示窗口
    app.exec_()  # 进入事件循环