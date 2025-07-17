from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import (PushButton, MessageBox, BodyLabel, 
                           ScrollArea, SmoothScrollArea)

class StepFour(QWidget):
    """技能选择页面"""
    
    next_step_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """初始化UI"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # 标题
        self.title_label = BodyLabel("技能选择", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        self.main_layout.addWidget(self.title_label)
        
        # 内容区域
        self.scroll_area = SmoothScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)
        
        # 下一步按钮
        self.next_button = PushButton("下一步", self)
        self.next_button.clicked.connect(self.on_next_step)
        self.main_layout.addWidget(self.next_button)
        
        # 存储接收的数据
        self.received_data = None
        
    def receive_data(self, data):
        """接收从step two传递的数据"""
        self.received_data = data
        print(f"StepFour接收到的数据: {data}")
        
        # 显示接收到的数据
        info_label = QLabel(f"""
            地图: {data.get('map', '未知')}
            英雄: {data.get('hero', {}).get('Chinese_name', '未知')}
            阵营: {'进攻' if data.get('side') == 'attack' else '防守'}
        """)
        self.scroll_layout.addWidget(info_label)
        
    def on_next_step(self):
        """处理下一步按钮点击"""
        self.next_step_requested.emit()