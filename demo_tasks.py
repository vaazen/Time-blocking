# demo_tasks.py - Создание демонстрационных задач для тестирования
from datetime import datetime, timedelta
import pytz
from task_manager import task_manager, TaskPriority, TaskStatus

def create_demo_tasks():
    """Создание демонстрационных задач на сегодня"""
    
    # Московская временная зона
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    today = now.date()
    
    print("Создание демонстрационных задач...")
    
    # Очищаем существующие задачи на сегодня (автоматически)
    existing_tasks = task_manager.get_tasks_for_today()
    if existing_tasks:
        print(f"Найдено {len(existing_tasks)} существующих задач на сегодня")
        print("Удаляем существующие задачи...")
        for task in existing_tasks:
            task_manager.delete_task(task.id)
        print("Существующие задачи удалены")
    
    # Демонстрационные задачи
    demo_tasks = [
        {
            'title': 'Утренняя зарядка',
            'description': 'Комплекс упражнений для бодрого начала дня',
            'start_hour': 7,
            'start_minute': 0,
            'duration_minutes': 30,
            'priority': TaskPriority.MEDIUM,
            'status': TaskStatus.COMPLETED
        },
        {
            'title': 'Завтрак и планирование дня',
            'description': 'Здоровый завтрак и составление плана на день',
            'start_hour': 8,
            'start_minute': 0,
            'duration_minutes': 45,
            'priority': TaskPriority.HIGH,
            'status': TaskStatus.COMPLETED
        },
        {
            'title': 'Работа над проектом',
            'description': 'Разработка гибридного приложения Time Blocking Planner',
            'start_hour': 9,
            'start_minute': 0,
            'duration_minutes': 180,  # 3 часа
            'priority': TaskPriority.URGENT,
            'status': TaskStatus.IN_PROGRESS
        },
        {
            'title': 'Обеденный перерыв',
            'description': 'Обед и короткий отдых',
            'start_hour': 12,
            'start_minute': 30,
            'duration_minutes': 60,
            'priority': TaskPriority.MEDIUM,
            'status': TaskStatus.PLANNED
        },
        {
            'title': 'Встреча с командой',
            'description': 'Обсуждение прогресса и планов на следующую неделю',
            'start_hour': 14,
            'start_minute': 0,
            'duration_minutes': 90,
            'priority': TaskPriority.HIGH,
            'status': TaskStatus.PLANNED
        },
        {
            'title': 'Изучение новых технологий',
            'description': 'Изучение Rust и WebAssembly для будущих проектов',
            'start_hour': 16,
            'start_minute': 0,
            'duration_minutes': 120,
            'priority': TaskPriority.MEDIUM,
            'status': TaskStatus.PLANNED
        },
        {
            'title': 'Спортзал',
            'description': 'Силовая тренировка и кардио',
            'start_hour': 18,
            'start_minute': 30,
            'duration_minutes': 90,
            'priority': TaskPriority.HIGH,
            'status': TaskStatus.PLANNED
        },
        {
            'title': 'Ужин с семьей',
            'description': 'Семейный ужин и общение',
            'start_hour': 20,
            'start_minute': 0,
            'duration_minutes': 60,
            'priority': TaskPriority.HIGH,
            'status': TaskStatus.PLANNED
        },
        {
            'title': 'Чтение книги',
            'description': 'Чтение технической литературы перед сном',
            'start_hour': 21,
            'start_minute': 30,
            'duration_minutes': 60,
            'priority': TaskPriority.LOW,
            'status': TaskStatus.PLANNED
        }
    ]
    
    created_count = 0
    
    for task_data in demo_tasks:
        try:
            # Создаем datetime объекты
            start_time = datetime.combine(
                today, 
                datetime.min.time().replace(
                    hour=task_data['start_hour'], 
                    minute=task_data['start_minute']
                )
            )
            start_time = moscow_tz.localize(start_time)
            
            end_time = start_time + timedelta(minutes=task_data['duration_minutes'])
            
            # Создаем задачу
            task = task_manager.create_task(
                title=task_data['title'],
                description=task_data['description'],
                start_time=start_time,
                end_time=end_time,
                priority=task_data['priority']
            )
            
            # Устанавливаем статус (если не запланированная)
            if task_data['status'] != TaskStatus.PLANNED:
                task_manager.update_task(task.id, status=task_data['status'])
                if task_data['status'] == TaskStatus.COMPLETED:
                    task_manager.complete_task(task.id)
            
            created_count += 1
            print(f"Создана задача: {task_data['title']}")
            
        except Exception as e:
            print(f"Ошибка создания задачи '{task_data['title']}': {e}")
    
    print(f"\nСоздано {created_count} демонстрационных задач")
    
    # Показываем статистику
    productivity_data = task_manager.calculate_productivity_today()
    print(f"\nТекущая статистика:")
    print(f"  Всего задач: {productivity_data['total_tasks']}")
    print(f"  Выполнено: {productivity_data['completed_tasks']}")
    print(f"  В ожидании: {productivity_data['pending_tasks']}")
    print(f"  Продуктивность: {productivity_data['productivity_percent']:.1f}%")
    print(f"  Эффективность: {productivity_data['efficiency']:.1f}%")
    print(f"  Запланировано времени: {productivity_data['total_time_planned']} мин")
    print(f"  Выполнено времени: {productivity_data['total_time_completed']} мин")

def create_weekly_demo_data():
    """Создание демонстрационных данных за неделю"""
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    print("\nСоздание данных за прошлые дни...")
    
    # Данные за предыдущие дни
    for days_ago in range(1, 7):
        day = now - timedelta(days=days_ago)
        day_date = day.date()
        
        # Создаем несколько задач для каждого дня
        tasks_for_day = [
            {
                'title': f'Работа - день {days_ago}',
                'description': 'Основная рабочая деятельность',
                'start_hour': 9,
                'duration_minutes': 240,
                'priority': TaskPriority.HIGH,
                'completed': True
            },
            {
                'title': f'Обучение - день {days_ago}',
                'description': 'Изучение новых технологий',
                'start_hour': 14,
                'duration_minutes': 120,
                'priority': TaskPriority.MEDIUM,
                'completed': days_ago <= 4  # Выполнено только для недавних дней
            },
            {
                'title': f'Спорт - день {days_ago}',
                'description': 'Физические упражнения',
                'start_hour': 18,
                'duration_minutes': 60,
                'priority': TaskPriority.MEDIUM,
                'completed': days_ago <= 3
            }
        ]
        
        for task_data in tasks_for_day:
            try:
                start_time = datetime.combine(
                    day_date,
                    datetime.min.time().replace(hour=task_data['start_hour'])
                )
                start_time = moscow_tz.localize(start_time)
                end_time = start_time + timedelta(minutes=task_data['duration_minutes'])
                
                task = task_manager.create_task(
                    title=task_data['title'],
                    description=task_data['description'],
                    start_time=start_time,
                    end_time=end_time,
                    priority=task_data['priority']
                )
                
                if task_data['completed']:
                    task_manager.complete_task(task.id)
                
            except Exception as e:
                print(f"Ошибка создания задачи для дня {days_ago}: {e}")
        
        print(f"Созданы задачи для {day_date}")
    
    print("Недельные данные созданы!")

if __name__ == "__main__":
    print("=== Создание демонстрационных данных ===")
    
    # Создаем задачи на сегодня
    create_demo_tasks()
    
    # Создаем данные за неделю
    create_weekly_demo_data()
    
    print("\n=== Демонстрационные данные готовы! ===")
    print("Теперь можно запустить приложение и увидеть реальную статистику:")
    print("python hybrid_app.py")
