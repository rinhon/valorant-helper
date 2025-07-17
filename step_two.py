import json
import os
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QSizePolicy, 
    QLabel, QFrame, QGraphicsDropShadowEffect, QMessageBox, QTabWidget
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPropertyAnimation, QParallelAnimationGroup, QPointF
from PyQt5.QtGui import QFont, QResizeEvent, QPixmap, QColor
from qfluentwidgets import (
    BodyLabel, 
    PushButton, 
    FluentIcon,
    ScrollArea,MessageBox
)

class HeroLabel(QLabel):
    """自定义英雄标签类，用于显示英雄头像并处理交互"""
    clicked = pyqtSignal(object)  # 点击信号，传递自身引用
    
    def __init__(self, hero_data=None, parent=None):
        super().__init__(parent)
        self.hero_data = hero_data or {}
        self.selected = False
        self.setFixedSize(120, 150)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)
        
        # # 打印hero_data用于调试
        # print(f"创建英雄标签，数据: {self.hero_data}")
        
        # 设置样式
        self.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        
        # 添加阴影效果
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(0, 0, 0, 50))
        self.shadow.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow)
        
        # 创建垂直布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignCenter)
        
        # 创建头像标签
        self.avatar_label = QLabel(self)
        self.avatar_label.setFixedSize(100, 100)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet("""
            background-color: transparent;
            border-radius: 5px;
        """)
        
        # 创建名称标签
        self.name_label = QLabel(self.hero_data.get('Chinese_name', '未知英雄') if self.hero_data else "", self)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("""
            background-color: transparent;
            color: black;
            font-weight: bold;
            font-size: 12px;
        """)
        
        # 添加到布局
        self.layout.addWidget(self.avatar_label)
        self.layout.addWidget(self.name_label)
        
        # 加载头像
        self.load_avatar()
    
    def load_avatar(self):
        """加载并设置英雄头像"""
        if not self.hero_data:
            return
            
        avatar_path = self.hero_data.get('avatar', '')
        if avatar_path:
            pixmap = QPixmap(avatar_path)
            if not pixmap.isNull():
                # 缩放图片以适应标签大小，保持纵横比
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.avatar_label.setPixmap(pixmap)
    
    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            print(f"鼠标点击事件触发 - 英雄: {self.hero_data.get('name')}")  # 调试用
            # 调试打印：检查信号接收者数量
            print(f"信号接收者数量: {self.receivers(self.clicked)}")
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
            
            # 发送点击信号，确保传递自身引用
            print(f"发射点击信号 - 英雄: {self.hero_data.get('name')}")
            self.clicked.emit(self)
            print(f"点击信号发射完成 - 英雄: {self.hero_data.get('name')}")
    
    def set_selected(self, selected):
        """设置选中状态"""
        self.selected = selected
        if selected:
            self.setStyleSheet("""
                QLabel {
                    background-color: #f5f5f5;
                    border: 3px solid rgb(250,68,84);
                    border-radius: 8px;
                    padding: 5px;
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
                    padding: 5px;
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
                    padding: 5px;
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
                    padding: 5px;
                }
            """)


class HeroCategoryWidget(QWidget):
    """英雄分类显示组件"""
    hero_selected = pyqtSignal(dict)  # 发送选定的英雄数据
    
    def __init__(self, category_name, heroes_data, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.heroes_data = heroes_data
        self.hero_labels = []
        self.selected_hero = None
        self.selected_label = None
        
        # 创建布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)
        
        # 创建分类标题
        self.title_label = BodyLabel(self.get_category_chinese_name(), self)
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        
        # 创建网格布局用于英雄标签
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(15)
        self.grid_layout.setVerticalSpacing(15)
        
        # 创建英雄标签
        for hero_data in self.heroes_data:
            hero_label = HeroLabel(hero_data)
            hero_label.clicked.connect(self.on_hero_label_clicked)
            self.hero_labels.append(hero_label)
        
        # 初始布局
        self.update_grid_layout()
        
        # 添加到主布局
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addStretch(1)  # 添加伸展因子
    
    def get_category_chinese_name(self):
        """获取分类的中文名称"""
        category_names = {
            "Duelers": "决斗",
            "Controllers": "控场",
            "Sentinels": "先锋",
            "Guardians": "哨位"
        }
        return category_names.get(self.category_name, self.category_name)
    
    def on_hero_label_clicked(self, label):
        """处理英雄标签点击事件"""
        print("英雄标签点击处理方法被调用")  # 调试用
        hero_data = label.hero_data
        if hero_data:
            print(f"点击了英雄: {hero_data.get('Chinese_name')} ({hero_data.get('name')})")
            print(f"英雄数据详情: {hero_data}")  # 调试用
            
            # 取消之前选择的标签高亮
            if self.selected_label:
                self.selected_label.set_selected(False)
            
            # 高亮当前选择的标签
            label.set_selected(True)
            
            # 更新选择的英雄和标签
            self.selected_hero = hero_data
            self.selected_label = label
            
            # 发送选择的英雄信号
            self.hero_selected.emit(hero_data)
    
    def update_grid_layout(self):
        """更新网格布局"""
        # 清除现有布局中的所有标签
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                self.grid_layout.removeWidget(item.widget())
        
        # 计算最佳列数
        width = self.width()
        # 根据窗口宽度动态计算列数，考虑标签固定宽度(120)和水平间距(15)
        label_width_with_spacing = 120 + 15  # 标签宽度加上水平间距
        
        # 计算可以容纳的最大列数，考虑左右边距
        available_width = width - 20  # 减去左右边距
        max_cols = max(1, int(available_width / label_width_with_spacing))
        
        # 限制最大列数为6，确保布局美观
        cols = min(max_cols, 6)
        
        # 设置网格布局的对齐方式为居中
        self.grid_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        # 重新布局标签
        for i, label in enumerate(self.hero_labels):
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(label, row, col)
    
    def resizeEvent(self, event: QResizeEvent):
        """处理窗口大小变化事件"""
        super().resizeEvent(event)
        # 当窗口大小变化时，更新网格布局
        self.update_grid_layout()
    
    def clear_selection(self):
        """清除选择状态"""
        if self.selected_label:
            self.selected_label.set_selected(False)
        self.selected_hero = None
        self.selected_label = None


class StepTwo(QWidget):
    # 信号定义
    hero_selected = pyqtSignal(dict)  # 发送选定的英雄数据
    prev_step_requested = pyqtSignal()
    next_step_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 存储英雄数据和选择状态
        self.heroes_data = {}
        self.selected_hero = None
        self.selected_map = None  # 初始化地图数据
        self.category_widgets = {}
        self.chose_side = None  # 进攻/防守选择状态
        
        # 连接地图选择信号
        if parent and hasattr(parent, 'step_one'):
            parent.step_one.map_selected.connect(self.set_map_data)
        
        # 创建布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # # 进攻/防守选择组件
        # self.side_selection_widget = QWidget()
        # side_layout = QHBoxLayout(self.side_selection_widget)
        # side_layout.setContentsMargins(0, 0, 0, 0)
        
        # # 进攻按钮
        # self.attack_btn = PushButton("进攻")
        # self.attack_btn.setCheckable(True)
        # self.attack_btn.clicked.connect(lambda: self.on_side_selected("attack"))
        
        # # 防守按钮
        # self.defense_btn = PushButton("防守") 
        # self.defense_btn.setCheckable(True)
        # self.defense_btn.clicked.connect(lambda: self.on_side_selected("defense"))
        
        # # 添加到布局
        # side_layout.addStretch(1)
        # side_layout.addWidget(self.attack_btn)
        # side_layout.addWidget(self.defense_btn)
        # side_layout.addStretch(1)
        
        # # 将组件添加到主布局
        # self.main_layout.addWidget(self.side_selection_widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #f8f8f8;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #333;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #f8f8f8;
                border-bottom: 2px solid rgb(250,68,84);
            }
            QTabBar::tab:hover:!selected {
                background-color: #e8e8e8;
            }
        """)
        
        # 添加组件到主布局
        # self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.tab_widget, 1)
        
        # 创建底部导航区域
        self.create_bottom_nav()
        
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
        
        # 添加上一步按钮
        self.prev_button = PushButton("返回")
        self.prev_button.setIcon(FluentIcon.LEFT_ARROW)
        self.prev_button.clicked.connect(self.on_prev_step)
        
        # 添加伸展因子
        nav_layout.addStretch(1)
        
        # 添加下一步按钮
        self.next_button = PushButton("下一步")
        self.next_button.setIcon(FluentIcon.CHEVRON_RIGHT)
        self.next_button.setProperty("iconPosition", "right")
        self.next_button.clicked.connect(self.on_next_step)
        self.next_button.setEnabled(False)  # 初始禁用
        
        # 将按钮添加到布局
        nav_layout.addWidget(self.prev_button)
        nav_layout.addStretch(1)
        nav_layout.addWidget(self.next_button)
        
        # 将底部导航添加到主布局
        self.main_layout.addWidget(bottom_nav)
        
        # 加载英雄数据
        self.load_heroes_data()
        
        # 创建英雄分类标签页
        self.create_hero_tabs()
    
    def load_heroes_data(self):
        """加载英雄数据"""
        try:
            with open('heroes/hero.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.heroes_data = data.get('heroes', {})
                # # 调试打印：显示加载的英雄数量和分类
                # hero_count = sum(len(heroes) for heroes in self.heroes_data.values())
                # print(f"成功加载英雄数据，共{hero_count}个英雄，分类: {list(self.heroes_data.keys())}")
        except Exception as e:
            print(f"加载英雄数据失败: {e}")
    
    def create_hero_tabs(self):
        """创建英雄分类标签页"""
        # 清除现有标签页
        self.tab_widget.clear()
        self.category_widgets = {}
        
        # 创建"全部"标签页
        all_heroes = []
        for category, heroes in self.heroes_data.items():
            all_heroes.extend(heroes)
        
        all_tab = QWidget()
        all_scroll = ScrollArea(all_tab)
        all_scroll.setWidgetResizable(True)
        all_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        all_content = QWidget()
        all_layout = QVBoxLayout(all_content)
        all_layout.setContentsMargins(10, 10, 10, 10)
        all_layout.setSpacing(15)
        
        all_grid = QGridLayout()
        all_grid.setHorizontalSpacing(15)
        all_grid.setVerticalSpacing(15)
        
        all_hero_labels = []
        for hero_data in all_heroes:
            # 打印英雄数据用于调试
            # print(f"创建英雄标签: {hero_data.get('name')} - {hero_data.get('Chinese_name')}")
            
            hero_label = HeroLabel(hero_data)
            # 调试打印：显示创建的英雄标签和信号连接状态
            # print(f"创建HeroLabel - 英雄: {hero_data.get('name')} - {hero_data.get('Chinese_name')}")
            # print(f"信号连接前状态: {'已连接' if hero_label.receivers(hero_label.clicked) > 0 else '未连接'}")
            
            # 修改信号连接方式，与其他类别一致
            hero_label.clicked.connect(lambda checked, label=hero_label: self.on_hero_selected(label.hero_data, label))
            all_hero_labels.append(hero_label)
            
            # 调试打印：显示信号连接后状态
            # print(f"信号连接后状态: {'已连接' if hero_label.receivers(hero_label.clicked) > 0 else '未连接'}")
        
         #  每行显示6个英雄
        cols = 6
        for i, label in enumerate(all_hero_labels):
            row = i // cols
            col = i % cols
            all_grid.addWidget(label, row, col)
        
        all_layout.addLayout(all_grid)
        all_layout.addStretch(1)
        
        all_scroll.setWidget(all_content)
        
        all_tab_layout = QVBoxLayout(all_tab)
        all_tab_layout.setContentsMargins(0, 0, 0, 0)
        all_tab_layout.addWidget(all_scroll)
        
        self.tab_widget.addTab(all_tab, "全部")
        
        # 为每个英雄分类创建标签页
        for category, heroes in self.heroes_data.items():
            tab = QWidget()
            scroll = ScrollArea(tab)
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            category_widget = HeroCategoryWidget(category, heroes)
            category_widget.hero_selected.connect(self.on_hero_selected_from_category)
            
            scroll.setWidget(category_widget)
            
            tab_layout = QVBoxLayout(tab)
            tab_layout.setContentsMargins(0, 0, 0, 0)
            tab_layout.addWidget(scroll)
            
            # 获取分类的中文名称
            category_chinese_name = self.get_category_chinese_name(category)
            
            self.tab_widget.addTab(tab, category_chinese_name)
            self.category_widgets[category] = category_widget
    
    def get_category_chinese_name(self, category):
        """获取分类的中文名称"""
        category_names = {
            "Duelers": "决斗",
            "Controllers": "电子烟",
            "Sentinels": "打闪的",
            "Guardians": "保安还阴啊"
        }
        return category_names.get(category, category)
    
    def on_hero_selected_from_category(self, hero_data):
        """处理从分类组件中选择英雄的事件"""
        # 清除其他分类中的选择
        for category, widget in self.category_widgets.items():
            if widget.selected_hero != hero_data:
                widget.clear_selection()
        
        # 更新当前选择的英雄
        self.selected_hero = hero_data
        
        # 启用下一步按钮
        self.next_button.setEnabled(True)
    
    def on_hero_selected(self, hero_data, label):
        """处理从全部标签页中选择英雄的事件"""
        
        # 清除所有分类中的选择
        for category, widget in self.category_widgets.items():
            widget.clear_selection()
        
        # 更新当前选择的英雄
        self.selected_hero = hero_data
        print(f"当前选择的英雄: {self.selected_hero.get('name')}")
        
        # 高亮当前选择的标签
        label.set_selected(True)
        
        label.set_selected(True)
        
        # 启用下一步按钮
        self.next_button.setEnabled(True)
    
    def on_prev_step(self):
        """处理上一步按钮点击"""
        self.prev_step_requested.emit()
    
    def on_side_selected(self, side):
        """处理进攻/防守选择"""
        self.chose_side = side
        if side == "attack":
            self.attack_btn.setChecked(True)
            self.defense_btn.setChecked(False)
        else:
            self.attack_btn.setChecked(False)
            self.defense_btn.setChecked(True)
    
    def on_next_step(self):
        """处理下一步按钮点击"""
        if not self.selected_hero:
            self.message_box = MessageBox("又不选？","你又又又又又不选？",self)
            self.message_box.yesButton.hide()
            self.message_box.buttonLayout.insertStretch(0, 1)
            return
            
  
        # 准备传递的数据
        data = {
            'map': self.selected_map,
            'hero': self.selected_hero,
        }
        
        # 获取step three页面并传递数据
        step_three = self.parent().widget(2)
        step_three.receive_data(data)
        
        # 发送信号并跳转页面
        self.hero_selected.emit(self.selected_hero)
        self.next_step_requested.emit()
    
    def set_map_data(self, map_data):
        """设置地图数据"""
        self.selected_map = map_data
   
    
    def show_content(self):
        """显示内容"""
        # 显示英雄
        # 选择界面
        self.show()