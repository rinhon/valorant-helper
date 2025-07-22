import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from qfluentwidgets import (
    ComboBox, LineEdit, PlainTextEdit, PushButton, 
    FluentIcon, CardWidget, ScrollArea, setTheme, Theme
)
from qfluentwidgets import FluentIcon as FIF

class ImageDisplayCard(CardWidget):
    """单个图片显示卡片"""
    removeClicked = pyqtSignal(str)  # 发射要删除的图片路径
    
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setFixedSize(200, 180)
        
        layout = QVBoxLayout(self)
        
        # 图片显示区域
        self.image_label = QLabel()
        self.image_label.setFixedSize(180, 140)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
            }
        """)
        
        # 加载并显示图片
        self.load_image()
        
        # 删除按钮
        self.remove_button = PushButton("删除", self)
        self.remove_button.setIcon(FIF.DELETE)
        self.remove_button.setFixedHeight(30)
        self.remove_button.clicked.connect(self.on_remove_clicked)
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.remove_button)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
    
    def load_image(self):
        """加载并显示图片"""
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            # 按比例缩放图片以适应标签大小
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("❌\n图片加载失败")
            self.image_label.setStyleSheet(self.image_label.styleSheet() + 
                                         "color: #FF6B6B; font-size: 14px;")
    
    def on_remove_clicked(self):
        """处理删除按钮点击"""
        self.removeClicked.emit(self.image_path)
class AddPointPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("表单页面")
        self.setFixedSize(1200, 800)
        
        # 设置主题
        setTheme(Theme.LIGHT)
        
        # 创建滚动区域
        scroll_area = ScrollArea(self)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        
        # 内容布局
        content_layout = QVBoxLayout(scroll_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(30, 30, 30, 30)
        
        # 第一行：四个下拉选择器
        first_row_layout = QHBoxLayout()
        
        # 选择地图
        map_combo = ComboBox()
        map_combo.addItems(["选择地图", "地图1", "地图2", "地图3"])
        map_combo.setFixedWidth(250)
        
        # 选择英雄
        hero_combo = ComboBox()
        hero_combo.addItems(["选择英雄", "英雄1", "英雄2", "英雄3"])
        hero_combo.setFixedWidth(250)
        
        # 英雄技能
        skill_combo = ComboBox()
        skill_combo.addItems(["英雄技能", "技能1", "技能2", "技能3"])
        skill_combo.setFixedWidth(250)
        
        # 进攻防守
        position_combo = ComboBox()
        position_combo.addItems(["进攻防守", "进攻", "防守"])
        position_combo.setFixedWidth(250)
        
        first_row_layout.addWidget(map_combo)
        first_row_layout.addWidget(hero_combo)
        first_row_layout.addWidget(skill_combo)
        first_row_layout.addWidget(position_combo)
        first_row_layout.addStretch()
        
        content_layout.addLayout(first_row_layout)
        
        # 第二行：站位和描点相关
        second_row_layout = QHBoxLayout()
        
        # 左侧：站位
        position_layout = QVBoxLayout()
        position_input = LineEdit()
        position_input.setPlaceholderText("站位")
        position_input.setFixedWidth(300)
        
        position_detail_input = LineEdit()
        position_detail_input.setPlaceholderText("站位详情")
        position_detail_input.setFixedWidth(300)
        
        position_layout.addWidget(position_input)
        position_layout.addWidget(position_detail_input)
        
        # 站位图片上传
        position_label = QLabel("站位图片上传")
        position_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        position_layout.addWidget(position_label)
        
        # position_image_card = ImageDisplayCard()
        # position_layout.addWidget(position_image_card)
        
        # 右侧：描点
        point_layout = QVBoxLayout()
        point_input = LineEdit()
        point_input.setPlaceholderText("描点")
        point_input.setFixedWidth(300)
        
        point_detail_input = LineEdit()
        point_detail_input.setPlaceholderText("描点详情")
        point_detail_input.setFixedWidth(300)
        
        point_layout.addWidget(point_input)
        point_layout.addWidget(point_detail_input)
        
        # 描点图片上传
        point_label = QLabel("描点图片上传")
        point_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        point_layout.addWidget(point_label)
        
        # point_image_card = ImageDisplayCard()
        # point_layout.addWidget(point_image_card)
        
        second_row_layout.addLayout(position_layout)
        second_row_layout.addSpacing(50)
        second_row_layout.addLayout(point_layout)
        second_row_layout.addStretch()
        
        content_layout.addLayout(second_row_layout)
        
        # 第三行：落点相关
        third_row_layout = QHBoxLayout()
        
        # 左侧：落点
        drop_layout = QVBoxLayout()
        drop_input = LineEdit()
        drop_input.setPlaceholderText("落点")
        drop_input.setFixedWidth(300)
        
        drop_detail_input = LineEdit()
        drop_detail_input.setPlaceholderText("落点详情")
        drop_detail_input.setFixedWidth(300)
        
        drop_layout.addWidget(drop_input)
        drop_layout.addWidget(drop_detail_input)
        
        # 落点图片上传
        drop_label = QLabel("落点图片上传")
        drop_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        drop_layout.addWidget(drop_label)
        
        # drop_image_card = ImageDisplayCard()
        # drop_layout.addWidget(drop_image_card)
        
        # 右侧：点位备注
        note_layout = QVBoxLayout()
        note_text = PlainTextEdit()
        note_text.setPlaceholderText("点位备注")
        note_text.setFixedSize(300, 280)
        note_layout.addWidget(note_text)
        
        third_row_layout.addLayout(drop_layout)
        third_row_layout.addSpacing(50)
        third_row_layout.addLayout(note_layout)
        third_row_layout.addStretch()
        
        content_layout.addLayout(third_row_layout)
        
        # 保存按钮
        save_button = PushButton("保存")
        save_button.setFixedSize(100, 40)
        save_button.clicked.connect(self.save_data)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        
        content_layout.addLayout(button_layout)
        content_layout.addStretch()
        
        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: #FAFAFA;
            }
            QLabel {
                color: #333333;
                font-size: 12px;
            }
        """)
    
    def save_data(self):
        print("保存数据...")
        # 在这里添加保存逻辑

