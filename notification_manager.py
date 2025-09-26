# notification_manager.py
from datetime import datetime, timedelta
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import winsound  # Для Windows, для других ОС нужна альтернатива

class NotificationManager:
    notification_triggered = pyqtSignal(str, str)  # title, message
    
    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_notifications)
        self.enabled = True
        self.notification_times = {}
    
    def start(self):
        """Запускает проверку уведомлений каждую минуту"""
        self.timer.start(60000)  # Каждую минуту
        self.check_notifications()
    
    def stop(self):
        """Останавливает проверку уведомлений"""
        self.timer.stop()
    
    def set_enabled(self, enabled):
        """Включает/выключает уведомления"""
        self.enabled = enabled
    
    def add_notification(self, block_id, start_time, title):
        """Добавляет блок для отслеживания уведомлений"""
        # Уведомление за 2 минуты до начала
        notify_time = start_time - timedelta(minutes=2)
        self.notification_times[block_id] = (notify_time, title)
    
    def remove_notification(self, block_id):
        """Удаляет блок из отслеживания"""
        if block_id in self.notification_times:
            del self.notification_times[block_id]
    
    def check_notifications(self):
        """Проверяет, нужно ли показать уведомление"""
        if not self.enabled:
            return
        
        current_time = datetime.now()
        blocks_to_remove = []
        
        for block_id, (notify_time, title) in self.notification_times.items():
            if current_time >= notify_time:
                # Показываем уведомление
                self.show_notification(title, notify_time)
                blocks_to_remove.append(block_id)
        
        # Удаляем обработанные уведомления
        for block_id in blocks_to_remove:
            del self.notification_times[block_id]
    
    def show_notification(self, title, notify_time):
        """Показывает уведомление"""
        try:
            # Звуковое уведомление (только для Windows)
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except:
            pass
        
        # Визуальное уведомление
        remaining_time = notify_time - datetime.now()
        minutes = max(0, int(remaining_time.total_seconds() / 60))
        
        message = f"Задача '{title}' начнется через {minutes} минут"
        
        # Используем сигнал для показа уведомления в главном окне
        self.notification_triggered.emit("Напоминание", message)
    
    def clear_all(self):
        """Очищает все уведомления"""
        self.notification_times.clear()