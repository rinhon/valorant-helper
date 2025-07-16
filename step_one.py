import json
import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QSizePolicy, QLabel, QFrame
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QResizeEvent, QPixmap
from qfluentwidgets import (
    CardWidget, 
    BodyLabel, 
    PushButton, 
    FluentIcon,
    ScrollArea
)

class StepOne(QWidget):
    # 信号定义
    map_selected = pyqtSignal(dict)  # 发送选定的地图数据
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 存储卡片和网格布局的引用
        self.cards = []
        self.grid_layout = None
        self.selected_map = None
        self.selected_card = None
        
        # 创建布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(30)
        
        # 创建内容区域
        self.create_content_area()
        
    def load_maps_data(self):
        """从maps.json加载地图数据"""
        try:
            with open('./maps/maps.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('maps', [])
        except Exception as e:
            print(f"加载地图数据失败: {e}")
            return []

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
        
        # 创建网格布局用于卡片
        self.grid_layout = QGridLayout()
        # 增加行间距，避免卡片遮挡
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(30)
        
        # 从JSON文件加载地图数据
        maps_data = self.load_maps_data()
        
        # 创建卡片
        self.cards = []
        for map_data in maps_data:
            card = CardWidget()
            # 设置固定大小，确保卡片大小不变
            card.setFixedSize(250, 150)
            
            # 为卡片添加内容
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(0, 0, 0, 0)  # 移除内边距
            card_layout.setSpacing(0)
            
            # 创建背景图片标签
            bg_label = QLabel()
            bg_label.setFixedSize(250, 150)
            
            # 加载图片
            url_path = map_data.get('url', '')
            if url_path.startswith('/'):
                url_path = url_path[1:]  # 移除开头的斜杠
            pixmap = QPixmap(url_path)
            if not pixmap.isNull():
                # 缩放图片以适应卡片大小
                pixmap = pixmap.scaled(250, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                bg_label.setPixmap(pixmap)
                bg_label.setScaledContents(True)
            
            # 创建地图名称标签
            name_label = QLabel(map_data.get('chinese', '未知地图'))
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0.5);
                color: white;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
            """)
            
            # 将标签添加到卡片布局
            card_layout.addWidget(bg_label)
            
            # 创建一个水平布局来放置名称标签在底部
            bottom_layout = QHBoxLayout()
            bottom_layout.addWidget(name_label)
            bottom_layout.setContentsMargins(0, 0, 0, 10)  # 底部边距
            
            # 将底部布局添加到卡片布局
            card_layout.addLayout(bottom_layout)
            
            # 添加鼠标悬停效果
            card.setStyleSheet("""
                CardWidget {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                }
                CardWidget:hover {
                    border: 2px solid #0078d4;
                }
            """)
            
            # 存储地图数据到卡片的属性中
            card.setProperty("map_data", map_data)
            
            # 添加点击事件
            card.mousePressEvent = lambda event, c=card: self.on_card_clicked(c)
            
            self.cards.append(card)
        
        # 初始布局
        self.update_grid_layout()
        
        content_layout.addLayout(self.grid_layout)
        
        # 设置滚动区域的内容
        scroll_area.setWidget(self.content_container)
        self.main_layout.addWidget(scroll_area, 1)  # 添加伸展因子
    
    def on_card_clicked(self, card):
        """处理卡片点击事件"""
        map_data = card.property("map_data")
        if map_data:
            print(f"点击了地图: {map_data.get('chinese')} ({map_data.get('english')})")
            
            # 取消之前选择的卡片高亮
            if self.selected_card:
                self.selected_card.setStyleSheet("""
                    CardWidget {
                        background-color: white;
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                    }
                    CardWidget:hover {
                        border: 2px solid #0078d4;
                    }
                """)
            
            # 高亮当前选择的卡片
            card.setStyleSheet("""
                CardWidget {
                    background-color: white;
                    border: 2px solid #0078d4;
                    border-radius: 8px;
                }
            """)
            
            # 更新选择的地图和卡片
            self.selected_map = map_data
            self.selected_card = card
            
            # 发送选择的地图信号
            self.map_selected.emit(map_data)

    def update_grid_layout(self):
        """更新网格布局"""
        # 清除现有布局中的所有卡片
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                self.grid_layout.removeWidget(item.widget())
        
        # 计算最佳列数
        width = self.width()
        # 根据窗口宽度动态计算列数，考虑卡片固定宽度(250)和水平间距(20)
        card_width_with_spacing = 250 + 20  # 卡片宽度加上水平间距
        
        # 计算可以容纳的最大列数，考虑左右边距
        available_width = width - 40  # 减去左右边距
        max_cols = max(1, int(available_width / card_width_with_spacing))
        
        # 限制最大列数为4，确保布局美观
        cols = min(max_cols, 4)
        
        # 设置网格布局的对齐方式为居中
        self.grid_layout.setAlignment(Qt.AlignCenter)
        
        # 重新布局卡片
        for i, card in enumerate(self.cards):
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(card, row, col)
    
    def resizeEvent(self, event: QResizeEvent):
        """处理窗口大小变化事件"""
        super().resizeEvent(event)
        # 当窗口大小变化时，更新网格布局
        self.update_grid_layout()
    
    def get_selected_map(self):
        """返回当前选定的地图"""
        return self.selected_map
        
    def clear_content(self):
        """清空内容"""
        # 隐藏所有卡片
        for card in self.cards:
            card.hide()
        
        # 清除选择状态
        self.selected_map = None
        self.selected_card = None