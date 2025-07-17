import json
import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QSizePolicy, QLabel, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPropertyAnimation, QParallelAnimationGroup, QPointF
from PyQt5.QtGui import QFont, QResizeEvent, QPixmap, QColor
from qfluentwidgets import (
    BodyLabel, 
    PushButton, 
    FluentIcon,
    ScrollArea
)

class MapLabel(QLabel):
    """自定义地图标签类，用于显示地图图片并处理交互"""
    clicked = pyqtSignal(object)  # 点击信号，传递自身引用
    
    def __init__(self, map_data=None, parent=None):
        super().__init__(parent)
        self.map_data = map_data
        self.selected = False
        self.setFixedSize(250, 150)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)
        
        # 设置样式
        self.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)
        
        # 添加阴影效果
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(0, 0, 0, 50))
        self.shadow.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow)
        
        # 加载图片
        self.load_image()
        
        # 创建名称标签
        self.name_label = QLabel(self.map_data.get('chinese', '未知地图') if self.map_data else "", self)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px;
            font-weight: bold;
            font-size: 14px;
            border-radius: 4px;
        """)
        
        # 设置名称标签位置
        self.name_label.setGeometry(10, 115, 230, 30)  # 位于底部，留出边距
    
    def load_image(self):
        """加载并设置地图图片"""
        if not self.map_data:
            return
            
        url_path = self.map_data.get('url', '')
        if url_path.startswith('/'):
            url_path = url_path[1:]  # 移除开头的斜杠
            
        pixmap = QPixmap(url_path)
        if not pixmap.isNull():
            # 缩放图片以适应标签大小，保持纵横比并扩展以填满整个区域
            pixmap = pixmap.scaled(250, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            # 如果缩放后的图片大于容器，裁剪图片以显示中心部分
            if pixmap.width() > 250 or pixmap.height() > 150:
                # 计算裁剪的起始点，使图片居中
                x = max(0, (pixmap.width() - 250) // 2)
                y = max(0, (pixmap.height() - 150) // 2)
                # 裁剪图片
                pixmap = pixmap.copy(x, y, min(250, pixmap.width()), min(150, pixmap.height()))
            
            self.setPixmap(pixmap)
    
    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            # 创建点击动画
            click_anim = QPropertyAnimation(self.shadow, b"blurRadius")
            click_anim.setDuration(100)
            click_anim.setStartValue(10)
            click_anim.setEndValue(5)
            
            offset_anim = QPropertyAnimation(self.shadow, b"offset")
            offset_anim.setDuration(100)
            offset_anim.setStartValue(QPointF(0, 2))
            offset_anim.setEndValue(QPointF(0, 1))
            
            # 创建动画组
            anim_group = QParallelAnimationGroup()
            anim_group.addAnimation(click_anim)
            anim_group.addAnimation(offset_anim)
            
            # 添加恢复动画
            restore_click_anim = QPropertyAnimation(self.shadow, b"blurRadius")
            restore_click_anim.setDuration(100)
            restore_click_anim.setStartValue(5)
            restore_click_anim.setEndValue(10)
            
            restore_offset_anim = QPropertyAnimation(self.shadow, b"offset")
            restore_offset_anim.setDuration(100)
            restore_offset_anim.setStartValue(QPointF(0, 1))
            restore_offset_anim.setEndValue(QPointF(0, 2))
            
            restore_group = QParallelAnimationGroup()
            restore_group.addAnimation(restore_click_anim)
            restore_group.addAnimation(restore_offset_anim)
            
            # 连接动画
            anim_group.finished.connect(restore_group.start)
            
            # 启动动画
            anim_group.start()
            
            # 发送点击信号
            self.clicked.emit(self)
    
    def set_selected(self, selected):
        """设置选中状态"""
        self.selected = selected
        if selected:
            self.setStyleSheet("""
                QLabel {
                    background-color: #f5f5f5;
                    border: 3px solid rgb(250,68,84);
                    border-radius: 8px;
                }
            """)
            # 增强选中的阴影效果
            self.shadow.setBlurRadius(20)
            self.shadow.setColor(QColor(250, 68, 84, 100))
            self.shadow.setOffset(0, 4)
        else:
            self.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                }
            """)
            # 恢复默认阴影效果
            self.shadow.setBlurRadius(10)
            self.shadow.setColor(QColor(0, 0, 0, 50))
            self.shadow.setOffset(0, 2)
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        if not self.selected:
            self.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    border: 2px solid rgb(250,68,84);
                    border-radius: 8px;
                }
            """)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        if not self.selected:
            self.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                }
            """)


class StepOne(QWidget):
    # 信号定义
    map_selected = pyqtSignal(dict)  # 发送选定的地图数据
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 存储地图标签和网格布局的引用
        self.map_labels = []
        self.grid_layout = None
        self.selected_map = None
        self.selected_label = None
        
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
        
        # 创建网格布局用于地图标签
        self.grid_layout = QGridLayout()
        # 增加行间距，避免标签遮挡
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(30)
        
        # 从JSON文件加载地图数据
        maps_data = self.load_maps_data()
        
        # 创建地图标签
        self.map_labels = []
        for map_data in maps_data:
            map_label = MapLabel(map_data)
            map_label.clicked.connect(self.on_map_label_clicked)
            self.map_labels.append(map_label)
        
        # 初始布局
        self.update_grid_layout()
        
        content_layout.addLayout(self.grid_layout)
        
        # 设置滚动区域的内容
        scroll_area.setWidget(self.content_container)
        self.main_layout.addWidget(scroll_area, 1)  # 添加伸展因子
    
    def on_map_label_clicked(self, label):
        """处理地图标签点击事件"""
        map_data = label.map_data
        if map_data:
            print(f"点击了地图: {map_data.get('chinese')} ({map_data.get('english')})")
            
            # 取消之前选择的标签高亮
            if self.selected_label:
                self.selected_label.set_selected(False)
            
            # 高亮当前选择的标签
            label.set_selected(True)
            
            # 更新选择的地图和标签
            self.selected_map = map_data
            self.selected_label = label
            
            # 发送选择的地图信号
            self.map_selected.emit(map_data)

    def update_grid_layout(self):
        """更新网格布局"""
        # 清除现有布局中的所有标签
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                self.grid_layout.removeWidget(item.widget())
        
        # 计算最佳列数
        width = self.width()
        # 根据窗口宽度动态计算列数，考虑标签固定宽度(250)和水平间距(20)
        label_width_with_spacing = 250 + 20  # 标签宽度加上水平间距
        
        # 计算可以容纳的最大列数，考虑左右边距
        available_width = width - 40  # 减去左右边距
        max_cols = max(1, int(available_width / label_width_with_spacing))
        
        # 限制最大列数为4，确保布局美观
        cols = min(max_cols, 4)
        
        # 设置网格布局的对齐方式为居中
        self.grid_layout.setAlignment(Qt.AlignCenter)
        
        # 重新布局标签
        for i, label in enumerate(self.map_labels):
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(label, row, col)
    
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
        # 隐藏所有标签
        for label in self.map_labels:
            label.hide()
        
        # 清除选择状态
        self.selected_map = None
        self.selected_label = None
    
    def show_content(self):
        """重新显示内容"""
        # 显示所有标签
        for label in self.map_labels:
            label.show()