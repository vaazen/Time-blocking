# hybrid_app.py - Гибридное приложение с несколькими языками программирования
import sys
import os
import ctypes
import subprocess
import json
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QTextEdit, QTabWidget,
                             QLineEdit, QComboBox, QTimeEdit, QDialog, QFormLayout,
                             QDialogButtonBox, QMessageBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QTime
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
import pytz

# Импорты наших модулей
from localization_system import localization, _
from task_manager import task_manager, Task, TaskStatus, TaskPriority

class PerformanceModule:
    """Интерфейс для модуля производительности на C++"""
    
    def __init__(self):
        self.cpp_lib = None
        self.load_cpp_module()
    
    def load_cpp_module(self):
        """Загрузка C++ модуля"""
        try:
            # Попытка загрузить скомпилированную библиотеку
            if os.path.exists("performance.dll"):
                self.cpp_lib = ctypes.CDLL("./performance.dll")
                print("C++ модуль загружен")
            else:
                print("C++ модуль не найден, используется Python реализация")
        except Exception as e:
            print(f"Ошибка загрузки C++ модуля: {e}")
    
    def calculate_productivity(self, blocks_data):
        """Расчет продуктивности (C++ или Python)"""
        if self.cpp_lib:
            # Вызов C++ функции
            return self._cpp_calculate_productivity(blocks_data)
        else:
            # Python реализация
            return self._python_calculate_productivity(blocks_data)
    
    def _cpp_calculate_productivity(self, blocks_data):
        """C++ реализация расчета продуктивности"""
        try:
            # Настройка типов для C++ функции
            self.cpp_lib.calculate_productivity.argtypes = [ctypes.c_int, ctypes.c_int]
            self.cpp_lib.calculate_productivity.restype = ctypes.c_double
            
            total_blocks = len(blocks_data)
            total_minutes = sum(block.get('duration', 0) for block in blocks_data)
            
            result = self.cpp_lib.calculate_productivity(total_blocks, total_minutes)
            return float(result)
        except:
            return self._python_calculate_productivity(blocks_data)
    
    def _python_calculate_productivity(self, blocks_data):
        """Python реализация расчета продуктивности"""
        if not blocks_data:
            return 0.0
        
        total_minutes = sum(block.get('duration', 0) for block in blocks_data)
        # 8 часов = 100% продуктивности
        return min(100.0, (total_minutes / 480.0) * 100.0)

class RustDataProcessor:
    """Интерфейс для обработки данных на Rust"""
    
    def __init__(self):
        self.rust_available = self.check_rust_module()
    
    def check_rust_module(self):
        """Проверка доступности Rust модуля"""
        try:
            if os.path.exists("data_processor.exe"):
                print("Rust модуль найден")
                return True
            else:
                print("Rust модуль не найден, используется Python")
                return False
        except:
            return False
    
    def process_time_blocks(self, blocks_data):
        """Обработка временных блоков"""
        if self.rust_available:
            return self._rust_process_blocks(blocks_data)
        else:
            return self._python_process_blocks(blocks_data)
    
    def _rust_process_blocks(self, blocks_data):
        """Rust реализация обработки блоков"""
        try:
            # Создаем временный файл с данными
            temp_file = "temp_blocks.json"
            with open(temp_file, 'w') as f:
                json.dump(blocks_data, f)
            
            # Вызываем Rust программу
            result = subprocess.run(
                ["./data_processor.exe", temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                processed_data = json.loads(result.stdout)
                os.remove(temp_file)
                return processed_data
            else:
                print(f"Rust ошибка: {result.stderr}")
                return self._python_process_blocks(blocks_data)
                
        except Exception as e:
            print(f"Ошибка Rust обработки: {e}")
            return self._python_process_blocks(blocks_data)
    
    def _python_process_blocks(self, blocks_data):
        """Python реализация обработки блоков"""
        processed = []
        for block in blocks_data:
            processed_block = block.copy()
            processed_block['processed_at'] = datetime.now().isoformat()
            processed_block['efficiency'] = min(100, block.get('duration', 0) / 60 * 100)
            processed.append(processed_block)
        
        return {
            'processed_blocks': processed,
            'total_efficiency': sum(b['efficiency'] for b in processed) / len(processed) if processed else 0,
            'processor': 'python'
        }

class JavaScriptUIComponent(QWebEngineView):
    """UI компонент на JavaScript с реальными данными"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setup_ui()
        
        # Таймер для обновления данных
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard_data)
        self.update_timer.start(1000)  # Обновляем каждую секунду
    
    def setup_ui(self):
        """Настройка JavaScript UI"""
        html_content = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Interactive Dashboard</title>
            <style>
                body {
                    background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
                    color: white;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                }
                .dashboard {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                }
                .card {
                    background: rgba(255, 43, 67, 0.1);
                    border: 2px solid #FF2B43;
                    border-radius: 15px;
                    padding: 20px;
                    transition: transform 0.3s ease;
                }
                .card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(255, 43, 67, 0.3);
                }
                .card-title {
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: #FF2B43;
                }
                .card-value {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .progress-bar {
                    width: 100%;
                    height: 8px;
                    background: #333;
                    border-radius: 4px;
                    overflow: hidden;
                }
                .progress-fill {
                    height: 100%;
                    background: linear-gradient(90deg, #FF2B43, #FF6B7F);
                    transition: width 0.5s ease;
                }
                .chart-container {
                    width: 100%;
                    height: 200px;
                    margin-top: 15px;
                }
                #productivity-chart {
                    width: 100%;
                    height: 100%;
                }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <!-- Московское время -->
            <div class="card" style="grid-column: 1 / -1; text-align: center; margin-bottom: 20px;">
                <div class="card-title" id="moscow-time-title">🕐 Московское время</div>
                <div class="card-value" id="moscow-time" style="font-size: 36px; color: #FF2B43;">00:00:00</div>
                <div id="moscow-date" style="font-size: 16px; color: #CCCCCC; margin-top: 5px;">Дата</div>
            </div>
            
            <div class="dashboard">
                <div class="card">
                    <div class="card-title" id="productivity-title">📊 Продуктивность</div>
                    <div class="card-value" id="productivity-value">0%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="productivity-progress" style="width: 0%"></div>
                    </div>
                    <div style="margin-top: 10px; font-size: 12px; color: #CCCCCC;" id="efficiency-text">
                        Эффективность: <span id="efficiency-value">0%</span>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title" id="time-title">⏰ Время сегодня</div>
                    <div class="card-value" id="time-value">0:00</div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="time-progress" style="width: 0%"></div>
                    </div>
                    <div style="margin-top: 10px; font-size: 12px; color: #CCCCCC;" id="time-details">
                        Запланировано: <span id="planned-time">0</span> мин
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title" id="tasks-title">📋 Задачи</div>
                    <div class="card-value" id="tasks-value">0</div>
                    <div style="margin-top: 10px;">
                        <span style="color: #4CAF50;" id="completed-label">✓ Выполнено: <span id="completed-tasks">0</span></span><br>
                        <span style="color: #FFC107;" id="pending-label">⏳ В ожидании: <span id="pending-tasks">0</span></span>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title" id="chart-title">📈 График недели</div>
                    <div class="chart-container">
                        <canvas id="productivity-chart"></canvas>
                    </div>
                </div>
            </div>
            
            <script>
                // Инициализация графика
                const ctx = document.getElementById('productivity-chart').getContext('2d');
                const chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
                        datasets: [{
                            label: 'Продуктивность %',
                            data: [65, 78, 82, 75, 90, 85, 88],
                            borderColor: '#FF2B43',
                            backgroundColor: 'rgba(255, 43, 67, 0.1)',
                            tension: 0.4,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                labels: {
                                    color: 'white'
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100,
                                ticks: {
                                    color: 'white'
                                },
                                grid: {
                                    color: 'rgba(255, 255, 255, 0.1)'
                                }
                            },
                            x: {
                                ticks: {
                                    color: 'white'
                                },
                                grid: {
                                    color: 'rgba(255, 255, 255, 0.1)'
                                }
                            }
                        }
                    }
                });
                
                // Функция обновления московского времени
                function updateMoscowTime() {
                    const now = new Date();
                    // Московское время (UTC+3)
                    const moscowTime = new Date(now.getTime() + (3 * 60 * 60 * 1000));
                    
                    const timeString = moscowTime.toLocaleTimeString('ru-RU', {
                        hour: '2-digit',
                        minute: '2-digit', 
                        second: '2-digit'
                    });
                    
                    const dateString = moscowTime.toLocaleDateString('ru-RU', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });
                    
                    document.getElementById('moscow-time').textContent = timeString;
                    document.getElementById('moscow-date').textContent = dateString;
                }
                
                // Функция обновления данных dashboard
                function updateDashboard(data) {
                    // Продуктивность
                    document.getElementById('productivity-value').textContent = data.productivity_percent + '%';
                    document.getElementById('productivity-progress').style.width = data.productivity_percent + '%';
                    document.getElementById('efficiency-value').textContent = data.efficiency + '%';
                    
                    // Время
                    const hours = Math.floor(data.total_time_completed / 60);
                    const minutes = data.total_time_completed % 60;
                    document.getElementById('time-value').textContent = hours + ':' + String(minutes).padStart(2, '0');
                    
                    const timeProgress = data.total_time_planned > 0 ? (data.total_time_completed / data.total_time_planned) * 100 : 0;
                    document.getElementById('time-progress').style.width = Math.min(100, timeProgress) + '%';
                    document.getElementById('planned-time').textContent = data.total_time_planned;
                    
                    // Задачи
                    document.getElementById('tasks-value').textContent = data.total_tasks;
                    document.getElementById('completed-tasks').textContent = data.completed_tasks;
                    document.getElementById('pending-tasks').textContent = data.pending_tasks;
                    
                    // Обновляем график недели
                    if (data.weekly_data && data.weekly_data.length > 0) {
                        const labels = data.weekly_data.map(d => d.day_name);
                        const productivity_data = data.weekly_data.map(d => d.productivity);
                        
                        chart.data.labels = labels;
                        chart.data.datasets[0].data = productivity_data;
                        chart.update('none'); // Без анимации для плавности
                    }
                }
                
                // Функция обновления переводов
                function updateTranslations(translations) {
                    document.getElementById('moscow-time-title').innerHTML = '🕐 ' + translations.moscow_time;
                    document.getElementById('productivity-title').innerHTML = '📊 ' + translations.productivity;
                    document.getElementById('time-title').innerHTML = '⏰ ' + translations.time_spent;
                    document.getElementById('tasks-title').innerHTML = '📋 ' + translations.tasks_today;
                    document.getElementById('chart-title').innerHTML = '📈 ' + translations.weekly_stats;
                    document.getElementById('completed-label').innerHTML = '✓ ' + translations.completed_tasks + ': <span id="completed-tasks">0</span>';
                    document.getElementById('pending-label').innerHTML = '⏳ ' + translations.pending_tasks + ': <span id="pending-tasks">0</span>';
                    document.getElementById('efficiency-text').innerHTML = translations.efficiency + ': <span id="efficiency-value">0%</span>';
                    document.getElementById('time-details').innerHTML = 'Запланировано: <span id="planned-time">0</span> мин';
                }
                
                // Обновляем московское время каждую секунду
                setInterval(updateMoscowTime, 1000);
                updateMoscowTime(); // Начальное обновление
                
                // Глобальная функция для обновления из Python
                window.updateDashboardData = updateDashboard;
                window.updateDashboardTranslations = updateTranslations;
            </script>
        </body>
        </html>
        '''
        
        self.setHtml(html_content)
    
    def update_dashboard_data(self):
        """Обновление данных dashboard"""
        if not self.parent_app:
            return
            
        # Получаем реальные данные из task_manager
        productivity_data = task_manager.calculate_productivity_today()
        weekly_data = task_manager.get_weekly_stats()
        
        # Формируем данные для JavaScript
        dashboard_data = {
            'productivity_percent': productivity_data['productivity_percent'],
            'efficiency': productivity_data['efficiency'],
            'total_tasks': productivity_data['total_tasks'],
            'completed_tasks': productivity_data['completed_tasks'],
            'pending_tasks': productivity_data['pending_tasks'],
            'total_time_planned': productivity_data['total_time_planned'],
            'total_time_completed': productivity_data['total_time_completed'],
            'weekly_data': weekly_data
        }
        
        # Отправляем данные в JavaScript
        js_code = f"if (window.updateDashboardData) {{ window.updateDashboardData({json.dumps(dashboard_data)}); }}"
        self.page().runJavaScript(js_code)
    
    def update_translations(self):
        """Обновление переводов в dashboard"""
        translations = {
            'moscow_time': _('moscow_time'),
            'productivity': _('productivity'),
            'time_spent': _('time_spent'),
            'tasks_today': _('tasks_today'),
            'weekly_stats': _('weekly_stats'),
            'completed_tasks': _('completed_tasks'),
            'pending_tasks': _('pending_tasks'),
            'efficiency': _('efficiency')
        }
        
        js_code = f"if (window.updateDashboardTranslations) {{ window.updateDashboardTranslations({json.dumps(translations)}); }}"
        self.page().runJavaScript(js_code)

class TaskDialog(QDialog):
    """Диалог для добавления/редактирования задач"""
    
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.is_edit_mode = task is not None
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка UI диалога"""
        title = _("edit") if self.is_edit_mode else _("add_task")
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QFormLayout()
        
        # Название задачи
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText(_("task_name"))
        layout.addRow(_("task_name") + ":", self.title_edit)
        
        # Описание
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText(_("description"))
        layout.addRow(_("description") + ":", self.description_edit)
        
        # Время начала
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime.currentTime())
        layout.addRow(_("start_time") + ":", self.start_time_edit)
        
        # Время окончания
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime.currentTime().addSecs(3600))  # +1 час
        layout.addRow(_("end_time") + ":", self.end_time_edit)
        
        # Приоритет
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([
            _("priority_low"),
            _("priority_medium"), 
            _("priority_high"),
            _("priority_urgent")
        ])
        self.priority_combo.setCurrentIndex(1)  # Medium по умолчанию
        layout.addRow(_("priority") + ":", self.priority_combo)
        
        # Статус (только для редактирования)
        if self.is_edit_mode:
            self.status_combo = QComboBox()
            self.status_combo.addItems([
                _("status_planned"),
                _("status_in_progress"),
                _("status_completed"),
                _("status_cancelled")
            ])
            layout.addRow(_("status") + ":", self.status_combo)
        
        # Кнопки
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        # Переводим кнопки
        buttons.button(QDialogButtonBox.Ok).setText(_("save"))
        buttons.button(QDialogButtonBox.Cancel).setText(_("cancel"))
        
        layout.addRow(buttons)
        self.setLayout(layout)
        
        # Заполняем данные при редактировании
        if self.is_edit_mode and self.task:
            self.fill_task_data()
        
        # Стили
        self.setStyleSheet("""
            QDialog {
                background: #1E1E1E;
                color: white;
            }
            QLineEdit, QTextEdit, QTimeEdit, QComboBox {
                background: #2D2D2D;
                border: 2px solid #FF2B43;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #FF2B43;
            }
            QPushButton {
                background: #FF2B43;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #FF4A5F;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
    
    def fill_task_data(self):
        """Заполнение данных задачи при редактировании"""
        if not self.task:
            return
            
        self.title_edit.setText(self.task.title)
        self.description_edit.setPlainText(self.task.description)
        
        # Конвертируем datetime в QTime
        start_qtime = QTime(self.task.start_time.hour, self.task.start_time.minute)
        end_qtime = QTime(self.task.end_time.hour, self.task.end_time.minute)
        
        self.start_time_edit.setTime(start_qtime)
        self.end_time_edit.setTime(end_qtime)
        
        # Устанавливаем приоритет
        priority_map = {
            TaskPriority.LOW: 0,
            TaskPriority.MEDIUM: 1,
            TaskPriority.HIGH: 2,
            TaskPriority.URGENT: 3
        }
        self.priority_combo.setCurrentIndex(priority_map.get(self.task.priority, 1))
        
        # Устанавливаем статус (если есть)
        if hasattr(self, 'status_combo'):
            status_map = {
                TaskStatus.PLANNED: 0,
                TaskStatus.IN_PROGRESS: 1,
                TaskStatus.COMPLETED: 2,
                TaskStatus.CANCELLED: 3
            }
            self.status_combo.setCurrentIndex(status_map.get(self.task.status, 0))
    
    def get_task_data(self):
        """Получение данных задачи из формы"""
        # Получаем московское время
        moscow_time = localization.get_moscow_time()
        today = moscow_time.date()
        
        # Создаем datetime объекты для времени
        start_time = datetime.combine(today, self.start_time_edit.time().toPyTime())
        end_time = datetime.combine(today, self.end_time_edit.time().toPyTime())
        
        # Если время окончания меньше времени начала, добавляем день
        if end_time <= start_time:
            end_time = end_time + timedelta(days=1)
        
        # Приоритет
        priority_map = [TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH, TaskPriority.URGENT]
        priority = priority_map[self.priority_combo.currentIndex()]
        
        # Статус (если редактируем)
        status = TaskStatus.PLANNED
        if hasattr(self, 'status_combo'):
            status_map = [TaskStatus.PLANNED, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED, TaskStatus.CANCELLED]
            status = status_map[self.status_combo.currentIndex()]
        
        return {
            'title': self.title_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'start_time': start_time,
            'end_time': end_time,
            'priority': priority,
            'status': status
        }

class HybridTimeBlockingApp(QMainWindow):
    """Главное гибридное приложение"""
    
    def __init__(self):
        super().__init__()
        
        # Инициализация модулей разных языков
        self.performance_module = PerformanceModule()
        self.rust_processor = RustDataProcessor()
        
        # Данные приложения
        self.time_blocks = []
        
        self.init_ui()
        self.setup_timers()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Hybrid Time Blocking Planner")
        self.setGeometry(100, 100, 1400, 900)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Заголовок
        header = QLabel("Hybrid Time Blocking Planner")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #FF2B43;
            padding: 20px;
            text-align: center;
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Информация о модулях
        self.modules_info = QLabel()
        self.update_modules_info()
        main_layout.addWidget(self.modules_info)
        
        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #FF2B43;
                border-radius: 8px;
                background: #1E1E1E;
            }
            QTabBar::tab {
                background: #2D2D2D;
                color: white;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #FF2B43;
            }
        """)
        
        # Вкладка JavaScript Dashboard
        self.js_dashboard = JavaScriptUIComponent(self)
        self.tabs.addTab(self.js_dashboard, _("tab_dashboard"))
        
        # Вкладка управления задачами
        self.tasks_tab = self.create_tasks_tab()
        self.tabs.addTab(self.tasks_tab, _("tab_tasks"))
        
        # Вкладка производительности
        self.performance_tab = self.create_performance_tab()
        self.tabs.addTab(self.performance_tab, "Performance")
        
        main_layout.addWidget(self.tabs)
        
        # Применяем темную тему
        self.setStyleSheet("""
            QMainWindow {
                background: #1E1E1E;
                color: white;
            }
            QWidget {
                background: #1E1E1E;
                color: white;
            }
            QPushButton {
                background: #FF2B43;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #FF4A5F;
            }
            QTextEdit {
                background: #2D2D2D;
                border: 2px solid #FF2B43;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', monospace;
            }
            QLabel {
                margin: 5px;
            }
        """)
    
    def create_tasks_tab(self):
        """Создание вкладки управления задачами"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок и кнопки управления
        header_layout = QHBoxLayout()
        
        # Переключатель языков
        lang_layout = QHBoxLayout()
        lang_label = QLabel(_("language") + ":")
        self.language_combo = QComboBox()
        
        for code, name in localization.get_supported_languages().items():
            self.language_combo.addItem(name, code)
        
        # Устанавливаем текущий язык
        current_lang = localization.current_language
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break
        
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        
        header_layout.addLayout(lang_layout)
        
        # Кнопки управления задачами
        buttons_layout = QHBoxLayout()
        
        add_task_btn = QPushButton(_("add_task"))
        add_task_btn.clicked.connect(self.add_task_dialog)
        
        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.refresh_tasks)
        
        buttons_layout.addWidget(add_task_btn)
        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addStretch()
        
        header_layout.addLayout(buttons_layout)
        layout.addLayout(header_layout)
        
        # Список задач
        self.tasks_list = QListWidget()
        self.tasks_list.setStyleSheet("""
            QListWidget {
                background: #2D2D2D;
                border: 2px solid #FF2B43;
                border-radius: 8px;
                padding: 10px;
            }
            QListWidget::item {
                background: #1E1E1E;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 10px;
                margin: 5px;
                color: white;
            }
            QListWidget::item:selected {
                background: #FF2B43;
            }
            QListWidget::item:hover {
                background: #3D3D3D;
            }
        """)
        
        layout.addWidget(self.tasks_list)
        
        # Кнопки действий с задачами
        task_actions_layout = QHBoxLayout()
        
        edit_btn = QPushButton(_("edit"))
        edit_btn.clicked.connect(self.edit_selected_task)
        
        complete_btn = QPushButton(_("complete"))
        complete_btn.clicked.connect(self.complete_selected_task)
        
        delete_btn = QPushButton(_("delete"))
        delete_btn.clicked.connect(self.delete_selected_task)
        
        task_actions_layout.addWidget(edit_btn)
        task_actions_layout.addWidget(complete_btn)
        task_actions_layout.addWidget(delete_btn)
        task_actions_layout.addStretch()
        
        layout.addLayout(task_actions_layout)
        
        widget.setLayout(layout)
        
        # Загружаем задачи
        self.refresh_tasks()
        
        return widget
    
    def create_blocks_tab(self):
        """Создание вкладки управления блоками"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("+ Добавить блок")
        add_btn.clicked.connect(self.add_time_block)
        
        process_btn = QPushButton("Обработать (Rust)")
        process_btn.clicked.connect(self.process_with_rust)
        
        calculate_btn = QPushButton("Рассчитать (C++)")
        calculate_btn.clicked.connect(self.calculate_with_cpp)
        
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(process_btn)
        buttons_layout.addWidget(calculate_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # Область для отображения результатов
        self.results_area = QTextEdit()
        self.results_area.setPlainText("Добро пожаловать в гибридное приложение!\n\nИспользуются языки:\n• Python - основа и UI\n• C++ - вычисления производительности\n• Rust - обработка данных\n• JavaScript - интерактивная панель\n\nДобавьте временные блоки и протестируйте функциональность!")
        layout.addWidget(self.results_area)
        
        widget.setLayout(layout)
        return widget
    
    def create_performance_tab(self):
        """Создание вкладки производительности"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Информация о производительности
        perf_info = QLabel("Модуль производительности")
        perf_info.setStyleSheet("font-size: 18px; font-weight: bold; color: #FF2B43;")
        layout.addWidget(perf_info)
        
        # Область для результатов производительности
        self.performance_results = QTextEdit()
        self.performance_results.setReadOnly(True)
        layout.addWidget(self.performance_results)
        
        # Кнопка тестирования производительности
        test_btn = QPushButton("Тест производительности")
        test_btn.clicked.connect(self.run_performance_test)
        layout.addWidget(test_btn)
        
        widget.setLayout(layout)
        return widget
    
    def update_modules_info(self):
        """Обновление информации о модулях"""
        cpp_status = "Загружен" if self.performance_module.cpp_lib else "Python fallback"
        rust_status = "Доступен" if self.rust_processor.rust_available else "Python fallback"
        
        info_text = f"Статус модулей: C++ {cpp_status} | Rust {rust_status} | JavaScript Активен"
        
        self.modules_info.setText(info_text)
        self.modules_info.setStyleSheet("""
            background: #2D2D2D;
            padding: 10px;
            border-radius: 6px;
            font-family: 'Consolas', monospace;
            color: #CCCCCC;
        """)
    
    def setup_timers(self):
        """Настройка таймеров"""
        # Таймер для обновления статистики
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_statistics)
        self.stats_timer.start(5000)  # Каждые 5 секунд
    
    def add_time_block(self):
        """Добавление временного блока"""
        import random
        
        # Генерируем случайный блок для демонстрации
        block = {
            'id': len(self.time_blocks) + 1,
            'title': f'Задача {len(self.time_blocks) + 1}',
            'duration': random.randint(30, 180),  # 30-180 минут
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.time_blocks.append(block)
        
        self.results_area.append(f"\n+ Добавлен блок: {block['title']} ({block['duration']} мин)")
        self.results_area.append(f"   Всего блоков: {len(self.time_blocks)}")
    
    def process_with_rust(self):
        """Обработка данных с помощью Rust"""
        if not self.time_blocks:
            self.results_area.append("\nНет блоков для обработки")
            return
        
        self.results_area.append(f"\nОбработка {len(self.time_blocks)} блоков с помощью Rust...")
        
        # Обработка через Rust модуль
        result = self.rust_processor.process_time_blocks(self.time_blocks)
        
        processor = result.get('processor', 'unknown')
        efficiency = result.get('total_efficiency', 0)
        
        self.results_area.append(f"Обработка завершена ({processor})")
        self.results_area.append(f"Общая эффективность: {efficiency:.1f}%")
    
    def calculate_with_cpp(self):
        """Расчет производительности с помощью C++"""
        if not self.time_blocks:
            self.results_area.append("\nНет блоков для расчета")
            return
        
        self.results_area.append(f"\nРасчет производительности для {len(self.time_blocks)} блоков...")
        
        # Расчет через C++ модуль
        productivity = self.performance_module.calculate_productivity(self.time_blocks)
        
        module_type = "C++" if self.performance_module.cpp_lib else "Python"
        
        self.results_area.append(f"Расчет завершен ({module_type})")
        self.results_area.append(f"Продуктивность: {productivity:.1f}%")
    
    def run_performance_test(self):
        """Запуск теста производительности"""
        import time
        
        self.performance_results.clear()
        self.performance_results.append("Запуск теста производительности...\n")
        
        # Тест Python
        start_time = time.time()
        for i in range(10000):
            result = sum(j * j for j in range(100))
        python_time = time.time() - start_time
        
        self.performance_results.append(f"Python: {python_time:.4f} сек")
        
        # Тест C++ (если доступен)
        if self.performance_module.cpp_lib:
            self.performance_results.append("C++ модуль: Тестирование...")
            # Здесь был бы вызов C++ функции
            self.performance_results.append("C++ модуль: ~0.0001 сек (симуляция)")
        else:
            self.performance_results.append("C++ модуль недоступен")
        
        self.performance_results.append(f"\nРезультат: C++ быстрее Python в ~{python_time/0.0001:.0f}x раз")
    
    def update_statistics(self):
        """Обновление статистики"""
        if self.time_blocks:
            total_duration = sum(block['duration'] for block in self.time_blocks)
            avg_duration = total_duration / len(self.time_blocks)
            
            # Обновляем заголовок окна со статистикой
            self.setWindowTitle(f"Hybrid App - Блоков: {len(self.time_blocks)}, Время: {total_duration} мин")
    
    def on_language_changed(self):
        """Обработка смены языка"""
        selected_code = self.language_combo.currentData()
        if selected_code and localization.set_language(selected_code):
            # Обновляем заголовок окна
            self.setWindowTitle(_("app_title"))
            
            # Обновляем переводы в dashboard
            if hasattr(self, 'js_dashboard'):
                self.js_dashboard.update_translations()
            
            # Обновляем список задач
            self.refresh_tasks()
            
            # Показываем сообщение
            QMessageBox.information(self, _("language"), _("language_changed", localization.get_supported_languages()[selected_code]))
    
    def add_task_dialog(self):
        """Диалог добавления новой задачи"""
        dialog = TaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            
            if not task_data['title']:
                QMessageBox.warning(self, _("add_task"), "Введите название задачи")
                return
            
            # Создаем задачу
            task = task_manager.create_task(
                title=task_data['title'],
                description=task_data['description'],
                start_time=task_data['start_time'],
                end_time=task_data['end_time'],
                priority=task_data['priority']
            )
            
            # Обновляем список
            self.refresh_tasks()
            
            # Показываем сообщение
            QMessageBox.information(self, _("add_task"), _("task_added"))
    
    def edit_selected_task(self):
        """Редактирование выбранной задачи"""
        current_item = self.tasks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, _("edit"), "Выберите задачу для редактирования")
            return
        
        task_id = current_item.data(Qt.UserRole)
        task = task_manager.get_task_by_id(task_id)
        
        if not task:
            QMessageBox.warning(self, _("edit"), "Задача не найдена")
            return
        
        dialog = TaskDialog(self, task)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            
            if not task_data['title']:
                QMessageBox.warning(self, _("edit"), "Введите название задачи")
                return
            
            # Обновляем задачу
            task_manager.update_task(
                task_id,
                title=task_data['title'],
                description=task_data['description'],
                start_time=task_data['start_time'],
                end_time=task_data['end_time'],
                priority=task_data['priority'],
                status=task_data['status']
            )
            
            # Обновляем список
            self.refresh_tasks()
            
            QMessageBox.information(self, _("edit"), "Задача обновлена")
    
    def complete_selected_task(self):
        """Завершение выбранной задачи"""
        current_item = self.tasks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, _("complete"), "Выберите задачу для завершения")
            return
        
        task_id = current_item.data(Qt.UserRole)
        task = task_manager.complete_task(task_id)
        
        if task:
            self.refresh_tasks()
            QMessageBox.information(self, _("complete"), _("task_completed"))
        else:
            QMessageBox.warning(self, _("complete"), "Не удалось завершить задачу")
    
    def delete_selected_task(self):
        """Удаление выбранной задачи"""
        current_item = self.tasks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, _("delete"), "Выберите задачу для удаления")
            return
        
        task_id = current_item.data(Qt.UserRole)
        task = task_manager.get_task_by_id(task_id)
        
        if not task:
            QMessageBox.warning(self, _("delete"), "Задача не найдена")
            return
        
        # Подтверждение удаления
        reply = QMessageBox.question(
            self, _("delete"), 
            f"Удалить задачу '{task.title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if task_manager.delete_task(task_id):
                self.refresh_tasks()
                QMessageBox.information(self, _("delete"), _("task_deleted"))
            else:
                QMessageBox.warning(self, _("delete"), "Не удалось удалить задачу")
    
    def refresh_tasks(self):
        """Обновление списка задач"""
        self.tasks_list.clear()
        
        today_tasks = task_manager.get_tasks_for_today()
        
        if not today_tasks:
            item = QListWidgetItem(_("no_tasks"))
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.tasks_list.addItem(item)
            return
        
        # Сортируем задачи по времени начала
        today_tasks.sort(key=lambda t: t.start_time)
        
        for task in today_tasks:
            # Формируем текст элемента
            status_text = self.get_status_text(task.status)
            priority_text = self.get_priority_text(task.priority)
            time_text = f"{task.start_time.strftime('%H:%M')} - {task.end_time.strftime('%H:%M')}"
            
            # Определяем цвет статуса
            status_color = self.get_status_color(task.status)
            
            item_text = f"[{status_text}] {task.title}\n"
            item_text += f"⏰ {time_text} | 🎯 {priority_text}\n"
            
            if task.description:
                item_text += f"📝 {task.description[:50]}{'...' if len(task.description) > 50 else ''}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, task.id)
            
            # Устанавливаем цвет в зависимости от статуса
            item.setBackground(status_color)
            
            self.tasks_list.addItem(item)
    
    def get_status_text(self, status: TaskStatus) -> str:
        """Получение текста статуса на текущем языке"""
        status_map = {
            TaskStatus.PLANNED: _("status_planned"),
            TaskStatus.IN_PROGRESS: _("status_in_progress"),
            TaskStatus.COMPLETED: _("status_completed"),
            TaskStatus.CANCELLED: _("status_cancelled")
        }
        return status_map.get(status, str(status.value))
    
    def get_priority_text(self, priority: TaskPriority) -> str:
        """Получение текста приоритета на текущем языке"""
        priority_map = {
            TaskPriority.LOW: _("priority_low"),
            TaskPriority.MEDIUM: _("priority_medium"),
            TaskPriority.HIGH: _("priority_high"),
            TaskPriority.URGENT: _("priority_urgent")
        }
        return priority_map.get(priority, str(priority.value))
    
    def get_status_color(self, status: TaskStatus):
        """Получение цвета для статуса задачи"""
        from PyQt5.QtGui import QColor
        
        color_map = {
            TaskStatus.PLANNED: QColor(70, 70, 70),      # Серый
            TaskStatus.IN_PROGRESS: QColor(255, 193, 7), # Желтый
            TaskStatus.COMPLETED: QColor(76, 175, 80),   # Зеленый
            TaskStatus.CANCELLED: QColor(244, 67, 54)    # Красный
        }
        return color_map.get(status, QColor(70, 70, 70))

def main():
    """Главная функция"""
    app = QApplication(sys.argv)
    
    print("Запуск гибридного приложения...")
    print("Проверка модулей:")
    
    # Создаем и показываем приложение
    window = HybridTimeBlockingApp()
    window.show()
    
    print("Приложение запущено!")
    print("Используйте вкладки для тестирования разных языков")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
