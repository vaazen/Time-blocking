# settings.py - Система настроек премиум-класса
import json
import os
from datetime import datetime
from PyQt5.QtCore import QSettings, QStandardPaths
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QGroupBox, QCheckBox, QComboBox, QSpinBox, 
                             QDoubleSpinBox, QLineEdit, QPushButton, 
                             QDialogButtonBox, QLabel, QTabWidget, QWidget,
                             QListWidget, QListWidgetItem, QScrollArea, QSlider, QMessageBox, QFileDialog)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal

class AppSettings:
    """Класс для управления настройками приложения"""
    
    def __init__(self, app_name="TimeBlockingPlanner"):
        self.app_name = app_name
        self.settings = QSettings("PremiumSoft", app_name)
        self.default_settings = self.get_default_settings()
        
    def get_default_settings(self):
        """Возвращает настройки по умолчанию"""
        return {
            "appearance": {
                "theme": "dark",
                "language": "ru",
                "font_size": 12,
                "font_family": "Segoe UI",
                "animations_enabled": True,
                "smooth_scrolling": True,
                "opacity": 1.0
            },
            "notifications": {
                "enabled": True,
                "sound_enabled": True,
                "popup_enabled": True,
                "early_minutes": 2,
                "snooze_minutes": 5,
                "working_hours_start": "08:00",
                "working_hours_end": "22:00"
            },
            "behavior": {
                "auto_save": True,
                "auto_save_interval": 5,
                "minimize_to_tray": True,
                "start_minimized": False,
                "confirm_deletions": True,
                "backup_on_start": True
            },
            "time_blocks": {
                "default_duration": 60,
                "default_color": "#FF2B43",
                "show_duration": True,
                "allow_overlap": False,
                "snap_to_grid": True,
                "grid_size": 15
            },
            "integration": {
                "calendar_sync": False,
                "export_format": "json",
                "auto_export": False,
                "cloud_sync": False
            },
            "privacy": {
                "analytics": False,
                "crash_reports": True,
                "auto_update": True
            }
        }
    
    def get(self, key, default=None):
        """Получить значение настройки"""
        keys = key.split('/')
        current = self.default_settings
        
        # Находим значение по умолчанию
        for k in keys:
            if k in current:
                current = current[k]
            else:
                return default
        
        # Пытаемся получить сохраненное значение
        value = self.settings.value(key, current)
        
        # Преобразуем типы данных
        if isinstance(current, bool):
            return value.lower() == 'true' if isinstance(value, str) else bool(value)
        elif isinstance(current, int):
            return int(value) if value is not None else current
        elif isinstance(current, float):
            return float(value) if value is not None else current
        else:
            return value if value is not None else current
    
    def set(self, key, value):
        """Установить значение настройки"""
        self.settings.setValue(key, value)
        self.settings.sync()
    
    def reset_to_defaults(self):
        """Сбросить все настройки к значениям по умолчанию"""
        self.settings.clear()
        self.settings.sync()
    
    def export_settings(self, filename):
        """Экспортировать настройки в файл"""
        try:
            all_settings = {}
            for key in self.settings.allKeys():
                all_settings[key] = self.settings.value(key)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_settings, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Ошибка экспорта настроек: {e}")
            return False
    
    def import_settings(self, filename):
        """Импортировать настройки из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            for key, value in imported_settings.items():
                self.settings.setValue(key, value)
            
            self.settings.sync()
            return True
        except Exception as e:
            print(f"Ошибка импорта настроек: {e}")
            return False
    
    def get_all_settings(self):
        """Получить все текущие настройки"""
        settings = {}
        for key in self.settings.allKeys():
            settings[key] = self.settings.value(key)
        return settings

class SettingsDialog(QDialog):
    """Диалоговое окно настроек"""
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None, settings_manager=None):
        super().__init__(parent)
        self.settings_manager = settings_manager or AppSettings()
        self.setWindowTitle("⚙️ Настройки - Time Blocking Planner")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.load_settings()
        
        # Применяем стили
        self.apply_styles()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        layout = QVBoxLayout(self)
        
        # Вкладки
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Создаем вкладки
        self.create_appearance_tab()
        self.create_notifications_tab()
        self.create_behavior_tab()
        self.create_blocks_tab()
        self.create_integration_tab()
        self.create_privacy_tab()
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton("🔄 Сбросить")
        self.reset_btn.clicked.connect(self.reset_settings)
        
        self.export_btn = QPushButton("📤 Экспорт")
        self.export_btn.clicked.connect(self.export_settings)
        
        self.import_btn = QPushButton("📥 Импорт")
        self.import_btn.clicked.connect(self.import_settings)
        
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.import_btn)
        
        # Стандартные кнопки диалога
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply_settings)
        
        layout.addLayout(button_layout)
        layout.addWidget(self.button_box)
    
    def create_appearance_tab(self):
        """Вкладка внешнего вида"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Группа темы
        theme_group = QGroupBox("🎨 Тема и оформление")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Темная", "Светлая", "Автоматически"])
        theme_layout.addRow("Цветовая тема:", self.theme_combo)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский", "English", "Deutsch"])
        theme_layout.addRow("Язык:", self.language_combo)
        
        self.animations_check = QCheckBox("Включить анимации")
        theme_layout.addRow(self.animations_check)
        
        self.smooth_scroll_check = QCheckBox("Плавная прокрутка")
        theme_layout.addRow(self.smooth_scroll_check)
        
        # Настройки шрифта
        font_group = QGroupBox("🔤 Шрифт и текст")
        font_layout = QFormLayout(font_group)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setSuffix(" px")
        font_layout.addRow("Размер шрифта:", self.font_size_spin)
        
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(["Segoe UI", "Arial", "Helvetica", "Inter", "Roboto"])
        font_layout.addRow("Шрифт:", self.font_family_combo)
        
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(50, 100)
        self.opacity_slider.setTickPosition(QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        font_layout.addRow("Непрозрачность:", self.opacity_slider)
        
        self.opacity_label = QLabel("100%")
        self.opacity_slider.valueChanged.connect(
            lambda v: self.opacity_label.setText(f"{v}%")
        )
        font_layout.addRow("", self.opacity_label)
        
        layout.addWidget(theme_group)
        layout.addWidget(font_group)
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "🎨 Внешний вид")
    
    def create_notifications_tab(self):
        """Вкладка уведомлений"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Основные настройки уведомлений
        notify_group = QGroupBox("🔔 Уведомления")
        notify_layout = QFormLayout(notify_group)
        
        self.notify_enabled_check = QCheckBox("Включить уведомления")
        self.notify_enabled_check.toggled.connect(self.toggle_notification_settings)
        notify_layout.addRow(self.notify_enabled_check)
        
        self.sound_check = QCheckBox("Звуковые уведомления")
        notify_layout.addRow(self.sound_check)
        
        self.popup_check = QCheckBox("Всплывающие уведомления")
        notify_layout.addRow(self.popup_check)
        
        # Время уведомлений
        time_group = QGroupBox("⏰ Время уведомлений")
        time_layout = QFormLayout(time_group)
        
        self.early_minutes_spin = QSpinBox()
        self.early_minutes_spin.setRange(1, 60)
        self.early_minutes_spin.setSuffix(" минут")
        time_layout.addRow("Уведомлять за:", self.early_minutes_spin)
        
        self.snooze_minutes_spin = QSpinBox()
        self.snooze_minutes_spin.setRange(1, 30)
        self.snooze_minutes_spin.setSuffix(" минут")
        time_layout.addRow("Откладывать на:", self.snooze_minutes_spin)
        
        # Рабочее время
        hours_group = QGroupBox("🕐 Рабочее время")
        hours_layout = QFormLayout(hours_group)
        
        self.work_start_edit = QLineEdit()
        self.work_start_edit.setPlaceholderText("08:00")
        hours_layout.addRow("Начало:", self.work_start_edit)
        
        self.work_end_edit = QLineEdit()
        self.work_end_edit.setPlaceholderText("22:00")
        hours_layout.addRow("Окончание:", self.work_end_edit)
        
        layout.addWidget(notify_group)
        layout.addWidget(time_group)
        layout.addWidget(hours_group)
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "🔔 Уведомления")
    
    def create_behavior_tab(self):
        """Вкладка поведения приложения"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Автосохранение
        autosave_group = QGroupBox("💾 Автосохранение")
        autosave_layout = QFormLayout(autosave_group)
        
        self.autosave_check = QCheckBox("Включить автосохранение")
        autosave_layout.addRow(self.autosave_check)
        
        self.autosave_interval_spin = QSpinBox()
        self.autosave_interval_spin.setRange(1, 60)
        self.autosave_interval_spin.setSuffix(" минут")
        autosave_layout.addRow("Интервал:", self.autosave_interval_spin)
        
        self.backup_check = QCheckBox("Создавать резервные копии")
        autosave_layout.addRow(self.backup_check)
        
        # Поведение при запуске
        startup_group = QGroupBox("🚀 Запуск приложения")
        startup_layout = QFormLayout(startup_group)
        
        self.start_minimized_check = QCheckBox("Запускать свернутым")
        startup_layout.addRow(self.start_minimized_check)
        
        self.minimize_to_tray_check = QCheckBox("Сворачивать в трей")
        startup_layout.addRow(self.minimize_to_tray_check)
        
        # Подтверждения
        confirm_group = QGroupBox("❓ Подтверждения")
        confirm_layout = QFormLayout(confirm_group)
        
        self.confirm_deletions_check = QCheckBox("Подтверждать удаление")
        confirm_layout.addRow(self.confirm_deletions_check)
        
        self.confirm_exit_check = QCheckBox("Подтверждать выход")
        confirm_layout.addRow(self.confirm_exit_check)
        
        layout.addWidget(autosave_group)
        layout.addWidget(startup_group)
        layout.addWidget(confirm_group)
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "⚙️ Поведение")
    
    def create_blocks_tab(self):
        """Вкладка настроек временных блоков"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Настройки по умолчанию
        default_group = QGroupBox("⚡ Настройки по умолчанию")
        default_layout = QFormLayout(default_group)
        
        self.default_duration_spin = QSpinBox()
        self.default_duration_spin.setRange(15, 240)
        self.default_duration_spin.setSuffix(" минут")
        default_layout.addRow("Длительность:", self.default_duration_spin)
        
        self.default_color_combo = QComboBox()
        colors = ["Красный", "Синий", "Зеленый", "Оранжевый", "Фиолетовый"]
        self.default_color_combo.addItems(colors)
        default_layout.addRow("Цвет:", self.default_color_combo)
        
        # Поведение блоков
        behavior_group = QGroupBox("🎯 Поведение блоков")
        behavior_layout = QFormLayout(behavior_group)
        
        self.show_duration_check = QCheckBox("Показывать длительность")
        behavior_layout.addRow(self.show_duration_check)
        
        self.allow_overlap_check = QCheckBox("Разрешить перекрытие")
        behavior_layout.addRow(self.allow_overlap_check)
        
        self.snap_to_grid_check = QCheckBox("Привязка к сетке")
        behavior_layout.addRow(self.snap_to_grid_check)
        
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setRange(5, 60)
        self.grid_size_spin.setSuffix(" минут")
        behavior_layout.addRow("Размер сетки:", self.grid_size_spin)
        
        layout.addWidget(default_group)
        layout.addWidget(behavior_group)
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "⏱️ Блоки")
    
    def create_integration_tab(self):
        """Вкладка интеграций"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Экспорт данных
        export_group = QGroupBox("📤 Экспорт данных")
        export_layout = QFormLayout(export_group)
        
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["JSON", "CSV", "XML", "PDF"])
        export_layout.addRow("Формат:", self.export_format_combo)
        
        self.auto_export_check = QCheckBox("Автоматический экспорт")
        export_layout.addRow(self.auto_export_check)
        
        # Синхронизация
        sync_group = QGroupBox("☁️ Синхронизация")
        sync_layout = QFormLayout(sync_group)
        
        self.calendar_sync_check = QCheckBox("Синхронизация с календарем")
        sync_layout.addRow(self.calendar_sync_check)
        
        self.cloud_sync_check = QCheckBox("Облачная синхронизация")
        sync_layout.addRow(self.cloud_sync_check)
        
        layout.addWidget(export_group)
        layout.addWidget(sync_group)
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "🔗 Интеграция")
    
    def create_privacy_tab(self):
        """Вкладка конфиденциальности"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Аналитика
        analytics_group = QGroupBox("📊 Аналитика")
        analytics_layout = QFormLayout(analytics_group)
        
        self.analytics_check = QCheckBox("Отправлять анонимную статистику")
        analytics_layout.addRow(self.analytics_check)
        
        self.crash_reports_check = QCheckBox("Отправлять отчеты об ошибках")
        analytics_layout.addRow(self.crash_reports_check)
        
        # Обновления
        update_group = QGroupBox("🔄 Обновления")
        update_layout = QFormLayout(update_group)
        
        self.auto_update_check = QCheckBox("Автоматические обновления")
        update_layout.addRow(self.auto_update_check)
        
        self.beta_updates_check = QCheckBox("Бета-версии")
        update_layout.addRow(self.beta_updates_check)
        
        # Конфиденциальность
        privacy_group = QGroupBox("🔒 Конфиденциальность")
        privacy_layout = QFormLayout(privacy_group)
        
        self.clear_history_btn = QPushButton("Очистить историю")
        self.clear_history_btn.clicked.connect(self.clear_history)
        privacy_layout.addRow("История:", self.clear_history_btn)
        
        self.clear_cache_btn = QPushButton("Очистить кэш")
        self.clear_cache_btn.clicked.connect(self.clear_cache)
        privacy_layout.addRow("Кэш:", self.clear_cache_btn)
        
        layout.addWidget(analytics_group)
        layout.addWidget(update_group)
        layout.addWidget(privacy_group)
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "🔒 Конфиденциальность")
    
    def apply_styles(self):
        """Применение стилей к диалогу"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1A1A1A, stop:1 #2A2A2A);
                color: white;
            }
            QGroupBox {
                color: #FF2B43;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #333;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTabWidget::pane {
                border: 1px solid #333;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #333;
                color: #CCC;
                padding: 8px 16px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #FF2B43;
                color: white;
            }
            QTabBar::tab:hover {
                background: #FF4C63;
            }
        """)
    
    def load_settings(self):
        """Загрузка текущих настроек в UI"""
        # Внешний вид
        theme_map = {"dark": 0, "light": 1, "auto": 2}
        self.theme_combo.setCurrentIndex(
            theme_map.get(self.settings_manager.get("appearance/theme"), 0)
        )
        
        self.language_combo.setCurrentIndex(
            {"ru": 0, "en": 1, "de": 2}.get(self.settings_manager.get("appearance/language"), 0)
        )
        
        self.animations_check.setChecked(
            self.settings_manager.get("appearance/animations_enabled", True)
        )
        self.smooth_scroll_check.setChecked(
            self.settings_manager.get("appearance/smooth_scrolling", True)
        )
        self.font_size_spin.setValue(
            self.settings_manager.get("appearance/font_size", 12)
        )
        self.opacity_slider.setValue(
            int(self.settings_manager.get("appearance/opacity", 1.0) * 100)
        )
        
        # Уведомления
        self.notify_enabled_check.setChecked(
            self.settings_manager.get("notifications/enabled", True)
        )
        self.sound_check.setChecked(
            self.settings_manager.get("notifications/sound_enabled", True)
        )
        self.popup_check.setChecked(
            self.settings_manager.get("notifications/popup_enabled", True)
        )
        self.early_minutes_spin.setValue(
            self.settings_manager.get("notifications/early_minutes", 2)
        )
        self.snooze_minutes_spin.setValue(
            self.settings_manager.get("notifications/snooze_minutes", 5)
        )
        self.work_start_edit.setText(
            self.settings_manager.get("notifications/working_hours_start", "08:00")
        )
        self.work_end_edit.setText(
            self.settings_manager.get("notifications/working_hours_end", "22:00")
        )
        
        # Обновляем состояние зависимых элементов
        self.toggle_notification_settings(self.notify_enabled_check.isChecked())
    
    def toggle_notification_settings(self, enabled):
        """Включение/выключение настроек уведомлений"""
        self.sound_check.setEnabled(enabled)
        self.popup_check.setEnabled(enabled)
        self.early_minutes_spin.setEnabled(enabled)
        self.snooze_minutes_spin.setEnabled(enabled)
        self.work_start_edit.setEnabled(enabled)
        self.work_end_edit.setEnabled(enabled)
    
    def collect_settings(self):
        """Сбор настроек из UI"""
        settings = {
            "appearance/theme": ["dark", "light", "auto"][self.theme_combo.currentIndex()],
            "appearance/language": ["ru", "en", "de"][self.language_combo.currentIndex()],
            "appearance/animations_enabled": self.animations_check.isChecked(),
            "appearance/smooth_scrolling": self.smooth_scroll_check.isChecked(),
            "appearance/font_size": self.font_size_spin.value(),
            "appearance/opacity": self.opacity_slider.value() / 100.0,
            
            "notifications/enabled": self.notify_enabled_check.isChecked(),
            "notifications/sound_enabled": self.sound_check.isChecked(),
            "notifications/popup_enabled": self.popup_check.isChecked(),
            "notifications/early_minutes": self.early_minutes_spin.value(),
            "notifications/snooze_minutes": self.snooze_minutes_spin.value(),
            "notifications/working_hours_start": self.work_start_edit.text(),
            "notifications/working_hours_end": self.work_end_edit.text(),
            
            "behavior/auto_save": self.autosave_check.isChecked(),
            "behavior/auto_save_interval": self.autosave_interval_spin.value(),
            "behavior/minimize_to_tray": self.minimize_to_tray_check.isChecked(),
            "behavior/start_minimized": self.start_minimized_check.isChecked(),
            "behavior/confirm_deletions": self.confirm_deletions_check.isChecked(),
            "behavior/backup_on_start": self.backup_check.isChecked(),
            
            "time_blocks/default_duration": self.default_duration_spin.value(),
            "time_blocks/default_color": ["#FF2B43", "#2B43FF", "#2BFF43", "#FFA52B", "#A52BFF"][self.default_color_combo.currentIndex()],
            "time_blocks/show_duration": self.show_duration_check.isChecked(),
            "time_blocks/allow_overlap": self.allow_overlap_check.isChecked(),
            "time_blocks/snap_to_grid": self.snap_to_grid_check.isChecked(),
            "time_blocks/grid_size": self.grid_size_spin.value(),
            
            "integration/export_format": ["json", "csv", "xml", "pdf"][self.export_format_combo.currentIndex()],
            "integration/auto_export": self.auto_export_check.isChecked(),
            "integration/calendar_sync": self.calendar_sync_check.isChecked(),
            "integration/cloud_sync": self.cloud_sync_check.isChecked(),
            
            "privacy/analytics": self.analytics_check.isChecked(),
            "privacy/crash_reports": self.crash_reports_check.isChecked(),
            "privacy/auto_update": self.auto_update_check.isChecked()
        }
        
        return settings
    
    def apply_settings(self):
        """Применение настроек"""
        try:
            settings = self.collect_settings()
            
            for key, value in settings.items():
                self.settings_manager.set(key, value)
            
            # Сигнал о изменении настроек
            self.settings_changed.emit(settings)
            
            return True
        except Exception as e:
            print(f"Ошибка применения настроек: {e}")
            return False
    
    def reset_settings(self):
        """Сброс настроек к значениям по умолчанию"""
        reply = QMessageBox.question(
            self, 
            "Сброс настроек", 
            "Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.settings_manager.reset_to_defaults()
            self.load_settings()
    
    def export_settings(self):
        """Экспорт настроек в файл"""
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Экспорт настроек", 
            f"timeblocking_settings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )
        
        if filename:
            if self.settings_manager.export_settings(filename):
                QMessageBox.information(self, "Успех", "Настройки успешно экспортированы")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось экспортировать настройки")
    
    def import_settings(self):
        """Импорт настроек из файла"""
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Импорт настроек", 
            "", 
            "JSON Files (*.json)"
        )
        
        if filename:
            if self.settings_manager.import_settings(filename):
                self.load_settings()
                QMessageBox.information(self, "Успех", "Настройки успешно импортированы")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось импортировать настройки")
    
    def clear_history(self):
        """Очистка истории"""
        reply = QMessageBox.question(
            self,
            "Очистка истории",
            "Вы уверены, что хотите очистить историю приложения?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Реализация очистки истории
            pass
    
    def clear_cache(self):
        """Очистка кэша"""
        reply = QMessageBox.question(
            self,
            "Очистка кэша",
            "Вы уверены, что хотите очистить кэш приложения?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Реализация очистки кэша
            pass
    
    def accept(self):
        """Обработка принятия диалога"""
        if self.apply_settings():
            super().accept()
    
    def reject(self):
        """Обработка отмены диалога"""
        # Можно добавить подтверждение отмены
        super().reject()

# Утилиты для работы с настройками
class SettingsUtils:
    """Утилиты для работы с настройками"""
    
    @staticmethod
    def migrate_old_settings(old_settings_path, new_settings_manager):
        """Миграция старых настроек"""
        try:
            if os.path.exists(old_settings_path):
                with open(old_settings_path, 'r') as f:
                    old_settings = json.load(f)
                
                # Конвертация старых настроек в новый формат
                for key, value in old_settings.items():
                    new_settings_manager.set(key, value)
                
                return True
        except:
            return False
    
    @staticmethod
    def validate_settings(settings):
        """Валидация настроек"""
        errors = []
        
        # Проверка времени
        try:
            datetime.strptime(settings.get('notifications/working_hours_start', '08:00'), '%H:%M')
            datetime.strptime(settings.get('notifications/working_hours_end', '22:00'), '%H:%M')
        except ValueError:
            errors.append("Некорректный формат времени")
        
        # Проверка числовых значений
        if not 0 <= settings.get('appearance/opacity', 1.0) <= 1.0:
            errors.append("Непрозрачность должна быть между 0 и 1")
        
        return errors
    
    @staticmethod
    def create_backup(settings_manager, backup_dir="backups"):
        """Создание резервной копии настроек"""
        try:
            os.makedirs(backup_dir, exist_ok=True)
            backup_file = os.path.join(
                backup_dir, 
                f"settings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            return settings_manager.export_settings(backup_file)
        except:
            return False

# Глобальный экземпляр менеджера настроек
app_settings = AppSettings()

def get_settings():
    """Глобальная функция для получения настроек"""
    return app_settings

if __name__ == "__main__":
    # Тестирование настроек
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.show()
    sys.exit(app.exec_())