import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QVBoxLayout, 
    QHBoxLayout, 
    QWidget, 
    QStackedWidget,
    QLabel
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from qfluentwidgets import (
    NavigationWidget, 
    NavigationItemPosition, 
    NavigationDisplayMode,
    FluentIcon,
    PushButton,
    BodyLabel
)

# 导入步骤模块
from step_one import StepOne
from step_two import StepTwo

class ValorantWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和大小
        self.setWindowTitle("超级无敌打瓦点位神器")
        self.resize(1000, 700)
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 创建标题区域
        self.create_title_area()
        
        # 创建内容区域
        self.create_content_area()
        
        # 创建底部导航区域
        self.create_bottom_nav()
        
        # 初始化步骤
        self.current_step = 0
        self.update_step_indicator()
        
        # 存储选择的地图数据
        self.selected_map = None
    
    def create_title_area(self):
        """创建标题区域"""
        # 创建标题容器
        title_container = QWidget()
        title_container.setObjectName("titleContainer")
        title_container.setStyleSheet("""
            #titleContainer {
                background-color: #fa4454;
                min-height: 60px;
            }
        """)
        
        # 创建标题布局
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 0, 20, 0)
        
        # 创建标题标签
        title_label = QLabel("超级无敌打瓦点位神器")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        
        # 将标题标签添加到布局
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)  # 添加伸展因子
        
        # 将标题容器添加到主布局
        self.main_layout.addWidget(title_container)
    
    def create_content_area(self):
        """创建内容区域"""
        # 创建内容容器
        content_container = QWidget()
        content_container.setObjectName("contentContainer")
        content_container.setStyleSheet("""
            #contentContainer {
                background-color: white;
            }
        """)
        
        # 创建内容布局
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 创建步骤指示器
        self.step_indicator = QWidget()
        self.step_indicator.setFixedHeight(50)
        self.step_indicator.setObjectName("stepIndicator")
        self.step_indicator.setStyleSheet("""
            #stepIndicator {
                background-color: #f5f5f5;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        
        # 创建步骤指示器布局
        step_layout = QHBoxLayout(self.step_indicator)
        step_layout.setContentsMargins(20, 0, 20, 0)
        
        # 创建步骤标签
        self.step_labels = []
        
        # 步骤1: 选择地图
        step1_label = BodyLabel("1. 选择地图")
        step1_label.setObjectName("activeStep")
        self.step_labels.append(step1_label)
        
        # 步骤2: 选择英雄
        step2_label = BodyLabel("2. 选择英雄")
        self.step_labels.append(step2_label)
        
        # 添加步骤标签到布局
        for label in self.step_labels:
            step_layout.addWidget(label)
            # 添加间隔
            if label != self.step_labels[-1]:
                separator = BodyLabel(" > ")
                separator.setObjectName("stepSeparator")
                step_layout.addWidget(separator)
        
        step_layout.addStretch(1)  # 添加伸展因子
        
        # 将步骤指示器添加到内容布局
        content_layout.addWidget(self.step_indicator)
        
        # 创建堆叠部件用于切换不同步骤
        self.stacked_widget = QStackedWidget()
        
        # 创建步骤1: 选择地图
        self.step_one = StepOne()
        self.step_one.map_selected.connect(self.on_map_selected)
        
        # 创建步骤2: 选择英雄
        self.step_two = StepTwo()
        
        # 将步骤添加到堆叠部件
        self.stacked_widget.addWidget(self.step_one)
        self.stacked_widget.addWidget(self.step_two)
        
        # 将堆叠部件添加到内容布局
        content_layout.addWidget(self.stacked_widget)
        
        # 将内容容器添加到主布局
        self.main_layout.addWidget(content_container, 1)  # 添加伸展因子
    
    def create_bottom_nav(self):
        """创建底部导航区域"""
        # 创建底部导航容器
        bottom_nav = QWidget()
        bottom_nav.setObjectName("bottomNav")
        bottom_nav.setStyleSheet("""
            #bottomNav {
                background-color: #f5f5f5;
                min-height: 60px;
                border-top: 1px solid #e0e0e0;
            }
        """)
        
        # 创建底部导航布局
        nav_layout = QHBoxLayout(bottom_nav)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        
        # 添加伸展因子
        nav_layout.addStretch(1)
        
        # 创建上一步按钮
        self.prev_button = PushButton("上一步")
        # 使用向左的箭头图标，尝试几种可能的名称
        try:
            # 尝试使用LEFT图标
            self.prev_button.setIcon(FluentIcon.LEFT)
        except:
            try:
                # 尝试使用BACK图标
                self.prev_button.setIcon(FluentIcon.BACK)
            except:
                # 如果都不存在，则不设置图标
                pass
        self.prev_button.clicked.connect(self.go_to_prev_step)
        self.prev_button.setEnabled(False)  # 初始禁用
        
        # 创建下一步按钮
        self.next_button = PushButton("下一步")
        self.next_button.setIcon(FluentIcon.CHEVRON_RIGHT)
        # PushButton没有setIconRight方法，尝试使用其他方式设置图标位置
        try:
            # 尝试使用其他可能的方法设置图标位置
            self.next_button.setProperty("iconPosition", "right")
        except:
            # 如果没有合适的方法，就不设置图标位置
            pass
        self.next_button.clicked.connect(self.go_to_next_step)
        
        # 将按钮添加到布局
        nav_layout.addWidget(self.prev_button)
        nav_layout.addSpacing(10)
        nav_layout.addWidget(self.next_button)
        
        # 将底部导航添加到主布局
        self.main_layout.addWidget(bottom_nav)
    
    def on_map_selected(self, map_data):
        """处理地图选择事件"""
        self.selected_map = map_data
        print(f"主窗口接收到选择的地图: {map_data.get('chinese')}")
    
    def go_to_next_step(self):
        """前往下一步"""
        if self.current_step == 0:  # 当前在第一步
            # 检查是否已选择地图
            if not self.selected_map:
                print("请先选择一个地图")
                return
            
            # 清空step_one的内容
            self.step_one.clear_content()
            
            # 将选择的地图传递给step_two
            self.step_two.set_map_data(self.selected_map)
            
            # 切换到下一步
            self.current_step = 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            
            # 更新按钮状态
            self.prev_button.setEnabled(True)
            
            # 更新步骤指示器
            self.update_step_indicator()
    
    def go_to_prev_step(self):
        """返回上一步"""
        if self.current_step > 0:  # 确保不是第一步
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            
            # 更新按钮状态
            self.prev_button.setEnabled(self.current_step > 0)
            
            # 更新步骤指示器
            self.update_step_indicator()
    
    def update_step_indicator(self):
        """更新步骤指示器"""
        # 重置所有步骤标签样式
        for i, label in enumerate(self.step_labels):
            if i == self.current_step:
                label.setStyleSheet("""
                    font-weight: bold;
                    color: #fa4454;
                """)
            else:
                label.setStyleSheet("")

if __name__ == "__main__":
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    
    # 创建主窗口
    window = ValorantWizard()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())