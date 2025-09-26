# time_scale.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt, pyqtSignal, QPoint  # Добавляем QPoint

class TimeScaleWidget(QWidget):
    time_clicked = pyqtSignal(int)  # Минуты от начала дня
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(100)
        self.start_hour = 8
        self.end_hour = 22
        self.pixels_per_minute = 2  # 2 пикселя на минуту
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Фон
        painter.fillRect(self.rect(), QColor(43, 43, 43))
        
        # Рисуем временную шкалу
        painter.setPen(QPen(QColor(255, 255, 255, 128), 1))
        
        total_minutes = (self.end_hour - self.start_hour) * 60
        height = total_minutes * self.pixels_per_minute
        
        for hour in range(self.start_hour, self.end_hour + 1):
            for minute in [0, 30]:
                if hour == self.end_hour and minute == 30:
                    continue
                    
                minutes_from_start = (hour - self.start_hour) * 60 + minute
                y_pos = minutes_from_start * self.pixels_per_minute
                
                # Часовая метка (толще)
                if minute == 0:
                    painter.setPen(QPen(QColor(255, 255, 255), 2))
                    painter.drawLine(30, y_pos, self.width(), y_pos)
                    
                    # Подпись часа
                    painter.setPen(QPen(QColor(255, 255, 255)))
                    painter.setFont(QFont("Arial", 10, QFont.Bold))
                    hour_text = f"{hour:02d}:00"
                    painter.drawText(5, y_pos - 5, 50, 20, Qt.AlignLeft, hour_text)
                else:
                    # Получасовая метка
                    painter.setPen(QPen(QColor(255, 255, 255, 128), 1))
                    painter.drawLine(40, y_pos, self.width(), y_pos)
                    
                    # Подпись получаса
                    painter.setPen(QPen(QColor(200, 200, 200)))
                    painter.setFont(QFont("Arial", 8))
                    minute_text = f"{hour:02d}:30"
                    painter.drawText(5, y_pos - 5, 50, 20, Qt.AlignLeft, minute_text)
        
        # Текущее время
        current_time = datetime.now()
        if self.start_hour <= current_time.hour < self.end_hour:
            minutes_from_start = (current_time.hour - self.start_hour) * 60 + current_time.minute
            y_pos = minutes_from_start * self.pixels_per_minute
            
            painter.setPen(QPen(QColor(255, 43, 43), 3))
            painter.drawLine(0, y_pos, self.width(), y_pos)
            
            # Треугольник-индикатор
            painter.setBrush(QColor(255, 43, 43))
            painter.drawPolygon([QPoint(0, y_pos - 5), QPoint(0, y_pos + 5), QPoint(10, y_pos)])

    def minimumHeight(self):
        total_minutes = (self.end_hour - self.start_hour) * 60
        return total_minutes * self.pixels_per_minute