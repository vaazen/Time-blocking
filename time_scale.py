# time_scale.py - Улучшенная шкала времени
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QLinearGradient
from datetime import datetime, timedelta

class PremiumTimeScale(QWidget):
    """Премиум шкала времени с улучшенной визуализацией"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_hour = 8
        self.end_hour = 22
        self.pixels_per_minute = 2
        self.current_time_line = None
        self.highlighted_hours = set()
        
        self.setFixedWidth(120)
        self.setMinimumHeight(600)
        
        # Таймер для обновления текущего времени
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(60000)  # Обновление каждую минуту
        
    def paintEvent(self, event):
        """Отрисовка шкалы времени"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Градиентный фон
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(30, 30, 30))
        gradient.setColorAt(1, QColor(50, 50, 50))
        painter.fillRect(self.rect(), gradient)
        
        # Рисуем временные метки
        self.draw_time_marks(painter)
        
        # Рисуем текущее время
        self.draw_current_time(painter)
        
        # Рисуем выделенные часы
        self.draw_highlighted_hours(painter)
    
    def draw_time_marks(self, painter):
        """Отрисовка временных меток"""
        for hour in range(self.start_hour, self.end_hour + 1):
            for minute in [0, 30]:
                if hour == self.end_hour and minute == 30:
                    continue
                    
                minutes_from_start = (hour - self.start_hour) * 60 + minute
                y_pos = minutes_from_start * self.pixels_per_minute
                
                if minute == 0:
                    # Часовая метка
                    painter.setPen(QPen(QColor(255, 255, 255), 2))
                    painter.drawLine(40, y_pos, self.width(), y_pos)
                    
                    # Текст часа
                    painter.setPen(QPen(QColor(255, 255, 255)))
                    painter.setFont(QFont("Arial", 10, QFont.Bold))
                    hour_text = f"{hour:02d}:00"
                    painter.drawText(10, y_pos - 10, 60, 20, Qt.AlignLeft, hour_text)
                else:
                    # Получасовая метка
                    painter.setPen(QPen(QColor(200, 200, 200, 150), 1))
                    painter.drawLine(60, y_pos, self.width(), y_pos)
                    
                    # Текст получаса
                    painter.setPen(QPen(QColor(200, 200, 200)))
                    painter.setFont(QFont("Arial", 8))
                    minute_text = f"{hour:02d}:30"
                    painter.drawText(10, y_pos - 10, 60, 20, Qt.AlignLeft, minute_text)
    
    def draw_current_time(self, painter):
        """Отрисовка текущего времени"""
        current_time = datetime.now()
        if self.start_hour <= current_time.hour < self.end_hour:
            minutes_from_start = (current_time.hour - self.start_hour) * 60 + current_time.minute
            y_pos = minutes_from_start * self.pixels_per_minute
            
            # Линия текущего времени
            painter.setPen(QPen(QColor(255, 43, 67), 3))
            painter.drawLine(0, y_pos, self.width(), y_pos)
            
            # Треугольник-индикатор
            painter.setBrush(QColor(255, 43, 67))
            painter.drawPolygon([
                QPoint(0, y_pos - 6), 
                QPoint(0, y_pos + 6), 
                QPoint(12, y_pos)
            ])
            
            # Текст текущего времени
            painter.setPen(QPen(QColor(255, 43, 67)))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            time_text = current_time.strftime("%H:%M")
            painter.drawText(15, y_pos - 15, 50, 20, Qt.AlignLeft, time_text)
    
    def draw_highlighted_hours(self, painter):
        """Отрисовка выделенных часов"""
        for hour in self.highlighted_hours:
            if self.start_hour <= hour < self.end_hour:
                start_y = (hour - self.start_hour) * 60 * self.pixels_per_minute
                end_y = start_y + 60 * self.pixels_per_minute
                
                # Полупрозрачное выделение
                painter.fillRect(0, start_y, self.width(), end_y - start_y, 
                               QColor(255, 43, 67, 30))
    
    def highlight_hour(self, hour):
        """Выделение определенного часа"""
        self.highlighted_hours.add(hour)
        self.update()
    
    def clear_highlights(self):
        """Очистка выделений"""
        self.highlighted_hours.clear()
        self.update()
    
    def minimumHeight(self):
        """Минимальная высота на основе диапазона времени"""
        total_minutes = (self.end_hour - self.start_hour) * 60
        return total_minutes * self.pixels_per_minute