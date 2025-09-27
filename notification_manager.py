# notification_manager.py - Продвинутая система уведомлений
import winsound
from datetime import datetime, timedelta
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon
from animations import NotificationAnimator

class PremiumNotificationManager(QObject):
    """Менеджер уведомлений премиум-класса"""
    notification_triggered = pyqtSignal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_notifications)
        self.enabled = True
        self.notification_times = {}
        self.snoozed_notifications = {}
        
        # Настройки уведомлений
        self.settings = {
            "sound_enabled": True,
            "popup_enabled": True,
            "snooze_duration": 5,  # минут
            "early_notification": 2  # минут до начала
        }
    
    def start(self):
        """Запуск проверки уведомлений"""
        self.timer.start(30000)  # Проверка каждые 30 секунд
        self.check_notifications()
    
    def stop(self):
        """Остановка проверки уведомлений"""
        self.timer.stop()
    
    def set_enabled(self, enabled):
        """Включение/выключение уведомлений"""
        self.enabled = enabled
        if enabled:
            self.timer.start(30000)
        else:
            self.timer.stop()
    
    def add_notification(self, block_id, start_time, title, reminder_type="start"):
        """Добавление уведомления"""
        notify_time = start_time - timedelta(minutes=self.settings["early_notification"])
        self.notification_times[block_id] = {
            "notify_time": notify_time,
            "title": title,
            "type": reminder_type,
            "sent": False
        }
    
    def remove_notification(self, block_id):
        """Удаление уведомления"""
        if block_id in self.notification_times:
            del self.notification_times[block_id]
    
    def check_notifications(self):
        """Проверка уведомлений"""
        if not self.enabled:
            return
        
        current_time = datetime.now()
        notifications_to_send = []
        
        # Проверка обычных уведомлений
        for block_id, notification in self.notification_times.items():
            if not notification["sent"] and current_time >= notification["notify_time"]:
                notifications_to_send.append((block_id, notification))
                notification["sent"] = True
        
        # Проверка отложенных уведомлений
        for block_id, notification in list(self.snoozed_notifications.items()):
            if current_time >= notification["snooze_until"]:
                notifications_to_send.append((block_id, notification))
                del self.snoozed_notifications[block_id]
        
        # Отправка уведомлений
        for block_id, notification in notifications_to_send:
            self.send_notification(notification)
    
    def send_notification(self, notification):
        """Отправка уведомления"""
        title = "Напоминание"
        message = f"Задача '{notification['title']}' начнется через {self.settings['early_notification']} минут"
        
        if notification["type"] == "end":
            message = f"Задача '{notification['title']}' скоро завершится"
        
        # Звуковое уведомление
        if self.settings["sound_enabled"]:
            self.play_notification_sound()
        
        # Всплывающее уведомление
        if self.settings["popup_enabled"]:
            self.show_popup_notification(title, message, notification)
        
        # Уведомление в системном трее
        if hasattr(self.parent, 'tray_icon'):
            self.parent.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 5000)
        
        # Сигнал для основного окна
        self.notification_triggered.emit(title, message)
    
    def play_notification_sound(self):
        """Воспроизведение звука уведомления"""
        try:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        except:
            pass  # Игнорируем ошибки воспроизведения звука
    
    def show_popup_notification(self, title, message, notification):
        """Показ всплывающего уведомления"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
        
        dialog = QDialog(self.parent)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(300, 150)
        dialog.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        
        layout = QVBoxLayout(dialog)
        
        # Сообщение
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        snooze_btn = QPushButton("Отложить (5 мин)")
        snooze_btn.clicked.connect(lambda: self.snooze_notification(notification, dialog))
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.accept)
        
        buttons_layout.addWidget(snooze_btn)
        buttons_layout.addWidget(close_btn)
        layout.addLayout(buttons_layout)
        
        # Анимация появления
        NotificationAnimator.show_notification(dialog, "", 0)
        dialog.exec_()
    
    def snooze_notification(self, notification, dialog):
        """Отложить уведомление"""
        snooze_until = datetime.now() + timedelta(minutes=self.settings["snooze_duration"])
        notification["snooze_until"] = snooze_until
        self.snoozed_notifications[id(notification)] = notification
        
        dialog.accept()
        
        # Уведомление об отложении
        if hasattr(self.parent, 'tray_icon'):
            self.parent.tray_icon.showMessage("Уведомление отложено", 
                                            f"Напоминание отложено на {self.settings['snooze_duration']} минут", 
                                            QSystemTrayIcon.Information, 2000)
    
    def clear_all(self):
        """Очистка всех уведомлений"""
        self.notification_times.clear()
        self.snoozed_notifications.clear()