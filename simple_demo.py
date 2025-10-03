# simple_demo.py - Простая демонстрация без эмодзи
from datetime import datetime
from task_manager import task_manager
from localization_system import localization

def show_stats():
    """Показать статистику"""
    print("\n" + "="*50)
    print("СТАТИСТИКА ПРИЛОЖЕНИЯ")
    print("="*50)
    
    # Московское время
    moscow_time = localization.get_moscow_time()
    print(f"Московское время: {moscow_time.strftime('%H:%M:%S %d.%m.%Y')}")
    
    # Статистика задач
    productivity_data = task_manager.calculate_productivity_today()
    print(f"\nЗадачи на сегодня:")
    print(f"  Всего: {productivity_data['total_tasks']}")
    print(f"  Выполнено: {productivity_data['completed_tasks']}")
    print(f"  В ожидании: {productivity_data['pending_tasks']}")
    print(f"  Продуктивность: {productivity_data['productivity_percent']:.1f}%")
    print(f"  Эффективность: {productivity_data['efficiency']:.1f}%")

def show_languages():
    """Показать языки"""
    print("\n" + "="*50)
    print("ПОДДЕРЖИВАЕМЫЕ ЯЗЫКИ")
    print("="*50)
    
    languages = localization.get_supported_languages()
    
    for lang_code, lang_name in languages.items():
        localization.set_language(lang_code)
        print(f"\n{lang_name} ({lang_code}):")
        print(f"  Приложение: {localization.get_text('app_title')}")
        print(f"  Продуктивность: {localization.get_text('productivity')}")
    
    # Возвращаем русский
    localization.set_language("ru")

def show_tasks():
    """Показать задачи"""
    print("\n" + "="*50)
    print("ЗАДАЧИ НА СЕГОДНЯ")
    print("="*50)
    
    today_tasks = task_manager.get_tasks_for_today()
    
    if not today_tasks:
        print("Нет задач на сегодня")
        return
    
    today_tasks.sort(key=lambda t: t.start_time)
    
    for i, task in enumerate(today_tasks, 1):
        print(f"\n{i}. {task.title}")
        print(f"   Статус: {task.status.value}")
        print(f"   Время: {task.start_time.strftime('%H:%M')} - {task.end_time.strftime('%H:%M')}")
        print(f"   Приоритет: {task.priority.value}")

def main():
    print("HYBRID TIME BLOCKING PLANNER - ДЕМОНСТРАЦИЯ")
    print("Многоязычное приложение с реальными данными")
    
    show_stats()
    show_languages()
    show_tasks()
    
    print("\n" + "="*50)
    print("ГОТОВО К ИСПОЛЬЗОВАНИЮ!")
    print("="*50)
    print("Для запуска приложения: python hybrid_app.py")
    print(f"Текущая продуктивность: {task_manager.calculate_productivity_today()['productivity_percent']:.1f}%")

if __name__ == "__main__":
    main()
