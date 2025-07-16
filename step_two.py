from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from qfluentwidgets import (
    BodyLabel, 
    PushButton, 
    FluentIcon,
    ScrollArea,
    CardWidget
)

class StepTwo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 存储地图数据
        self.map_data = None
        
        # 创建布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(30)
        
        # 创建内容区域
        self.create_content_area()
    
    def create_content_area(self):
        """创建内容区域"""
        # 创建滚动区域
        scroll_area = ScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 创建内容容器
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignTop)
        
        # 创建地图信息区域
        self.map_info_widget = QWidget()
        self.map_info_layout = QVBoxLayout(self.map_info_widget)
        self.map_info_layout.setContentsMargins(0, 0, 0, 0)
        self.map_info_layout.setSpacing(20)
        
        # 创建地图标题标签
        self.map_title = BodyLabel("")
        self.map_title.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        self.map_info_layout.addWidget(self.map_title)
        
        # 创建地图图片区域
        self.map_image = QLabel()
        self.map_image.setAlignment(Qt.AlignCenter)
        self.map_image.setMinimumHeight(300)
        self.map_image.setStyleSheet("background-color: #f0f0f0; border-radius: 8px;")
        self.map_info_layout.addWidget(self.map_image)
        
        # 创建地图描述标签
        self.map_description = BodyLabel("请先在上一步选择地图")
        self.map_description.setWordWrap(True)
        self.map_info_layout.addWidget(self.map_description)
        
        # 将地图信息区域添加到内容布局
        content_layout.addWidget(self.map_info_widget)
        
        # 设置滚动区域的内容
        scroll_area.setWidget(self.content_container)
        self.main_layout.addWidget(scroll_area, 1)  # 添加伸展因子
    
    def set_map_data(self, map_data):
        """接收并处理地图数据"""
        if not map_data:
            return
            
        self.map_data = map_data
        
        # 更新UI显示
        self.map_title.setText(f"{map_data.get('chinese', '未知地图')} ({map_data.get('english', 'Unknown')})")
        
        # 加载地图图片
        url_path = map_data.get('url', '')
        if url_path.startswith('/'):
            url_path = url_path[1:]  # 移除开头的斜杠
            
        pixmap = QPixmap(url_path)
        if not pixmap.isNull():
            # 缩放图片以适应显示区域，保持纵横比
            pixmap = pixmap.scaled(800, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.map_image.setPixmap(pixmap)
            
        # 更新描述信息（这里可以添加更多地图相关信息）
        self.map_description.setText(f"您选择了 {map_data.get('chinese', '未知地图')} 地图。")