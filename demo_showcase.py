# demo_showcase.py - Демонстрация всех возможностей гибридного приложения
import time
import json
from datetime import datetime
from task_manager import task_manager
from localization_system import localization

def show_current_stats():
    """Показать текущую статистику"""
    print("\n" + "="*60)
    print("ТЕКУЩАЯ СТАТИСТИКА ПРИЛОЖЕНИЯ")
    print("="*60)
    
    # Московское время
    moscow_time = localization.get_moscow_time()
    print(f"Московское время: {moscow_time.strftime('%H:%M:%S %d.%m.%Y')}")
    
    # Статистика задач
    productivity_data = task_manager.calculate_productivity_today()
    print(f"\nЗадачи на сегодня:")
    print(f"   Всего: {productivity_data['total_tasks']}")
    print(f"   Выполнено: {productivity_data['completed_tasks']}")
    print(f"   В ожидании: {productivity_data['pending_tasks']}")
    
    print(f"\nПродуктивность:")
    print(f"   Процент выполнения: {productivity_data['productivity_percent']:.1f}%")
    print(f"   Эффективность времени: {productivity_data['efficiency']:.1f}%")
    
    print(f"\nВремя:")
    print(f"   Запланировано: {productivity_data['total_time_planned']} мин")
    print(f"   Выполнено: {productivity_data['total_time_completed']} мин")
    
    # Недельная статистика
    weekly_stats = task_manager.get_weekly_stats()
    print(f"\nСтатистика за неделю:")
    for day_stat in weekly_stats[-7:]:
        print(f"   {day_stat['day_name']}: {day_stat['productivity']:.1f}% ({day_stat['completed_tasks']}/{day_stat['total_tasks']})")

def show_language_demo():
    """Демонстрация многоязычности"""
    print("\n" + "="*60)
    print("🌐 ДЕМОНСТРАЦИЯ МНОГОЯЗЫЧНОСТИ")
    print("="*60)
    
    languages = localization.get_supported_languages()
    
    for lang_code, lang_name in languages.items():
        localization.set_language(lang_code)
        print(f"\n🗣️ {lang_name} ({lang_code}):")
        print(f"   Название приложения: {localization.get_text('app_title')}")
        print(f"   Добавить задачу: {localization.get_text('add_task')}")
        print(f"   Продуктивность: {localization.get_text('productivity')}")
        print(f"   Завершено: {localization.get_text('completed_tasks')}")
        print(f"   Московское время: {localization.get_text('moscow_time')}")
    
    # Возвращаем русский язык
    localization.set_language("ru")

def show_task_details():
    """Показать детали задач"""
    print("\n" + "="*60)
    print("📋 ДЕТАЛИ ЗАДАЧ НА СЕГОДНЯ")
    print("="*60)
    
    today_tasks = task_manager.get_tasks_for_today()
    
    if not today_tasks:
        print("❌ Нет задач на сегодня")
        return
    
    # Сортируем по времени
    today_tasks.sort(key=lambda t: t.start_time)
    
    for i, task in enumerate(today_tasks, 1):
        status_emoji = {
            'planned': '⏳',
            'in_progress': '🔄', 
            'completed': '✅',
            'cancelled': '❌'
        }
        
        priority_emoji = {
            'low': '🔵',
            'medium': '🟡',
            'high': '🟠', 
            'urgent': '🔴'
        }
        
        print(f"\n{i}. {task.title}")
        print(f"   {status_emoji.get(task.status.value, '❓')} Статус: {task.status.value}")
        print(f"   {priority_emoji.get(task.priority.value, '⚪')} Приоритет: {task.priority.value}")
        print(f"   ⏰ Время: {task.start_time.strftime('%H:%M')} - {task.end_time.strftime('%H:%M')}")
        print(f"   📝 Описание: {task.description}")
        print(f"   ⏱️ Длительность: {task.get_duration_minutes()} мин")

def show_file_info():
    """Показать информацию о файлах"""
    print("\n" + "="*60)
    print("📁 ИНФОРМАЦИЯ О ФАЙЛАХ ПРОЕКТА")
    print("="*60)
    
    import os
    
    files_info = [
        ("hybrid_app.py", "Главное приложение"),
        ("localization_system.py", "Система локализации"),
        ("task_manager.py", "Менеджер задач"),
        ("demo_tasks.py", "Демонстрационные данные"),
        ("performance.cpp", "C++ модуль производительности"),
        ("data_processor.rs", "Rust модуль обработки данных"),
        ("build_modules.py", "Система сборки"),
        ("tasks_data.json", "Пользовательские данные"),
        ("requirements_updated.txt", "Зависимости")
    ]
    
    for filename, description in files_info:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            size_kb = size / 1024
            print(f"📄 {filename:<25} | {description:<30} | {size_kb:.1f} KB")
        else:
            print(f"❌ {filename:<25} | {description:<30} | Не найден")

def show_architecture_info():
    """Показать информацию об архитектуре"""
    print("\n" + "="*60)
    print("🏗️ АРХИТЕКТУРА ПРИЛОЖЕНИЯ")
    print("="*60)
    
    print("""
🐍 PYTHON (Координатор)
├── PyQt5 GUI интерфейс
├── Система локализации (3 языка)
├── Управление задачами (CRUD)
├── Интеграция с другими модулями
└── Fallback система

🟨 JAVASCRIPT (Dashboard)
├── Chart.js графики
├── Реальное время (московское)
├── CSS3 анимации
├── Responsive дизайн
└── Интерактивные элементы

⚡ C++ (Производительность)
├── Быстрые математические вычисления
├── Оптимизация алгоритмов расписания
├── Анализ паттернов работы
├── Бенчмарки производительности
└── Минимальное использование памяти

🦀 RUST (Обработка данных)
├── Безопасная работа с памятью
├── JSON парсинг и валидация
├── Интеллектуальный анализ данных
├── Генерация рекомендаций
└── Высокая производительность
    """)

def show_demo_commands():
    """Показать команды для демонстрации"""
    print("\n" + "="*60)
    print("🚀 КОМАНДЫ ДЛЯ ДЕМОНСТРАЦИИ")
    print("="*60)
    
    commands = [
        ("python hybrid_app.py", "Запуск основного приложения"),
        ("python demo_tasks.py", "Создание демонстрационных задач"),
        ("python build_modules.py", "Сборка C++ и Rust модулей"),
        ("python demo_showcase.py", "Эта демонстрация"),
    ]
    
    for command, description in commands:
        print(f"💻 {command:<30} | {description}")

def main():
    """Главная функция демонстрации"""
    print("ДОБРО ПОЖАЛОВАТЬ В HYBRID TIME BLOCKING PLANNER!")
    print("Демонстрация всех возможностей приложения")
    
    # Показываем все разделы
    show_current_stats()
    time.sleep(1)
    
    show_language_demo()
    time.sleep(1)
    
    show_task_details()
    time.sleep(1)
    
    show_file_info()
    time.sleep(1)
    
    show_architecture_info()
    time.sleep(1)
    
    show_demo_commands()
    
    print("\n" + "="*60)
    print("🎯 ИТОГОВАЯ ИНФОРМАЦИЯ")
    print("="*60)
    
    print(f"""
✅ Приложение полностью функционально
✅ Поддерживает 3 языка интерфейса
✅ Использует реальные пользовательские данные
✅ Показывает московское время в реальном времени
✅ Рассчитывает продуктивность на основе выполненных задач
✅ Готово к использованию и демонстрации

🚀 Для запуска приложения выполните:
   python hybrid_app.py

📊 Текущая продуктивность: {task_manager.calculate_productivity_today()['productivity_percent']:.1f}%
⏰ Московское время: {localization.format_moscow_time()}

Спасибо за внимание! 🎉
    """)

if __name__ == "__main__":
    main()
