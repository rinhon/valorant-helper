from qfluentwidgets import FluentIcon, PushButton, BodyLabel, ComboBox, SwitchButton, IndicatorPosition, ExpandGroupSettingCard, PrimaryToolButton, PrimaryPushButton, ToolButton
from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SubtitleLabel, setFont, setTheme, Theme
from components.upload import AddPointPage
from qfluentwidgets import FluentIcon as FIF
import time
import os
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, QEventLoop, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame, QSizePolicy, QPushButton, QHBoxLayout, QScrollArea, QComboBox
from qframelesswindow import FramelessWindow, StandardTitleBar
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, PushButton, TitleLabel, BodyLabel, PrimaryPushButton, FluentWindow,
                         FlowLayout,   FluentIcon, CardWidget, qrouter, setTheme, Theme)
import sys
from components.home import Home # Assuming home.py is in the same directory
from components.queryPage import QueryPage # Assuming upload.py is in the same directory


class ValorantMainWindow(QMainWindow):
    """主向导窗口"""
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        # 主界面 功能：1.查询点位 新增点位
        self.homeInterface = Home(self)
        self.homeInterface.setObjectName("主页")  
        
        self.qureyPointInterface = QueryPage( )
        self.qureyPointInterface.setObjectName("查询点位")  
        
        self.addNewPointInterface = AddPointPage()
        self.addNewPointInterface.setObjectName("新增点位")  

        self.settingInterface = CardWidget( self)
        self.settingInterface.setObjectName("设置")  

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        """初始化导航栏"""
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')

        # 添加分隔符
        # self.navigationInterface.addSeparator()

        self.addSubInterface(self.qureyPointInterface, FIF.SEARCH, '查询点位')
        self.addSubInterface(self.addNewPointInterface, FIF.ADD, '新增点位')

        self.addSubInterface(self.settingInterface, FIF.SETTING,
                             '设置', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        """初始化窗口"""
        self.resize(900, 700)
        self.setWindowIcon(QIcon('./resource/icon/valorant_icon.icon'))
        self.setWindowTitle('究极无敌打瓦神器')

    def switchToInterface(self, routeKey: str):
        """根据路由键切换界面"""
        interface_map = {
            "home": self.homeInterface,
            "add": self.addNewPointInterface,
            "query": self.qureyPointInterface,
            "settings": self.settingInterface
        }
        
        if routeKey in interface_map:
            self.switchTo(interface_map[routeKey])
            self.navigationInterface.setCurrentItem(routeKey)
        

if __name__ == '__main__':
    # 启用高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # 设置主题
    setTheme(Theme.LIGHT)

    # 创建主窗口
    window = Window()
    window.show()

    sys.exit(app.exec_())
