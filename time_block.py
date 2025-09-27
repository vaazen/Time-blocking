# time_block.py - Улучшенный временной блок с анимациями
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QMenu, QAction, QGraphicsDropShadowEffect, QDialog, QSlider)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QMouseEvent, QFont, QPainter, QColor, QPen, QLinearGradient
from animations import PremiumTimeBlockAnimator

class PremiumTimeBlock(QWidget):
    """Временной блок с премиум анимациями и эффектами"""
    deleted = pyqtSignal(object)
    edited = pyqtSignal(object)
    color_changed = pyqtSignal(object, str)
    time_changed = pyqtSignal(object)
    
    def __init__(self, start_time, end_time, title="", color=None, notify=True, parent=None):
        super().__init__(parent)
        self.start_time = start_time
        self.end_time = end_time
        self.title = title
        self.color = color or "#FF2B43"
        self.notify = notify
        self.is_dragging = False
        self.is_resizing = False
        self.resize_edge = None
        self.drag_start_pos = None
        self.block_id = id(self)
        
        # Настройка UI
        self.init_ui()
        self.setup_animations()
        self.apply_styles()
        
        # Контекстное меню
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # События мыши
        self.setMouseTracking(True)
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setMinimumHeight(40)
        self.setMinimumWidth(200)
        
        # Основной layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)
        self.setLayout(layout)
        
        # Заголовок и уведомления
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setWordWrap(True)
        header_layout.addWidget(self.title_label)
        
        self.notify_indicator = QLabel("🔔" if self.notify else "🔕")
        self.notify_indicator.setToolTip("Уведомления включены" if self.notify else "Уведомления выключены")
        header_layout.addWidget(self.notify_indicator)
        
        layout.addLayout(header_layout)
        
        # Время и продолжительность
        time_text = f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        duration = (self.end_time - self.start_time).total_seconds() / 60
        time_text += f" ({int(duration)} мин)"
        
        self.time_label = QLabel(time_text)
        self.time_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.time_label)
        
        # Прогресс выполнения (если задача в процессе)
        self.progress_layout = QHBoxLayout()
        self.progress_label = QLabel("Выполнено:")
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.setValue(0)
        self.progress_slider.valueChanged.connect(self.on_progress_changed)
        
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.progress_slider)
        self.progress_layout.setContentsMargins(0, 5, 0, 0)
        
        # Скрываем прогресс по умолчанию
        self.progress_label.hide()
        self.progress_slider.hide()
        
        layout.addLayout(self.progress_layout)
    
    def setup_animations(self):
        """Настройка анимаций"""
        self.animator = PremiumTimeBlockAnimator(self)
        
        # Тень при наведении
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setColor(QColor(0, 0, 0, 80))
        self.shadow_effect.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow_effect)
        
        # Анимация тени
        self.shadow_animation = QPropertyAnimation(self.shadow_effect, b"blurRadius")
        self.shadow_animation.setDuration(300)
        self.shadow_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet(f"""
            PremiumTimeBlock {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color}33, stop:0.5 {self.color}22, stop:1 {self.color}11);
                border: 2px solid {self.color};
                border-radius: 12px;
                margin: 2px;
            }}
            PremiumTimeBlock:hover {{
                border: 2px solid {self.color}CC;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color}55, stop:0.5 {self.color}44, stop:1 {self.color}33);
            }}
            QLabel {{
                color: #FFFFFF;
                font-size: 11px;
                background: transparent;
            }}
            QLabel[objectName="title_label"] {{
                font-weight: bold;
                font-size: 12px;
                color: #FFFFFF;
            }}
            QSlider::groove:horizontal {{
                background: #333333;
                height: 4px;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {self.color};
                width: 12px;
                height: 12px;
                border-radius: 6px;
                margin: -4px 0;
            }}
        """)
        
        # Специальный стиль для заголовка
        self.title_label.setStyleSheet(f"""
            background: {self.color};
            padding: 4px 8px;
            border-radius: 6px;
            color: white;
            font-weight: bold;
        """)
    
    def enterEvent(self, event):
        """Обработчик входа курсора"""
        self.animator.animate_hover_enter()
        self.shadow_animation.setStartValue(20)
        self.shadow_animation.setEndValue(40)
        self.shadow_animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Обработчик выхода курсора"""
        self.animator.animate_hover_leave()
        self.shadow_animation.setStartValue(40)
        self.shadow_animation.setEndValue(20)
        self.shadow_animation.start()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Обработчик нажатия мыши"""
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            height = self.height()
            
            # Проверяем, кликнули ли на границу для изменения размера
            if pos.y() < 10:
                self.is_resizing = True
                self.resize_edge = 'top'
            elif pos.y() > height - 10:
                self.is_resizing = True
                self.resize_edge = 'bottom'
            else:
                self.is_dragging = True
                self.drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()
            
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Обработчик движения мыши"""
        pos = event.pos()
        height = self.height()
        
        # Изменение курсора при наведении на границы
        if pos.y() < 8 or pos.y() > height - 8:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        
        if self.is_dragging and event.buttons() == Qt.LeftButton:
            new_pos = event.globalPos() - self.drag_start_pos
            self.move(new_pos)
            self.time_changed.emit(self)
            event.accept()
        elif self.is_resizing and event.buttons() == Qt.LeftButton:
            # Здесь будет логика изменения размера
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Обработчик отпускания мыши"""
        self.is_dragging = False
        self.is_resizing = False
        self.resize_edge = None
        event.accept()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Обработчик двойного клика"""
        self.edit_block()
        event.accept()
    
    def show_context_menu(self, pos):
        """Показ контекстного меню"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #2B2B2B;
                color: white;
                border: 1px solid #FF2B43;
                border-radius: 8px;
            }
            QMenu::item {
                padding: 8px 16px;
            }
            QMenu::item:selected {
                background: #FF2B43;
            }
        """)
        
        # Действия меню
        edit_action = QAction("✏️ Редактировать", self)
        edit_action.triggered.connect(self.edit_block)
        menu.addAction(edit_action)
        
        color_menu = QMenu("🎨 Изменить цвет", self)
        colors = ["#FF2B43", "#FF4C63", "#FF6B7F", "#FF8A99", 
                 "#FF4C43", "#FF6B5F", "#FF8A79", "#FFA999"]
        
        for color in colors:
            color_action = QAction("■", self)
            color_action.setStyleSheet(f"color: {color}; font-size: 16px;")
            color_action.triggered.connect(lambda checked, c=color: self.set_color(c))
            color_menu.addAction(color_action)
        
        menu.addMenu(color_menu)
        
        progress_action = QAction("📊 Отслеживать прогресс", self)
        progress_action.setCheckable(True)
        progress_action.setChecked(self.progress_slider.isVisible())
        progress_action.triggered.connect(self.toggle_progress_tracking)
        menu.addAction(progress_action)
        
        notify_action = QAction("🔔 Уведомления", self)
        notify_action.setCheckable(True)
        notify_action.setChecked(self.notify)
        notify_action.triggered.connect(self.toggle_notifications)
        menu.addAction(notify_action)
        
        menu.addSeparator()
        
        delete_action = QAction("🗑️ Удалить", self)
        delete_action.triggered.connect(lambda: self.deleted.emit(self))
        menu.addAction(delete_action)
        
        menu.exec_(self.mapToGlobal(pos))
    
    def edit_block(self):
        """Редактирование блока"""
        from .modals import BlockEditorModal
        modal = BlockEditorModal(self, self.parent().parent())
        if modal.exec_() == QDialog.Accepted:
            self.update_from_modal(modal.get_data())
    
    def update_from_modal(self, data):
        """Обновление данных из модального окна"""
        self.title = data['title']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.color = data['color']
        self.notify = data['notify']
        
        self.update_display()
        self.apply_styles()
        
        self.edited.emit(self)
    
    def update_display(self):
        """Обновление отображения"""
        time_text = f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        duration = (self.end_time - self.start_time).total_seconds() / 60
        time_text += f" ({int(duration)} мин)"
        
        self.title_label.setText(self.title)
        self.time_label.setText(time_text)
        self.notify_indicator.setText("🔔" if self.notify else "🔕")
        self.notify_indicator.setToolTip("Уведомления включены" if self.notify else "Уведомления выключены")
    
    def set_color(self, color):
        """Изменение цвета блока"""
        self.color = color
        self.apply_styles()
        self.color_changed.emit(self, color)
    
    def toggle_notifications(self):
        """Переключение уведомлений"""
        self.notify = not self.notify
        self.notify_indicator.setText("🔔" if self.notify else "🔕")
        self.notify_indicator.setToolTip("Уведомления включены" if self.notify else "Уведомления выключены")
    
    def toggle_progress_tracking(self):
        """Переключение отслеживания прогресса"""
        visible = not self.progress_label.isVisible()
        self.progress_label.setVisible(visible)
        self.progress_slider.setVisible(visible)
    
    def on_progress_changed(self, value):
        """Обработчик изменения прогресса"""
        self.progress_label.setText(f"Выполнено: {value}%")
    
    def get_duration_minutes(self):
        """Получение продолжительности в минутах"""
        return int((self.end_time - self.start_time).total_seconds() / 60)
    
    def paintEvent(self, event):
        """Отрисовка дополнительных элементов"""
        super().paintEvent(event)
        
        # Рисуем индикаторы изменения размера
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 150), 2))
        
        # Верхняя граница
        painter.drawLine(15, 6, self.width() - 15, 6)
        # Нижняя граница
        painter.drawLine(15, self.height() - 6, self.width() - 15, self.height() - 6)
        
        # Если задача в процессе, рисуем индикатор прогресса
        if self.progress_slider.isVisible() and self.progress_slider.value() > 0:
            progress = self.progress_slider.value()
            painter.setPen(QPen(QColor(0, 255, 0, 100), 3))
            painter.drawLine(0, self.height() - 2, 
                           self.width() * progress / 100, self.height() - 2)