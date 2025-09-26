# time_block.py
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QMenu, QAction, QInputDialog, QLineEdit, 
                             QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QMouseEvent, QFont, QPainter, QColor, QPen
from PyQt5.QtCore import QPropertyAnimation, QRect

class ResizableTimeBlock(QWidget):
    deleted = pyqtSignal(object)
    edited = pyqtSignal(object)
    color_changed = pyqtSignal(object, str)
    time_changed = pyqtSignal(object)
    resized = pyqtSignal(object)
    
    def __init__(self, start_time, end_time, title="", color=None, notify=True, parent=None):
        super().__init__(parent)
        self.start_time = start_time
        self.end_time = end_time
        self.title = title
        self.color = color or "#FF2B2B"
        self.notify = notify
        self.is_dragging = False
        self.is_resizing = False
        self.resize_edge = None  # 'top', 'bottom'
        self.drag_start_pos = None
        self.block_id = id(self)
        
        self.init_ui()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.setMouseTracking(True)
        
        # Анимация при наведении
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def init_ui(self):
        self.setMinimumHeight(30)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)
        self.setLayout(layout)
        
        # Заголовок
        title_layout = QHBoxLayout()
        
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setStyleSheet(f"""
            color: white; 
            font-weight: bold; 
            font-size: 11px;
            background-color: {self.color};
            padding: 4px 8px;
            border-radius: 3px;
        """)
        title_layout.addWidget(self.title_label)
        
        # Индикатор уведомления
        self.notify_indicator = QLabel("🔔" if self.notify else "🔕")
        self.notify_indicator.setToolTip("Уведомления включены" if self.notify else "Уведомления выключены")
        title_layout.addWidget(self.notify_indicator)
        
        layout.addLayout(title_layout)
        
        # Время
        time_text = f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        duration = (self.end_time - self.start_time).total_seconds() / 60
        time_text += f" ({int(duration)} мин)"
        
        self.time_label = QLabel(time_text)
        self.time_label.setAlignment(Qt.AlignLeft)
        self.time_label.setStyleSheet("color: #CCCCCC; font-size: 9px;")
        layout.addWidget(self.time_label)
        
        self.update_style()
    
    def update_style(self):
        self.setStyleSheet(f"""
            ResizableTimeBlock {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color}33, stop:0.5 {self.color}22, stop:1 {self.color}11);
                border: 2px solid {self.color};
                border-radius: 6px;
                margin: 1px;
            }}
            ResizableTimeBlock:hover {{
                border: 2px solid {self.color}CC;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color}55, stop:0.5 {self.color}44, stop:1 {self.color}33);
            }}
        """)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            height = self.height()
            
            # Проверяем, кликнули ли на верхнюю или нижнюю границу для изменения размера
            if pos.y() < 10:  # Верхняя граница
                self.is_resizing = True
                self.resize_edge = 'top'
            elif pos.y() > height - 10:  # Нижняя граница
                self.is_resizing = True
                self.resize_edge = 'bottom'
            else:  # Перетаскивание
                self.is_dragging = True
                self.drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()
            
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.pos()
        height = self.height()
        
        # Изменение курсора при наведении на границы
        if pos.y() < 8 or pos.y() > height - 8:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        
        if self.is_dragging and event.buttons() == Qt.LeftButton:
            # Перетаскивание блока
            new_pos = event.globalPos() - self.drag_start_pos
            self.move(new_pos)
            self.time_changed.emit(self)
            event.accept()
        elif self.is_resizing and event.buttons() == Qt.LeftButton:
            # Изменение размера - эмулируем, фактическое изменение времени будет в родительском виджете
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.is_dragging = False
        self.is_resizing = False
        self.resize_edge = None
        event.accept()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        self.edit_block()
        event.accept()
    
    def edit_block(self):
        """Редактирование блока через диалог"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QCheckBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование блока")
        dialog.setMinimumWidth(300)
        
        layout = QFormLayout(dialog)
        
        title_edit = QLineEdit(self.title)
        layout.addRow("Название задачи:", title_edit)
        
        start_time_edit = QLineEdit(self.start_time.strftime("%H:%M"))
        layout.addRow("Время начала (ЧЧ:ММ):", start_time_edit)
        
        end_time_edit = QLineEdit(self.end_time.strftime("%H:%M"))
        layout.addRow("Время окончания (ЧЧ:ММ):", end_time_edit)
        
        notify_check = QCheckBox("Уведомлять за 2 минуты до начала")
        notify_check.setChecked(self.notify)
        layout.addRow(notify_check)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            from datetime import datetime
            try:
                # Обновляем время
                new_start = datetime.strptime(start_time_edit.text(), "%H:%M").time()
                new_end = datetime.strptime(end_time_edit.text(), "%H:%M").time()
                
                # Сохраняем дату, меняем только время
                new_start_dt = self.start_time.replace(hour=new_start.hour, minute=new_start.minute)
                new_end_dt = self.end_time.replace(hour=new_end.hour, minute=new_end.minute)
                
                if new_start_dt < new_end_dt:
                    self.start_time = new_start_dt
                    self.end_time = new_end_dt
                    self.title = title_edit.text()
                    self.notify = notify_check.isChecked()
                    
                    self.update_display()
                    self.edited.emit(self)
            except ValueError:
                pass
    
    def update_display(self):
        """Обновляет отображение блока"""
        time_text = f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        duration = (self.end_time - self.start_time).total_seconds() / 60
        time_text += f" ({int(duration)} мин)"
        
        self.title_label.setText(self.title)
        self.time_label.setText(time_text)
        self.notify_indicator.setText("🔔" if self.notify else "🔕")
        self.notify_indicator.setToolTip("Уведомления включены" if self.notify else "Уведомления выключены")
        self.update_style()
    
    def show_context_menu(self, pos):
        menu = QMenu(self)
        
        # Редактировать
        edit_action = QAction("✏️ Редактировать", self)
        edit_action.triggered.connect(self.edit_block)
        menu.addAction(edit_action)
        
        menu.addSeparator()
        
        # Цвета
        color_menu = QMenu("🎨 Изменить цвет", self)
        colors = ["#FF2B2B", "#FF4444", "#FF6B6B", "#FF8B8B", 
                 "#FF4C4C", "#FF6666", "#FF8C8C", "#FFAAAA"]
        
        for color in colors:
            color_action = QAction("■", self)
            color_action.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: bold;")
            color_action.triggered.connect(lambda checked, c=color: self.set_color(c))
            color_menu.addAction(color_action)
        
        menu.addMenu(color_menu)
        
        menu.addSeparator()
        
        # Уведомления
        notify_action = QAction("🔔 Уведомления: Вкл" if not self.notify else "🔕 Уведомления: Выкл", self)
        notify_action.triggered.connect(self.toggle_notifications)
        menu.addAction(notify_action)
        
        menu.addSeparator()
        
        # Удалить
        delete_action = QAction("🗑️ Удалить", self)
        delete_action.triggered.connect(lambda: self.deleted.emit(self))
        menu.addAction(delete_action)
        
        menu.exec_(self.mapToGlobal(pos))
    
    def set_color(self, color):
        self.color = color
        self.update_style()
        self.title_label.setStyleSheet(f"""
            color: white; 
            font-weight: bold; 
            font-size: 11px;
            background-color: {color};
            padding: 4px 8px;
            border-radius: 3px;
        """)
        self.color_changed.emit(self, color)
    
    def toggle_notifications(self):
        self.notify = not self.notify
        self.notify_indicator.setText("🔔" if self.notify else "🔕")
        self.notify_indicator.setToolTip("Уведомления включены" if self.notify else "Уведомления выключены")
    
    def get_duration_minutes(self):
        return int((self.end_time - self.start_time).total_seconds() / 60)
    
    def paintEvent(self, event):
        super().paintEvent(event)
        # Рисуем индикаторы для изменения размера
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 128), 2))
        
        # Верхняя граница
        painter.drawLine(10, 4, self.width() - 10, 4)
        # Нижняя граница
        painter.drawLine(10, self.height() - 4, self.width() - 10, self.height() - 4)