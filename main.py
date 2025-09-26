# main.py
import sys
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QScrollArea, QMessageBox,
                             QInputDialog, QColorDialog, QMenuBar, QAction, QFileDialog,
                             QDialog, QFormLayout, QDialogButtonBox, QCheckBox, QGroupBox,
                             QSpinBox, QComboBox, QSplitter, QSizePolicy, QFrame, QLineEdit)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QMouseEvent

from styles import STYLESHEET
from time_block import ResizableTimeBlock
from time_scale import TimeScaleWidget
from data_manager import DataManager
from notification_manager import NotificationManager

class BlockCreationDialog(QDialog):
    def __init__(self, start_time, end_time, parent=None):
        super().__init__(parent)
        self.start_time = start_time
        self.end_time = end_time
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Создание временного блока")
        self.setMinimumWidth(400)
        
        layout = QFormLayout(self)
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Введите название задачи")
        layout.addRow("Название задачи:", self.title_edit)
        
        # Время начала и окончания
        time_layout = QHBoxLayout()
        
        self.start_time_edit = QLineEdit(self.start_time.strftime("%H:%M"))
        time_layout.addWidget(QLabel("С:"))
        time_layout.addWidget(self.start_time_edit)
        
        self.end_time_edit = QLineEdit(self.end_time.strftime("%H:%M"))
        time_layout.addWidget(QLabel("До:"))
        time_layout.addWidget(self.end_time_edit)
        
        layout.addRow("Время:", time_layout)
        
        # Цвет
        self.color_combo = QComboBox()
        colors = ["#FF2B2B", "#FF4444", "#FF6B6B", "#FF8B8B", 
                 "#FF4C4C", "#FF6666", "#FF8C8C", "#FFAAAA"]
        for color in colors:
            self.color_combo.addItem("■", color)
            self.color_combo.setItemData(self.color_combo.count()-1, color, Qt.BackgroundRole)
        layout.addRow("Цвет:", self.color_combo)
        
        # Уведомления
        self.notify_check = QCheckBox("Уведомлять за 2 минуты до начала")
        self.notify_check.setChecked(True)
        layout.addRow("", self.notify_check)
        
        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def validate_and_accept(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название задачи")
            return
        
        try:
            start = datetime.strptime(self.start_time_edit.text(), "%H:%M").time()
            end = datetime.strptime(self.end_time_edit.text(), "%H:%M").time()
            
            if start >= end:
                QMessageBox.warning(self, "Ошибка", "Время окончания должно быть позже времени начала")
                return
                
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный формат времени (используйте ЧЧ:ММ)")
    
    def get_data(self):
        start = datetime.strptime(self.start_time_edit.text(), "%H:%M").time()
        end = datetime.strptime(self.end_time_edit.text(), "%H:%M").time()
        
        return {
            "title": self.title_edit.text(),
            "start_time": start,
            "end_time": end,
            "color": self.color_combo.currentData(),
            "notify": self.notify_check.isChecked()
        }

class TimeBlockingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time_blocks = []
        self.dragging_block = None
        self.drag_start_pos = None
        self.current_date = datetime.now().date()
        
        # Менеджеры
        self.data_manager = DataManager()
        self.notification_manager = NotificationManager(self)
        self.notification_manager.notification_triggered.connect(self.show_notification)
        
        self.init_ui()
        self.setup_menubar()
        self.setup_statusbar()
        self.start_timers()
        
        # Загрузка данных текущего дня
        self.load_current_day()
    
    def init_ui(self):
        self.setWindowTitle("Time Blocking Planner - Черно-красный стиль")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(STYLESHEET)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Панель заголовка с датой и кнопками
        self.setup_header(main_layout)
        
        # Основная область контента
        content_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # Левая панель - шкала времени
        self.time_scale = TimeScaleWidget()
        self.time_scale.setMinimumWidth(100)
        content_splitter.addWidget(self.time_scale)
        
        # Правая панель - область блоков
        self.setup_blocks_area(content_splitter)
        
        # Панель статистики
        self.setup_stats_bar(main_layout)
        
        content_splitter.setSizes([100, 1300])
    
    def setup_header(self, layout):
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Заголовок с датой
        self.date_label = QLabel()
        self.update_date_display()
        self.date_label.setObjectName("title")
        header_layout.addWidget(self.date_label)
        
        header_layout.addStretch()
        
        # Кнопки управления
        buttons = [
            ("📅 Новый день", self.new_day),
            ("💾 Сохранить", self.save_current_day),
            ("📂 Загрузить", self.load_specific_day),
            ("⚙️ Настройки", self.show_settings),
            ("📊 Статистика", self.show_stats),
            ("🔔 Уведомления", self.toggle_notifications)
        ]
        
        for text, slot in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            btn.setMaximumWidth(120)
            header_layout.addWidget(btn)
        
        layout.addWidget(header_widget)
    
    def setup_blocks_area(self, splitter):
        # Основная область для блоков
        blocks_container = QWidget()
        blocks_layout = QVBoxLayout(blocks_container)
        
        # Область прокрутки для временных блоков
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Виджет для блоков
        self.blocks_widget = QWidget()
        self.blocks_widget.setMouseTracking(True)
        self.blocks_widget.mousePressEvent = self.handle_canvas_click
        self.blocks_layout = QVBoxLayout(self.blocks_widget)
        self.blocks_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(self.blocks_widget)
        blocks_layout.addWidget(self.scroll_area)
        
        splitter.addWidget(blocks_container)
    
    def setup_stats_bar(self, layout):
        stats_widget = QFrame()
        stats_widget.setFrameStyle(QFrame.StyledPanel)
        stats_layout = QHBoxLayout(stats_widget)
        
        self.stats_label = QLabel("Загрузка...")
        stats_layout.addWidget(self.stats_label)
        
        stats_layout.addStretch()
        
        self.productivity_label = QLabel("Продуктивность: --%")
        stats_layout.addWidget(self.productivity_label)
        
        layout.addWidget(stats_widget)
    
    def setup_menubar(self):
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("📁 Файл")
        file_menu.addAction("📅 Новый день", self.new_day, "Ctrl+N")
        file_menu.addAction("💾 Сохранить", self.save_current_day, "Ctrl+S")
        file_menu.addAction("📂 Загрузить день...", self.load_specific_day)
        file_menu.addSeparator()
        file_menu.addAction("📤 Экспорт в JSON...", self.export_data)
        file_menu.addAction("📥 Импорт из JSON...", self.import_data)
        file_menu.addSeparator()
        file_menu.addAction("🚪 Выход", self.close, "Ctrl+Q")
        
        # Меню Правка
        edit_menu = menubar.addMenu("✏️ Правка")
        edit_menu.addAction("➕ Создать блок", self.create_block_dialog, "Insert")
        edit_menu.addAction("🗑️ Очистить все", self.clear_all_blocks)
        
        # Меню Вид
        view_menu = menubar.addMenu("👁️ Вид")
        view_menu.addAction("🕐 Показать текущее время", self.toggle_current_time_display)
        view_menu.addAction("📊 Статистика продуктивности", self.show_stats)
        
        # Меню Помощь
        help_menu = menubar.addMenu("❓ Помощь")
        help_menu.addAction("📖 О программе", self.show_about)
        help_menu.addAction("🎯 Советы по использованию", self.show_tips)
    
    def setup_statusbar(self):
        self.statusBar().showMessage("Готов к работе")
    
    def start_timers(self):
        # Таймер для обновления текущего времени
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_current_time_display)
        self.time_timer.start(1000)
        
        # Таймер для проверки уведомлений
        self.notification_manager.start()
        
        # Таймер для автосохранения
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(300000)  # Каждые 5 минут
    
    def handle_canvas_click(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Создание нового блока по клику
            y_pos = event.pos().y()
            start_minutes = 8 * 60 + (y_pos // 2)  # 2 пикселя = 1 минута
            duration = 60  # 1 час по умолчанию
            
            start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes=start_minutes)
            end_time = start_time + timedelta(minutes=duration)
            
            dialog = BlockCreationDialog(start_time, end_time, self)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                self.create_time_block(data)
    
    def create_time_block(self, data):
        """Создает новый временной блок"""
        start_dt = datetime.combine(self.current_date, data["start_time"])
        end_dt = datetime.combine(self.current_date, data["end_time"])
        
        block = ResizableTimeBlock(start_dt, end_dt, data["title"], data["color"], data["notify"])
        
        # Подключаем сигналы
        block.deleted.connect(self.delete_time_block)
        block.edited.connect(self.edit_time_block)
        block.color_changed.connect(self.change_block_color)
        block.time_changed.connect(self.on_block_time_changed)
        
        self.time_blocks.append(block)
        self.blocks_layout.addWidget(block)
        
        # Добавляем уведомление
        if data["notify"]:
            self.notification_manager.add_notification(block.block_id, start_dt, data["title"])
        
        self.update_stats()
        self.statusBar().showMessage(f"Создан блок: {data['title']}")
    
    def delete_time_block(self, block):
        reply = QMessageBox.question(self, "Удаление", 
                                   f"Удалить блок '{block.title}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Удаляем уведомление
            self.notification_manager.remove_notification(block.block_id)
            
            # Удаляем из интерфейса
            block.deleteLater()
            self.time_blocks.remove(block)
            
            self.update_stats()
            self.statusBar().showMessage("Блок удален")
    
    def edit_time_block(self, block):
        # Обновляем уведомление
        self.notification_manager.remove_notification(block.block_id)
        if block.notify:
            self.notification_manager.add_notification(block.block_id, block.start_time, block.title)
        
        self.update_stats()
        self.statusBar().showMessage(f"Блок обновлен: {block.title}")
    
    def change_block_color(self, block, color):
        self.statusBar().showMessage(f"Цвет блока изменен")
    
    def on_block_time_changed(self, block):
        self.update_stats()
    
    def new_day(self):
        reply = QMessageBox.question(self, "Новый день", 
                                   "Сохранить текущий день перед очисткой?",
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        
        if reply == QMessageBox.Cancel:
            return
        
        if reply == QMessageBox.Yes:
            self.save_current_day()
        
        # Очищаем все блоки
        self.clear_all_blocks()
        
        # Устанавливаем новую дату
        self.current_date = datetime.now().date()
        self.update_date_display()
        
        # Загружаем данные для нового дня, если они есть
        self.load_current_day()
        
        self.statusBar().showMessage("Начат новый день")
    
    def clear_all_blocks(self):
        reply = QMessageBox.question(self, "Очистка", 
                                   "Очистить все временные блоки?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for block in self.time_blocks[:]:
                self.notification_manager.remove_notification(block.block_id)
                block.deleteLater()
            self.time_blocks.clear()
            
            self.notification_manager.clear_all()
            self.update_stats()
            self.statusBar().showMessage("Все блоки очищены")
    
    def save_current_day(self):
        if self.data_manager.save_day(self.time_blocks, self.current_date):
            self.statusBar().showMessage("День сохранен успешно")
        else:
            self.statusBar().showMessage("Ошибка при сохранении дня")
    
    def load_current_day(self):
        blocks_data = self.data_manager.load_day(self.current_date)
        
        for block_data in blocks_data:
            try:
                start_time = datetime.fromisoformat(block_data["start_time"])
                end_time = datetime.fromisoformat(block_data["end_time"])
                
                block = ResizableTimeBlock(
                    start_time, end_time,
                    block_data["title"],
                    block_data.get("color", "#FF2B2B"),
                    block_data.get("notify", True)
                )
                
                block.deleted.connect(self.delete_time_block)
                block.edited.connect(self.edit_time_block)
                block.color_changed.connect(self.change_block_color)
                block.time_changed.connect(self.on_block_time_changed)
                
                self.time_blocks.append(block)
                self.blocks_layout.addWidget(block)
                
                if block.notify:
                    self.notification_manager.add_notification(block.block_id, start_time, block.title)
                    
            except Exception as e:
                print(f"Ошибка загрузки блока: {e}")
        
        self.update_stats()
        self.statusBar().showMessage(f"Загружено {len(blocks_data)} блоков")
    
    def load_specific_day(self):
        dates = self.data_manager.get_saved_dates()
        if not dates:
            QMessageBox.information(self, "Загрузка", "Нет сохраненных дней")
            return
        
        date_str, ok = QInputDialog.getItem(
            self, "Выбор дня", "Выберите день для загрузки:",
            [date.strftime("%Y-%m-%d (%A)") for date in dates],
            0, False
        )
        
        if ok and date_str:
            # Очищаем текущие блоки
            self.clear_all_blocks()
            
            # Загружаем выбранный день
            selected_date = dates[[date.strftime("%Y-%m-%d (%A)") for date in dates].index(date_str)]
            self.current_date = selected_date
            self.update_date_display()
            self.load_current_day()
    
    def export_data(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт данных", 
            f"timeblocking_export_{self.current_date.strftime('%Y-%m-%d')}.json",
            "JSON Files (*.json)"
        )
        
        if filename:
            if self.data_manager.export_to_json(self.time_blocks, filename):
                QMessageBox.information(self, "Экспорт", "Данные успешно экспортированы")
            else:
                QMessageBox.warning(self, "Экспорт", "Ошибка при экспорте данных")
    
    def import_data(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Импорт данных", "", "JSON Files (*.json)"
        )
        
        if filename:
            blocks_data = self.data_manager.import_from_json(filename)
            if blocks_data:
                # Очищаем текущие блоки
                self.clear_all_blocks()
                
                # Загружаем импортированные данные
                for block_data in blocks_data:
                    self.create_time_block(block_data)
                
                QMessageBox.information(self, "Импорт", "Данные успешно импортированы")
    
    def show_settings(self):
        QMessageBox.information(self, "Настройки", "Раздел настроек будет реализован в будущих версиях")
    
    def toggle_notifications(self):
        enabled = not self.notification_manager.enabled
        self.notification_manager.set_enabled(enabled)
        
        status = "включены" if enabled else "выключены"
        self.statusBar().showMessage(f"Уведомления {status}")
    
    def show_stats(self):
        total_blocks = len(self.time_blocks)
        total_minutes = sum(block.get_duration_minutes() for block in self.time_blocks)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        productivity = min(100, int((total_minutes / 480) * 100))
        
        stats_text = f"""
        <h3>Статистика за {self.current_date.strftime('%d.%m.%Y')}</h3>
        <b>Количество блоков:</b> {total_blocks}<br>
        <b>Общее время:</b> {hours}ч {minutes}м<br>
        <b>Продуктивность:</b> {productivity}%<br>
        <b>Запланировано времени:</b> {hours:02d}:{minutes:02d}
        """
        
        QMessageBox.information(self, "Статистика", stats_text)
    
    def update_stats(self):
        total_blocks = len(self.time_blocks)
        total_minutes = sum(block.get_duration_minutes() for block in self.time_blocks)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        productivity = min(100, int((total_minutes / 480) * 100))
        
        self.stats_label.setText(
            f"Блоков: {total_blocks} | "
            f"Время: {hours:02d}:{minutes:02d} | "
            f"Продуктивность: {productivity}%"
        )
    
    def update_date_display(self):
        today = datetime.now().date()
        date_str = self.current_date.strftime("%d %B %Y (%A)")
        
        if self.current_date == today:
            date_str += " - СЕГОДНЯ"
        elif self.current_date > today:
            date_str += " - БУДУЩЕЕ"
        else:
            date_str += " - ПРОШЛОЕ"
        
        self.date_label.setText(f"📅 {date_str}")
    
    def update_current_time_display(self):
        self.time_scale.update()
        self.update()
    
    def toggle_current_time_display(self):
        pass
    
    def show_notification(self, title, message):
        QMessageBox.information(self, title, message)
        self.statusBar().showMessage(f"Уведомление: {message}")
    
    def show_about(self):
        about_text = """
        <h3>Time Blocking Planner</h3>
        <p><b>Версия:</b> 1.0</p>
        <p><b>Описание:</b> Планировщик времени с методикой тайм-блокировки</p>
        <p><b>Разработчик:</b> Ваша команда</p>
        <p><b>Лицензия:</b> MIT</p>
        <p>Использует PyQt5 для создания интерфейса</p>
        """
        QMessageBox.about(self, "О программе", about_text)
    
    def show_tips(self):
        tips = """
        <h3>Советы по использованию:</h3>
        <ul>
        <li><b>Создание блока:</b> Кликните на шкале времени для создания нового блока</li>
        <li><b>Перетаскивание:</b> Перетаскивайте блоки для изменения времени</li>
        <li><b>Изменение размера:</b> Тяните за верхнюю/нижнюю границу блока</li>
        <li><b>Редактирование:</b> Двойной клик по блоку для редактирования</li>
        <li><b>Контекстное меню:</b> Правый клик для дополнительных опций</li>
        <li><b>Автосохранение:</b> Данные сохраняются автоматически каждые 5 минут</li>
        </ul>
        """
        QMessageBox.information(self, "Советы по использованию", tips)
    
    def autosave(self):
        if self.time_blocks:
            self.data_manager.save_day(self.time_blocks, self.current_date)
            self.statusBar().showMessage("Автосохранение выполнено")
    
    def create_block_dialog(self):
        # Диалог для ручного создания блока
        current_time = datetime.now().time()
        start_time = current_time.replace(minute=(current_time.minute // 30) * 30)
        end_time = (datetime.now() + timedelta(hours=1)).time()
        
        start_dt = datetime.combine(self.current_date, start_time)
        end_dt = datetime.combine(self.current_date, end_time)
        
        dialog = BlockCreationDialog(start_dt, end_dt, self)
        if dialog.exec_() == QDialog.Accepted:
            self.create_time_block(dialog.get_data())
    
    def closeEvent(self, event):
        # Автосохранение при закрытии
        if self.time_blocks:
            self.data_manager.save_day(self.time_blocks, self.current_date)
        
        self.notification_manager.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = TimeBlockingApp()
    window.show()
    
    sys.exit(app.exec_())