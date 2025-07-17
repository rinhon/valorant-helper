from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from qfluentwidgets import (PrimaryPushButton, PushButton, FluentIcon, 
                           TitleLabel, CardWidget, TransparentToolButton, 
                           ScrollArea, isDarkTheme,PopupTeachingTip,InfoBarIcon,TeachingTipTailPosition)
from PyQt5.QtGui import QIcon


class StepThree(QWidget):
    """第三步：选择攻防"""
    
    side_selected = pyqtSignal(dict)  # 发送选择的攻防信息
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_side = None
        self.setup_ui()
    
    def setup_ui(self):
        """初始化界面"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        
        # 标题
        self.title_label = TitleLabel("选择攻防")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # 攻防选择卡片容器
        self.sides_container = QWidget()
        self.sides_x_layout = QHBoxLayout(self.sides_container)
        #水平居中
        self.sides_x_layout.setAlignment(Qt.AlignCenter)
        self.sides_x_layout.setContentsMargins(0, 0, 0, 0)
        self.sides_x_layout.setSpacing(20)
   

        # 进攻按钮
        self.attack_button = PushButton("进攻", self)
        self.attack_button.setFixedSize(150, 60)
        self.attack_button.setCheckable(True)
        self.attack_button.clicked.connect(lambda: self.on_side_button_clicked("attack"))
        
        # 防守按钮
        self.defense_button = PushButton("防守", self)
        self.defense_button.setFixedSize(150, 60)
        self.defense_button.setCheckable(True)
        self.defense_button.clicked.connect(lambda: self.on_side_button_clicked("defense"))

        # 添加按钮到布局
        self.sides_x_layout.addWidget(self.attack_button)
        self.sides_x_layout.addWidget(self.defense_button)
        self.sides_x_layout.addStretch(1)
        
        # 底部按钮布局
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 20, 0, 0)
        self.button_layout.setSpacing(15)
        
        # 返回按钮
        self.back_button = PushButton("返回", self)
        self.back_button.setIcon(FluentIcon.RETURN)
        self.back_button.clicked.connect(self.on_back_clicked)
        
        # 确认按钮
        self.confirm_button = PrimaryPushButton("确认选择", self)
        self.confirm_button.setIcon(FluentIcon.ACCEPT)
        self.confirm_button.clicked.connect(self.on_confirm_clicked)
        
        # 添加按钮到布局
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.confirm_button)
        
        # 添加组件到主布局
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.sides_container, 1)
        self.main_layout.addLayout(self.button_layout)
        
    def on_confirm_clicked(self):
        """处理确认按钮点击事件"""
        if self.selected_side:
            # 确保数据包含所有必要字段
            confirm_data = {
                "side": self.selected_side["side"],
                "map": self.map_data,
                "hero": self.selected_hero
            }
            self.side_selected.emit(confirm_data)
            print(f"{confirm_data}")
            print(f"已选择攻防: {self.selected_side['side']}")
            
        else:
            self.check_side_selected()
            

    def check_side_selected(self):
        PopupTeachingTip .create(
            target=self.confirm_button,
            icon=InfoBarIcon.WARNING,
            title='？',
            content="你进攻防守都不知道？",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
    
    
    def on_back_clicked(self):
        """处理返回按钮点击事件"""
        from step_two import StepTwo
        parent = self.parent()
        if parent:
            # 获取父窗口中的 step_two 实例
            step_two = parent.findChild(StepTwo)
            if step_two:
                # 隐藏当前界面，显示 step_two
                self.hide()
                step_two.show()
    
    def receive_data(self, data):
        """接收从step two传递的数据"""
        self.map_data = data.get('map')
        self.selected_hero = data.get('hero')
        # 更新标题，显示选择的英雄名称
        if self.selected_hero and 'Chines_name' in self.selected_hero:
            self.title_label.setText(f"为 {self.selected_hero['Chines_name']} 选择攻防")

    def clear_content(self):
        """清除内容"""
        self.selected_side = None
        self.update_selection_style()
        self.title_label.setText("选择攻防")
    
    def on_side_button_clicked(self, side):
        """处理阵营选择按钮点击"""
        self.selected_side = {"side": side, "Chinese_name": "进攻" if side == "attack" else "防守"}
        
        # 切换按钮选中状态
        if side == "attack":
            self.attack_button.setChecked(True)
            self.defense_button.setChecked(False)
        else:
            self.attack_button.setChecked(False)
            self.defense_button.setChecked(True)
    
    def show_content(self):
        """显示内容"""
        self.show()
        # 如果有选择的英雄，更新标题
        if self.selected_hero and 'Chines_name' in self.selected_hero:
            self.title_label.setText(f"为 {self.selected_hero['Chines_name']} 选择攻防")