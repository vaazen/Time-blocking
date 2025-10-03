from datetime import datetime, time
import datetime as dt
import sys
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QScrollArea, QMessageBox,
                             QInputDialog, QMenuBar, QAction, QFileDialog, QDialog,
                             QSplitter, QSizePolicy, QFrame, QStackedWidget, QTabWidget,
                             QGraphicsDropShadowEffect, QSystemTrayIcon, QMenu, QStatusBar)
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QSize, QTimer
from PyQt5.QtGui import QIcon, QPainter, QPalette, QLinearGradient, QFont, QFontDatabase, QColor

from styles import PremiumTheme
from animations import (FadeAnimation, SlideAnimation, NotificationAnimator, 
                        BouncyAnimation, PulseAnimation, SlideStackedAnimation)
from modern_widgets import PremiumButton, GlassFrame, GradientLabel, StatisticsCard, NavigationBar
from time_block import PremiumTimeBlock
from time_scale import PremiumTimeScale
from data_manager import PremiumDataManager
from notification_manager import PremiumNotificationManager
from settings import SettingsDialog, get_settings

class SplashScreen(QDialog):
    """Экран загрузки приложения"""
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 300)
        
        self.setup_ui()
        self.start_animation()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Логотип
        self.logo_label = QLabel("⏰")
        self.logo_label.setStyleSheet("font-size: 80px;")
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        # Название приложения
        self.title_label = GradientLabel("Time Blocking Planner")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; margin: 20px;")
        
        # Версия
        self.version_label = QLabel("Premium Edition v2.0")
        self.version_label.setStyleSheet("color: #FF6B7F; font-size: 14px;")
        self.version_label.setAlignment(Qt.AlignCenter)
        
        # Прогресс бар
        self.progress_frame = QFrame()
        self.progress_frame.setFixedSize(200, 4)
        self.progress_frame.setStyleSheet("""
            QFrame {
                background: #333;
                border-radius: 2px;
            }
        """)
        
        self.progress_bar = QFrame(self.progress_frame)
        self.progress_bar.setGeometry(0, 0, 0, 4)
        self.progress_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF2B43, stop:1 #FF6B7F);
                border-radius: 2px;
            }
        """)
        
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.version_label)
        layout.addSpacing(40)
        layout.addWidget(self.progress_frame)
        layout.setAlignment(self.progress_frame, Qt.AlignCenter)
        
        self.setLayout(layout)
        
        # Стеклянный эффект
        self.setStyleSheet("""
            QDialog {
                background: rgba(13, 13, 13, 0.95);
                border: 1px solid rgba(255, 43, 67, 0.3);
                border-radius: 20px;
            }
        """)
        
        # Тень
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
    
    def start_animation(self):
        """Анимация прогресса загрузки с дополнительными эффектами"""
        # Анимация прогресс-бара
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"geometry")
        self.progress_animation.setDuration(2000)
        self.progress_animation.setStartValue(self.progress_bar.geometry())
        self.progress_animation.setEndValue(self.progress_frame.rect())
        self.progress_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Анимация пульсации логотипа
        self.logo_pulse = QPropertyAnimation(self.logo_label, b"size")
        self.logo_pulse.setDuration(1500)
        self.logo_pulse.setEasingCurve(QEasingCurve.InOutSine)
        self.logo_pulse.setLoopCount(-1)
        
        original_size = self.logo_label.size()
        pulse_size = QSize(int(original_size.width() * 1.1), int(original_size.height() * 1.1))
        
        self.logo_pulse.setKeyValueAt(0, original_size)
        self.logo_pulse.setKeyValueAt(0.5, pulse_size)
        self.logo_pulse.setKeyValueAt(1, original_size)
        
        # Запуск анимаций
        self.progress_animation.start()
        self.logo_pulse.start()
        
        # Останавливаем пульсацию логотипа через 2 секунды
        QTimer.singleShot(2000, self.logo_pulse.stop)

class MainWindow(QMainWindow):
    """Главное окно приложения премиум-класса"""
    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)  # Минимальный размер
        self.setMaximumSize(1920, 1080)  # Максимальный размер


        # Показываем экран загрузки
        self.splash = SplashScreen()
        self.splash.show()
        
        # Инициализация компонентов
        self.time_blocks = []
        self.current_date = datetime.now().date()
        self.settings_manager = get_settings()
        
        # Менеджеры
        self.data_manager = PremiumDataManager()
        self.notification_manager = PremiumNotificationManager(self)
        
        # Загрузка настроек
        self.load_settings()
        
        # Настройка UI
        self.init_ui()
        self.setup_animations()
        
        # Загрузка данных
        QTimer.singleShot(2000, self.finish_loading)
    
    def resizeEvent(self, event):
        # При изменении размера обновляем отрисовку
        super().resizeEvent(event)
        # Обновляем с небольшой задержкой для стабильности
        QTimer.singleShot(10, self.update_widgets)
    
    def update_widgets(self):
        # Принудительно обновляем все кастомные виджеты
        for widget in self.findChildren(QWidget):
            widget.update()
    
    def finish_loading(self):
        """Завершение загрузки приложения"""
        self.splash.close()
        self.show()
        
        # Загрузка данных текущего дня
        self.load_current_day()
        
        # Запуск сервисов
        self.start_services()
        
        # Показ приветственного сообщения
        self.show_welcome_message()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Time Blocking Planner - Premium Edition")
        self.setGeometry(100, 50, 1600, 1000)
        self.setMinimumSize(1200, 700)
        
        # Применение темы
        PremiumTheme.apply_dark_palette(QApplication.instance())
        self.setStyleSheet(PremiumTheme.get_stylesheet())
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(15)
        central_widget.setLayout(main_layout)
        
        # Верхняя панель
        self.setup_header(main_layout)
        
        # Навигационная панель
        self.setup_navigation(main_layout)
        
        # Основное содержание
        self.setup_content(main_layout)
        
        # Статус бар
        self.setup_status_bar()
        
        # Меню
        self.setup_menu()
        
        # Системный трей
        self.setup_tray()
    
    def setup_header(self, layout):
        """Настройка верхней панели"""
        header_frame = GlassFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Логотип и название
        logo_layout = QHBoxLayout()
        logo_label = QLabel("⏰")
        logo_label.setStyleSheet("font-size: 32px; margin-right: 10px;")
        
        title_label = GradientLabel("Time Blocking Planner")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(title_label)
        logo_layout.addStretch()
        
        # Дата
        self.date_label = QLabel()
        self.update_date_display()
        self.date_label.setStyleSheet("font-size: 16px; color: #FF6B7F; font-weight: bold;")
        
        # Кнопки управления
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        control_buttons = [
            ("🎯 Новый день", self.new_day, "secondary"),
            ("💾 Сохранить", self.save_current_day, "secondary"),
            ("📊 Статистика", self.show_statistics, ""),
            ("⚙️ Настройки", self.show_settings, ""),
            ("🎨 Тема", self.change_theme, "")
        ]
        
        for text, slot, style in control_buttons:
            btn = PremiumButton(text)
            if style:
                btn.setProperty("class", style)
            btn.clicked.connect(slot)
            btn.setFixedHeight(35)
            controls_layout.addWidget(btn)
        
        header_layout.addLayout(logo_layout)
        header_layout.addSpacing(20)
        header_layout.addWidget(self.date_label)
        header_layout.addStretch()
        header_layout.addLayout(controls_layout)
        
        layout.addWidget(header_frame)
    
    def setup_navigation(self, layout):
        """Настройка навигационной панели"""
        self.nav_bar = NavigationBar()
        self.nav_bar.tabChanged.connect(self.switch_tab)
        layout.addWidget(self.nav_bar)
    
    def setup_content(self, layout):
        """Настройка основного контента"""
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Боковая панель (статистика)
        self.sidebar = self.create_sidebar()
        content_splitter.addWidget(self.sidebar)
        content_splitter.setStretchFactor(0, 0)
        content_splitter.setStretchFactor(1, 1)
        
        # Основная область
        self.stacked_widget = QStackedWidget()
        
        # Вкладка планирования
        self.schedule_tab = self.create_schedule_tab()
        self.stacked_widget.addWidget(self.schedule_tab)
        
        # Вкладка статистики
        self.stats_tab = self.create_stats_tab()
        self.stacked_widget.addWidget(self.stats_tab)
        
        # Вкладка настроек
        self.settings_tab = self.create_settings_tab()
        self.stacked_widget.addWidget(self.settings_tab)
        
        content_splitter.addWidget(self.stacked_widget)
        content_splitter.setSizes([300, 1000])
        
        layout.addWidget(content_splitter)
    
    def create_sidebar(self):
        """Создание боковой панели"""
        sidebar = QScrollArea()
        sidebar.setWidgetResizable(True)
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setSpacing(15)
        
        # Быстрые действия
        quick_actions = GlassFrame()
        quick_layout = QVBoxLayout(quick_actions)
        
        quick_title = QLabel("Быстрые действия")
        quick_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF2B43;")
        quick_layout.addWidget(quick_title)
        
        quick_buttons = [
            ("➕ Быстрый блок", self.quick_add_block),
            ("📅 На сегодня", self.focus_today),
            ("🚀 Автопланирование", self.auto_schedule),
            ("🧹 Очистить день", self.clear_day)
        ]
        
        for text, slot in quick_buttons:
            btn = PremiumButton(text)
            btn.clicked.connect(slot)
            btn.setFixedHeight(35)
            quick_layout.addWidget(btn)
        
        sidebar_layout.addWidget(quick_actions)
        
        # Статистика дня
        self.stats_cards = GlassFrame()
        stats_layout = QVBoxLayout(self.stats_cards)
        
        stats_title = QLabel("Статистика дня")
        stats_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF2B43;")
        stats_layout.addWidget(stats_title)
        
        self.blocks_card = StatisticsCard("Блоки", "0", "шт")
        self.time_card = StatisticsCard("Время", "0:00", "часов")
        self.productivity_card = StatisticsCard("Продуктивность", "0", "%")
        
        stats_layout.addWidget(self.blocks_card)
        stats_layout.addWidget(self.time_card)
        stats_layout.addWidget(self.productivity_card)
        
        sidebar_layout.addWidget(self.stats_cards)
        sidebar_layout.addStretch()
        
        sidebar.setWidget(sidebar_widget)
        return sidebar
    
    def create_schedule_tab(self):
        """Создание вкладки планирования"""
        tab_widget = QWidget()
        layout = QHBoxLayout(tab_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Шкала времени
        self.time_scale = PremiumTimeScale()
        self.time_scale.setFixedWidth(120)
        layout.addWidget(self.time_scale)
        
        # Область блоков
        blocks_container = QWidget()
        blocks_layout = QVBoxLayout(blocks_container)
        blocks_layout.setContentsMargins(0, 0, 0, 0)
        
        # Панель инструментов блоков
        tools_frame = QFrame()
        tools_layout = QHBoxLayout(tools_frame)
        
        view_buttons = [
            ("📋 Список", self.switch_to_list_view),
            ("⏰ Время", self.switch_to_time_view),
            ("🎯 Приоритет", self.switch_to_priority_view)
        ]
        
        for text, slot in view_buttons:
            btn = PremiumButton(text)
            btn.clicked.connect(slot)
            btn.setFixedHeight(30)
            tools_layout.addWidget(btn)
        
        tools_layout.addStretch()
        
        # Кнопка добавления
        add_btn = PremiumButton("➕ Добавить блок")
        add_btn.clicked.connect(self.add_time_block_dialog)
        add_btn.setFixedHeight(30)
        tools_layout.addWidget(add_btn)
        
        blocks_layout.addWidget(tools_frame)
        
        # Область для блоков
        self.blocks_scroll = QScrollArea()
        self.blocks_scroll.setWidgetResizable(True)
        self.blocks_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.blocks_widget = QWidget()
        self.blocks_widget.setMouseTracking(True)
        self.blocks_widget.mousePressEvent = self.handle_canvas_click
        self.blocks_layout = QVBoxLayout(self.blocks_widget)
        self.blocks_layout.setAlignment(Qt.AlignTop)
        self.blocks_layout.setSpacing(10)
        
        self.blocks_scroll.setWidget(self.blocks_widget)
        blocks_layout.addWidget(self.blocks_scroll)
        
        layout.addWidget(blocks_container)
        
        return tab_widget
    
    def create_stats_tab(self):
        """Создание вкладки статистики"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        # Заголовок
        title = QLabel("📊 Детальная статистика")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF2B43; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Здесь будет расширенная статистика
        stats_info = QLabel("Расширенная статистика будет доступна в следующем обновлении")
        stats_info.setStyleSheet("font-size: 16px; color: #CCCCCC;")
        stats_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(stats_info)
        
        return tab_widget
    
    def create_settings_tab(self):
        """Создание вкладки настроек"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        # Заголовок
        title = QLabel("⚙️ Настройки")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF2B43; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Здесь будут настройки
        settings_info = QLabel("Настройки будут доступны в следующем обновлении")
        settings_info.setStyleSheet("font-size: 16px; color: #CCCCCC;")
        settings_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(settings_info)
        
        return tab_widget
    
    def setup_status_bar(self):
        """Настройка статус бара"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Левая часть - информация о дне
        self.day_info_label = QLabel("Загрузка...")
        status_bar.addWidget(self.day_info_label, 1)
        
        # Правая часть - системная информация
        self.sys_info_label = QLabel("Готов к работе")
        status_bar.addPermanentWidget(self.sys_info_label)
    
    def setup_menu(self):
        """Настройка меню"""
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("📁 Файл")
        file_menu.addAction("📅 Новый день", self.new_day, "Ctrl+N")
        file_menu.addAction("💾 Сохранить", self.save_current_day, "Ctrl+S")
        file_menu.addSeparator()
        file_menu.addAction("📤 Экспорт", self.export_data)
        file_menu.addAction("📥 Импорт", self.import_data)
        file_menu.addSeparator()
        file_menu.addAction("🚪 Выход", self.close, "Ctrl+Q")
        
        # Меню Правка
        edit_menu = menubar.addMenu("✏️ Правка")
        edit_menu.addAction("➕ Добавить блок", self.add_time_block_dialog, "Insert")
        edit_menu.addAction("🎯 Автопланирование", self.auto_schedule)
        edit_menu.addSeparator()
        edit_menu.addAction("🧹 Очистить день", self.clear_day)
        
        # Меню Вид
        view_menu = menubar.addMenu("👁️ Вид")
        view_menu.addAction("📋 Список", self.switch_to_list_view)
        view_menu.addAction("⏰ Время", self.switch_to_time_view)
        view_menu.addAction("🎯 Приоритет", self.switch_to_priority_view)
        view_menu.addSeparator()
        view_menu.addAction("🎨 Сменить тему", self.change_theme)
        
        # Меню Сервис
        tool_menu = menubar.addMenu("⚙️ Сервис")
        tool_menu.addAction("📊 Статистика", self.show_statistics)
        tool_menu.addAction("🔔 Уведомления", self.toggle_notifications)
        tool_menu.addAction("⚙️ Настройки", self.show_settings)
        
        # Меню Помощь
        help_menu = menubar.addMenu("❓ Помощь")
        help_menu.addAction("📖 О программе", self.show_about)
        help_menu.addAction("🎯 Советы", self.show_tips)
    
    def setup_tray(self):
        """Настройка системного трея"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QApplication.windowIcon())
        
        tray_menu = QMenu()
        tray_menu.addAction("Показать", self.show)
        tray_menu.addAction("Скрыть", self.hide)
        tray_menu.addSeparator()
        tray_menu.addAction("Выход", QApplication.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def setup_animations(self):
        """Настройка анимаций"""
        self.fade_animation = FadeAnimation(self)
        self.slide_animation = SlideAnimation(self)
        self.bouncy_animation = BouncyAnimation(self)
        self.slide_stacked_animation = SlideStackedAnimation(self.stacked_widget)
        
        # Анимации для кнопок
        self.button_animations = {}
        
        # Пульсация для важных элементов
        self.pulse_animations = {}
    
    def switch_tab(self, index):
        """Переключение между вкладками с анимацией"""
        current_index = self.stacked_widget.currentIndex()
        
        # Определяем направление анимации
        direction = "left" if index > current_index else "right"
        
        # Используем новую анимацию скольжения
        self.slide_stacked_animation.slide_to_widget(index, direction)
        
        # Обновляем навигационную панель
        if hasattr(self, 'nav_bar'):
            self.nav_bar.setCurrentIndex(index)
    
    def handle_canvas_click(self, event):
        """Обработка клика по области блоков"""
        if event.button() == Qt.LeftButton:
            # Расчет времени по позиции клика
            y_pos = event.pos().y()
            start_minutes = 8 * 60 + (y_pos // 2)
            duration = 60  # 1 час по умолчанию
            
            start_time = datetime.now().replace(hour=0, minute=0) + timedelta(minutes=start_minutes)
            end_time = start_time + timedelta(minutes=duration)
            
            self.add_time_block(start_time, end_time)
    
    def add_time_block_dialog(self):
        """Диалог добавления временного блока"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QTimeEdit
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить временной блок")
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout(dialog)
        
        title_edit = QLineEdit()
        title_edit.setPlaceholderText("Введите название задачи")
        layout.addRow("Название:", title_edit)
        
        start_time_edit = QTimeEdit()
        start_time_edit.setTime(datetime.now().time())
        layout.addRow("Время начала:", start_time_edit)
        
        end_time_edit = QTimeEdit()
        end_time_edit.setTime((datetime.now() + timedelta(hours=1)).time())
        layout.addRow("Время окончания:", end_time_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            # Получаем время из QTimeEdit
            start_q_time = start_time_edit.time()
            end_q_time = end_time_edit.time()
            
            # Преобразуем QTime в datetime.time
            start_py_time = time(start_q_time.hour(), start_q_time.minute(), start_q_time.second())
            end_py_time = time(end_q_time.hour(), end_q_time.minute(), end_q_time.second())
            
            # Создаем полные datetime объекты
            start_dt = datetime.combine(self.current_date, start_py_time)
            end_dt = datetime.combine(self.current_date, end_py_time)
            
            # Добавляем блок
            self.add_time_block(start_dt, end_dt, title_edit.text())
    
    def add_time_block(self, start_time, end_time, title="Новая задача"):
        """Добавление временного блока с анимацией"""
        block = PremiumTimeBlock(start_time, end_time, title)
        block.deleted.connect(self.delete_time_block)
        block.edited.connect(self.update_time_block)
        
        self.time_blocks.append(block)
        self.blocks_layout.addWidget(block)
        
        # Показываем блок
        block.show()
        
        # Анимация появления с отскоком
        QTimer.singleShot(50, lambda: self.animate_block_appearance(block))
        
        self.update_stats()
        self.statusBar().showMessage(f"Добавлен блок: {title}")
    
    def animate_block_appearance(self, block):
        """Анимация появления блока"""
        bouncy_anim = BouncyAnimation(block, duration=600)
        bouncy_anim.bounce_in()
        
        # Добавляем пульсацию на короткое время
        pulse_anim = PulseAnimation(block, duration=800)
        pulse_anim.start_pulse(1.03)
        
        # Останавливаем пульсацию через 2 секунды
        QTimer.singleShot(2000, pulse_anim.stop_pulse)
    
    def delete_time_block(self, block):
        """Удаление временного блока"""
        reply = QMessageBox.question(self, "Удаление", 
                                   f"Удалить блок '{block.title}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.time_blocks.remove(block)
            block.deleteLater()
            self.update_stats()
            self.statusBar().showMessage("Блок удален")
    
    def update_time_block(self, block):
        """Обновление временного блока"""
        self.update_stats()
        self.statusBar().showMessage(f"Обновлен блок: {block.title}")
    
    def new_day(self):
        """Начало нового дня"""
        reply = QMessageBox.question(self, "Новый день", 
                                   "Сохранить текущий день перед очисткой?",
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        
        if reply != QMessageBox.Cancel:
            if reply == QMessageBox.Yes:
                self.save_current_day()
            
            # Очистка блоков
            for block in self.time_blocks:
                block.deleteLater()
            self.time_blocks.clear()
            
            # Новый день
            self.current_date = datetime.now().date()
            self.update_date_display()
            self.update_stats()
            
            self.statusBar().showMessage("Начат новый день")
    
    def save_current_day(self):
        """Сохранение текущего дня"""
        if self.data_manager.save_day(self.time_blocks, self.current_date):
            self.statusBar().showMessage("День сохранен")
        else:
            self.statusBar().showMessage("Ошибка сохранения")
    
    def load_current_day(self):
        """Загрузка текущего дня"""
        blocks_data = self.data_manager.load_day(self.current_date)
        
        for block_data in blocks_data:
            try:
                start_time = datetime.fromisoformat(block_data["start_time"])
                end_time = datetime.fromisoformat(block_data["end_time"])
                
                block = PremiumTimeBlock(
                    start_time, end_time,
                    block_data["title"],
                    block_data.get("color", "#FF2B43"),
                    block_data.get("notify", True)
                )
                
                block.deleted.connect(self.delete_time_block)
                block.edited.connect(self.update_time_block)
                
                self.time_blocks.append(block)
                self.blocks_layout.addWidget(block)
                
            except Exception as e:
                print(f"Ошибка загрузки блока: {e}")
        
        self.update_stats()
        self.statusBar().showMessage(f"Загружено {len(blocks_data)} блоков")
    
    def update_stats(self):
        """Обновление статистики с анимацией"""
        total_blocks = len(self.time_blocks)
        total_minutes = sum(block.get_duration_minutes() for block in self.time_blocks)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        productivity = min(100, int((total_minutes / 480) * 100))
        
        # Обновление карточек статистики с анимацией
        self.animate_stat_update(self.blocks_card, total_blocks)
        self.animate_stat_update(self.time_card, f"{hours:02d}:{minutes:02d}")
        self.animate_stat_update(self.productivity_card, productivity)
        
        # Обновление статус бара
        self.day_info_label.setText(
            f"Блоков: {total_blocks} | Время: {hours:02d}:{minutes:02d} | Продуктивность: {productivity}%"
        )
    
    def animate_stat_update(self, card, new_value):
        """Анимация обновления статистической карточки"""
        # Создаем анимацию масштабирования
        scale_anim = QPropertyAnimation(card, b"size")
        scale_anim.setDuration(200)
        scale_anim.setEasingCurve(QEasingCurve.OutBack)
        
        original_size = card.size()
        scaled_size = QSize(
            int(original_size.width() * 1.05),
            int(original_size.height() * 1.05)
        )
        
        # Анимация увеличения
        scale_anim.setStartValue(original_size)
        scale_anim.setEndValue(scaled_size)
        
        def on_scale_finished():
            # Обновляем значение
            card.update_value(new_value)
            
            # Анимация возврата к исходному размеру
            return_anim = QPropertyAnimation(card, b"size")
            return_anim.setDuration(200)
            return_anim.setEasingCurve(QEasingCurve.OutBack)
            return_anim.setStartValue(scaled_size)
            return_anim.setEndValue(original_size)
            return_anim.start()
        
        scale_anim.finished.connect(on_scale_finished)
        scale_anim.start()
    
    def update_date_display(self):
        """Обновление отображения даты"""
        date_str = self.current_date.strftime("%d %B %Y (%A)")
        if self.current_date == datetime.now().date():
            date_str += " - СЕГОДНЯ"
        
        self.date_label.setText(f"📅 {date_str}")
    
    def load_settings(self):
        """Загрузка настроек"""
        # Загрузка настроек из файла или установка значений по умолчанию
        self.settings = {
            "theme": "dark",
            "notifications": True,
            "auto_save": True,
            "language": "ru"
        }
    
    def start_services(self):
        """Запуск фоновых сервисов"""
        # Автосохранение
        if self.settings.get("auto_save", True):
            self.auto_save_timer = QTimer()
            self.auto_save_timer.timeout.connect(self.auto_save)
            self.auto_save_timer.start(300000)  # 5 минут
        
        # Проверка уведомлений
        self.notification_manager.start()
    
    def auto_save(self):
        """Автосохранение"""
        if self.time_blocks:
            self.data_manager.save_day(self.time_blocks, self.current_date)
            self.sys_info_label.setText("Автосохранение выполнено")
    
    def show_welcome_message(self):
        """Показать приветственное сообщение"""
        NotificationAnimator.show_notification(
            self, "Добро пожаловать в Time Blocking Planner Premium!", 3000
        )
    
    # Дополнительные методы для быстрых действий
    def quick_add_block(self):
        """Быстрое добавление блока"""
        current_time = datetime.now()
        start_time = current_time.replace(minute=(current_time.minute // 30) * 30)
        end_time = start_time + timedelta(hours=1)
        
        self.add_time_block(start_time, end_time, "Быстрая задача")
    
    def focus_today(self):
        """Фокусировка на сегодняшнем дне"""
        self.current_date = datetime.now().date()
        self.update_date_display()
        self.load_current_day()
    
    def auto_schedule(self):
        """Автопланирование"""
        QMessageBox.information(self, "Автопланирование", 
                              "Функция автопланирования будет доступна в следующем обновлении")
    
    def clear_day(self):
        """Очистка дня"""
        reply = QMessageBox.question(self, "Очистка дня", 
                                   "Очистить все временные блоки?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for block in self.time_blocks:
                block.deleteLater()
            self.time_blocks.clear()
            self.update_stats()
    
    def switch_to_list_view(self):
        """Переключение в режим списка"""
        self.statusBar().showMessage("Режим: Список")
    
    def switch_to_time_view(self):
        """Переключение в режим времени"""
        self.statusBar().showMessage("Режим: Временная шкала")
    
    def switch_to_priority_view(self):
        """Переключение в режим приоритетов"""
        self.statusBar().showMessage("Режим: Приоритеты")
    
    def change_theme(self):
        """Смена темы"""
        themes = ["Темная", "Светлая", "Авто"]
        theme, ok = QInputDialog.getItem(self, "Смена темы", "Выберите тему:", themes, 0, False)
        
        if ok:
            self.settings["theme"] = theme.lower()
            self.setStyleSheet(PremiumTheme.get_stylesheet(theme.lower()))
            self.statusBar().showMessage(f"Тема изменена на: {theme}")
    
    def show_statistics(self):
        """Показать статистику"""
        self.switch_tab(1)  # Переключение на вкладку статистики
    
    def show_settings(self):
        """Показать настройки"""
        self.switch_tab(2)  # Переключение на вкладку настроек
    
    def toggle_notifications(self):
        """Переключение уведомлений"""
        self.settings["notifications"] = not self.settings.get("notifications", True)
        status = "включены" if self.settings["notifications"] else "выключены"
        self.statusBar().showMessage(f"Уведомления {status}")
    
    def export_data(self):
        """Экспорт данных"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт данных", 
            f"timeblocking_export_{self.current_date.strftime('%Y-%m-%d')}.json",
            "JSON Files (*.json)"
        )
        
        if filename:
            # Реализация экспорта
            pass
    
    def import_data(self):
        """Импорт данных"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Импорт данных", "", "JSON Files (*.json)"
        )
        
        if filename:
            # Реализация импорта
            pass
    
    def show_about(self):
        """Показать информацию о программе"""
        QMessageBox.about(self, "О программе", 
                         "Планировщик времени")
    
    def show_tips(self):
        """Показать советы"""
        QMessageBox.information(self, "Советы", 
                              "💡 Используйте быстрые клавиши для эффективной работы\n"
                              "💡 Настраивайте уведомления для важных задач\n"
                              "💡 Экспортируйте данные для резервного копирования")
    
    def tray_icon_activated(self, reason):
        """Обработка активации иконки в трее"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.raise_()
            self.activateWindow()
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        if self.time_blocks and self.settings.get("auto_save", True):
            self.data_manager.save_day(self.time_blocks, self.current_date)
        
        self.notification_manager.stop()
        
        # Скрыть в трей вместо закрытия
        if self.settings.get("minimize_to_tray", True) and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()

    def show_settings_dialog(self):
        """Показать диалог настроек"""
        dialog = SettingsDialog(self, self.settings_manager)
        dialog.settings_changed.connect(self.on_settings_changed)
        dialog.exec_()

    def on_settings_changed(self, new_settings):
        """Обработка изменения настроек"""
        # Применяем новые настройки
        if 'appearance/theme' in new_settings:
            self.apply_theme(new_settings['appearance/theme'])
        
        if 'appearance/font_size' in new_settings:
            self.apply_font_size(new_settings['appearance/font_size'])
        
        # Обновляем другие компоненты...
        self.statusBar().showMessage("Настройки применены")


def main():
    """Основная функция приложения"""
    app = QApplication(sys.argv)
    app.setApplicationName("Планировщик времени")
    app.setApplicationVersion("5.0")
    app.setOrganizationName("КС54 4 вариант")
    
    # Загрузка шрифтов (если нужно)
    # QFontDatabase.addApplicationFont("assets/fonts/Inter.ttf")
    
    window = MainWindow()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()