# modern_widgets.py - Современные кастомные виджеты
from PyQt5.QtWidgets import (QPushButton, QFrame, QLabel, QSlider, QProgressBar, 
                             QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRectF
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QFont, QPen, QPainterPath
from animations import RippleEffect, FadeAnimation

class PremiumButton(QPushButton):
    """Кнопка премиум-класса с эффектами"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.ripple = RippleEffect(self)
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        
        # Тень
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(255, 43, 67, 100))
        self.shadow.setOffset(0, 3)
        self.setGraphicsEffect(self.shadow)
    
    def mousePressEvent(self, event):
        self.ripple.create_ripple(event.pos())
        super().mousePressEvent(event)
        
        # Анимация нажатия
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(100)
        anim.setStartValue(self.geometry())
        anim.setEndValue(self.geometry().translated(0, 2))
        anim.start()

class GlassFrame(QFrame):
    """Стеклянный эффект рамки"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Очищаем область перед отрисовкой
            painter.fillRect(self.rect(), QColor(0, 0, 0, 0))  # Прозрачный фон
            
            # Создаем путь с закругленными углами
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), 15, 15)
            
            # Устанавливаем обрезку по пути
            painter.setClipPath(path)
            
            # Рисуем фон
            painter.fillPath(path, self.backgroundColor)
            
            # Рисуем границу если нужно
            if self.border_width > 0:
                pen = QPen(self.border_color, self.border_width)
                painter.setPen(pen)
                painter.drawPath(path)
                
        except Exception as e:
            print(f"Ошибка отрисовки: {e}")
class GradientLabel(QLabel):
    """Текст с градиентной заливкой"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.color1 = QColor(255, 43, 67)
        self.color2 = QColor(255, 100, 120)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Градиент для текста
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, self.color1)
        gradient.setColorAt(1, self.color2)
        
        painter.setPen(QPen(gradient, 1))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class ModernSlider(QSlider):
    """Современный слайдер"""
    valueChanged = pyqtSignal(int)
    
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #333;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF2B43, stop:1 #FF6B7F);
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -7px 0;
            }
        """)

class CircularProgressBar(QProgressBar):
    """Круглый прогресс-бар"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.value = 0
        self.width = 200
        self.height = 200
    
    def set_value(self, value):
        self.value = value
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Фон
        painter.setPen(QPen(QColor(50, 50, 50), 10))
        painter.drawArc(10, 10, self.width-20, self.height-20, 0, 360*16)
        
        # Прогресс
        angle = self.value * 360 / 100
        painter.setPen(QPen(QColor(255, 43, 67), 10))
        painter.drawArc(10, 10, self.width-20, self.height-20, 90*16, -angle*16)
        
        # Текст
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 20))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")

class TimeDisplay(QLabel):
    """Стильное отображение времени"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.time_string = "00:00"
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #FF2B43, stop:1 #FF6B7F);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            padding: 20px;
        """)
    
    def set_time(self, hours, minutes):
        self.time_string = f"{hours:02d}:{minutes:02d}"
        self.setText(self.time_string)

class StatisticsCard(QFrame):
    """Карточка статистики"""
    def __init__(self, title, value, unit="", parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.unit = unit
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel(self.title)
        self.value_label = QLabel(f"{self.value}")
        self.unit_label = QLabel(self.unit)
        
        self.title_label.setAlignment(Qt.AlignCenter)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.unit_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.unit_label)
        
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            StatisticsCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1A1A1A, stop:1 #2A2A2A);
                border: 1px solid #333;
                border-radius: 12px;
                padding: 20px;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLabel:nth-child(2) {
                font-size: 32px;
                font-weight: bold;
                color: #FF2B43;
            }
        """)
    
    def update_value(self, new_value):
        self.value = new_value
        self.value_label.setText(f"{new_value}")

class NavigationBar(QFrame):
    """Панель навигации"""
    tabChanged = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = ["📅 Расписание", "📊 Статистика", "⚙️ Настройки"]
        self.current_tab = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout()
        
        for i, tab in enumerate(self.tabs):
            btn = PremiumButton(tab)
            btn.setCheckable(True)
            btn.setChecked(i == 0)
            btn.clicked.connect(lambda checked, idx=i: self.switch_tab(idx))
            layout.addWidget(btn)
        
        self.setLayout(layout)
    
    def switch_tab(self, index):
        self.current_tab = index
        self.tabChanged.emit(index)
        
        # Обновляем состояние кнопок
        for i, btn in enumerate(self.findChildren(PremiumButton)):
            btn.setChecked(i == index)

class NotificationToast(QFrame):
    """Всплывающее уведомление"""
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QHBoxLayout()
        icon = QLabel("🔔")
        message_label = QLabel(self.message)
        
        layout.addWidget(icon)
        layout.addWidget(message_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            NotificationToast {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF2B43, stop:1 #FF6B7F);
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-weight: bold;
            }
        """)
        
        # Тень
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)