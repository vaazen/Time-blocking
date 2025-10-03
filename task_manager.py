# task_manager.py - Менеджер задач с реальными данными
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import pytz

class TaskStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Task:
    """Модель задачи"""
    id: str
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    def get_duration_minutes(self) -> int:
        """Получение длительности в минутах"""
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)
    
    def get_duration_hours(self) -> float:
        """Получение длительности в часах"""
        return self.get_duration_minutes() / 60
    
    def is_active_now(self, moscow_time: datetime) -> bool:
        """Проверка, активна ли задача сейчас"""
        return self.start_time <= moscow_time <= self.end_time
    
    def is_overdue(self, moscow_time: datetime) -> bool:
        """Проверка, просрочена ли задача"""
        return moscow_time > self.end_time and self.status != TaskStatus.COMPLETED
    
    def mark_completed(self, moscow_time: datetime):
        """Отметить как выполненную"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = moscow_time
        self.updated_at = moscow_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        data = asdict(self)
        # Преобразуем datetime в строки
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, (TaskStatus, TaskPriority)):
                data[key] = value.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Создание из словаря"""
        # Преобразуем строки обратно в datetime
        for key in ['start_time', 'end_time', 'created_at', 'updated_at']:
            if key in data and data[key]:
                data[key] = datetime.fromisoformat(data[key])
        
        if 'completed_at' in data and data['completed_at']:
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        
        # Преобразуем enum'ы
        if 'priority' in data:
            data['priority'] = TaskPriority(data['priority'])
        if 'status' in data:
            data['status'] = TaskStatus(data['status'])
        
        return cls(**data)

class TaskManager:
    """Менеджер задач"""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.data_file = "tasks_data.json"
        self.moscow_tz = pytz.timezone('Europe/Moscow')
        self.load_tasks()
    
    def get_moscow_time(self) -> datetime:
        """Получение московского времени"""
        return datetime.now(self.moscow_tz)
    
    def create_task(self, title: str, description: str, start_time: datetime, 
                   end_time: datetime, priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        """Создание новой задачи"""
        moscow_time = self.get_moscow_time()
        
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            priority=priority,
            status=TaskStatus.PLANNED,
            created_at=moscow_time,
            updated_at=moscow_time
        )
        
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Обновление задачи"""
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        
        moscow_time = self.get_moscow_time()
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = moscow_time
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Удаление задачи"""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False
    
    def complete_task(self, task_id: str) -> Optional[Task]:
        """Завершение задачи"""
        task = self.get_task_by_id(task_id)
        if task:
            moscow_time = self.get_moscow_time()
            task.mark_completed(moscow_time)
            self.save_tasks()
            return task
        return None
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Получение задачи по ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_for_today(self) -> List[Task]:
        """Получение задач на сегодня"""
        moscow_time = self.get_moscow_time()
        today = moscow_time.date()
        
        return [
            task for task in self.tasks
            if task.start_time.date() == today
        ]
    
    def get_active_task(self) -> Optional[Task]:
        """Получение текущей активной задачи"""
        moscow_time = self.get_moscow_time()
        
        for task in self.tasks:
            if task.is_active_now(moscow_time) and task.status == TaskStatus.IN_PROGRESS:
                return task
        
        return None
    
    def get_completed_tasks_today(self) -> List[Task]:
        """Получение выполненных задач за сегодня"""
        today_tasks = self.get_tasks_for_today()
        return [task for task in today_tasks if task.status == TaskStatus.COMPLETED]
    
    def get_pending_tasks_today(self) -> List[Task]:
        """Получение невыполненных задач за сегодня"""
        today_tasks = self.get_tasks_for_today()
        return [task for task in today_tasks if task.status in [TaskStatus.PLANNED, TaskStatus.IN_PROGRESS]]
    
    def calculate_productivity_today(self) -> Dict[str, Any]:
        """Расчет продуктивности за сегодня"""
        today_tasks = self.get_tasks_for_today()
        completed_tasks = self.get_completed_tasks_today()
        
        if not today_tasks:
            return {
                'productivity_percent': 0,
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'total_time_planned': 0,
                'total_time_completed': 0,
                'efficiency': 0
            }
        
        total_planned_minutes = sum(task.get_duration_minutes() for task in today_tasks)
        completed_minutes = sum(task.get_duration_minutes() for task in completed_tasks)
        
        productivity_percent = (len(completed_tasks) / len(today_tasks)) * 100
        efficiency = (completed_minutes / total_planned_minutes) * 100 if total_planned_minutes > 0 else 0
        
        return {
            'productivity_percent': round(productivity_percent, 1),
            'total_tasks': len(today_tasks),
            'completed_tasks': len(completed_tasks),
            'pending_tasks': len(today_tasks) - len(completed_tasks),
            'total_time_planned': total_planned_minutes,
            'total_time_completed': completed_minutes,
            'efficiency': round(efficiency, 1)
        }
    
    def get_weekly_stats(self) -> List[Dict[str, Any]]:
        """Получение статистики за неделю"""
        moscow_time = self.get_moscow_time()
        stats = []
        
        for i in range(7):
            day = moscow_time - timedelta(days=i)
            day_tasks = [
                task for task in self.tasks
                if task.start_time.date() == day.date()
            ]
            
            completed = [task for task in day_tasks if task.status == TaskStatus.COMPLETED]
            productivity = (len(completed) / len(day_tasks)) * 100 if day_tasks else 0
            
            stats.append({
                'date': day.date().isoformat(),
                'day_name': day.strftime('%a'),
                'total_tasks': len(day_tasks),
                'completed_tasks': len(completed),
                'productivity': round(productivity, 1)
            })
        
        return list(reversed(stats))  # От понедельника к воскресенью
    
    def save_tasks(self):
        """Сохранение задач в файл"""
        try:
            data = {
                'tasks': [task.to_dict() for task in self.tasks],
                'saved_at': self.get_moscow_time().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения задач: {e}")
    
    def load_tasks(self):
        """Загрузка задач из файла"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.tasks = []
                for task_data in data.get('tasks', []):
                    try:
                        task = Task.from_dict(task_data)
                        self.tasks.append(task)
                    except Exception as e:
                        print(f"Ошибка загрузки задачи: {e}")
        except Exception as e:
            print(f"Ошибка загрузки файла задач: {e}")
            self.tasks = []

# Глобальный экземпляр
task_manager = TaskManager()
