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
    BodyLabel,PopupTeachingTip ,
    InfoBarIcon,TeachingTipTailPosition,
)

# 导入步骤模块
from step_one import StepOne
from step_two import StepTwo
from step_three import StepThree
from step_four import StepFour

class ValorantWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口图标
        
        # 设置窗口标题和大小
        self.setWindowTitle("超级无敌打瓦点位神器")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon("./icon/valorant_icon.icon"))

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
        
        # 初始化步骤
        self.current_step = 0
        self.update_step_indicator()
        
        # 存储选择的数据
        self.selected_map = None
        self.selected_hero = None
        self.selected_side = None
    
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
                background-color: #f0f0f0;
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
        
        # 步骤3: 选择攻防
        step3_label = BodyLabel("3. 选择攻防")
        self.step_labels.append(step3_label)
        
        # 步骤4: 技能选择
        step4_label = BodyLabel("4. 技能选择")
        self.step_labels.append(step4_label)
        
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
        self.step_one.next_step_requested.connect(self.go_to_next_step)
        
        # 创建步骤2: 选择英雄
        self.step_two = StepTwo()
        self.step_two.hero_selected.connect(self.on_hero_selected)
        self.step_two.prev_step_requested.connect(self.go_to_prev_step)
        self.step_two.next_step_requested.connect(self.go_to_next_step)
        
        # 创建步骤3: 选择攻防
        self.step_three = StepThree()
        self.step_three.side_selected.connect(self.on_side_selected)
        
        # 创建步骤4: 技能选择
        self.step_four = StepFour()
        self.step_four.next_step_requested.connect(self.go_to_next_step)
        
        # 将步骤添加到堆叠部件
        self.stacked_widget.addWidget(self.step_one)
        self.stacked_widget.addWidget(self.step_two)
        self.stacked_widget.addWidget(self.step_three)
        self.stacked_widget.addWidget(self.step_four)

        # 将堆叠部件添加到内容布局
        content_layout.addWidget(self.stacked_widget)
        
        # 将内容容器添加到主布局
        self.main_layout.addWidget(content_container, 1)  # 添加伸展因子
    
    def on_map_selected(self, map_data):
        """处理地图选择事件"""
        self.selected_map = map_data
        self.step_two.set_map_data(map_data)  # 将地图数据传递给step_two
        print(f"主窗口接收到选择的地图: {map_data.get('chinese')} ({map_data.get('english')})")
    
    def on_hero_selected(self, hero_data):
        """处理英雄选择事件"""
        self.selected_hero = hero_data
        chinese_name = hero_data.get('Chinese_name')
        hear_name = hero_data.get('name')
        print(f"主窗口接收到选择的英雄: {chinese_name} ({hear_name})")
    
    def on_side_selected(self, side_data):
        """处理地图选择事件"""
        self.selected_side = side_data
        print(f"主窗口接收到选择的攻防: {side_data}")
        self.go_to_next_step()  # 自动导航到下一步
    
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

    def go_to_next_step(self):
        """切换到下一步"""
        if self.current_step < 3:  # 0=step1, 1=step2, 2=step3, 3=step4
            self.current_step += 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.update_step_indicator()

    def go_to_prev_step(self):
        """切换到上一步"""
        if self.current_step > 0:
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.update_step_indicator()

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