# localization_system.py - Система локализации с поддержкой русского, английского и немецкого
import json
import os
from typing import Dict, Any
from datetime import datetime
import pytz

class LocalizationManager:
    """Менеджер локализации для многоязычного интерфейса"""
    
    def __init__(self):
        self.current_language = "ru"
        self.supported_languages = {
            "ru": "Русский",
            "en": "English", 
            "de": "Deutsch"
        }
        self.translations = self.load_translations()
        
        # Московская временная зона
        self.moscow_tz = pytz.timezone('Europe/Moscow')
    
    def load_translations(self) -> Dict[str, Dict[str, str]]:
        """Загрузка переводов для всех языков"""
        return {
            "ru": {
                # Основной интерфейс
                "app_title": "Гибридный планировщик времени",
                "add_task": "Добавить задачу",
                "task_name": "Название задачи",
                "start_time": "Время начала",
                "end_time": "Время окончания",
                "description": "Описание",
                "priority": "Приоритет",
                "status": "Статус",
                "save": "Сохранить",
                "cancel": "Отмена",
                "delete": "Удалить",
                "edit": "Редактировать",
                "complete": "Завершить",
                
                # Статусы задач
                "status_planned": "Запланировано",
                "status_in_progress": "В процессе",
                "status_completed": "Завершено",
                "status_cancelled": "Отменено",
                
                # Приоритеты
                "priority_low": "Низкий",
                "priority_medium": "Средний", 
                "priority_high": "Высокий",
                "priority_urgent": "Срочный",
                
                # Dashboard
                "dashboard": "Панель управления",
                "productivity": "Продуктивность",
                "tasks_today": "Задач сегодня",
                "time_spent": "Затрачено времени",
                "completed_tasks": "Выполнено задач",
                "pending_tasks": "В ожидании",
                "efficiency": "Эффективность",
                "weekly_stats": "Статистика недели",
                
                # Время
                "moscow_time": "Московское время",
                "current_time": "Текущее время",
                "today": "Сегодня",
                "this_week": "На этой неделе",
                "hours": "часов",
                "minutes": "минут",
                "seconds": "секунд",
                
                # Сообщения
                "task_added": "Задача добавлена",
                "task_completed": "Задача выполнена",
                "task_deleted": "Задача удалена",
                "no_tasks": "Нет задач на сегодня",
                "add_first_task": "Добавьте первую задачу",
                
                # Кнопки и действия
                "process_rust": "Обработать (Rust)",
                "calculate_cpp": "Рассчитать (C++)",
                "performance_test": "Тест производительности",
                "language": "Язык",
                "settings": "Настройки",
                
                # Вкладки
                "tab_dashboard": "Панель",
                "tab_tasks": "Задачи", 
                "tab_performance": "Производительность"
            },
            
            "en": {
                # Main interface
                "app_title": "Hybrid Time Planner",
                "add_task": "Add Task",
                "task_name": "Task Name",
                "start_time": "Start Time",
                "end_time": "End Time",
                "description": "Description",
                "priority": "Priority",
                "status": "Status",
                "save": "Save",
                "cancel": "Cancel",
                "delete": "Delete",
                "edit": "Edit",
                "complete": "Complete",
                
                # Task statuses
                "status_planned": "Planned",
                "status_in_progress": "In Progress",
                "status_completed": "Completed",
                "status_cancelled": "Cancelled",
                
                # Priorities
                "priority_low": "Low",
                "priority_medium": "Medium",
                "priority_high": "High", 
                "priority_urgent": "Urgent",
                
                # Dashboard
                "dashboard": "Dashboard",
                "productivity": "Productivity",
                "tasks_today": "Tasks Today",
                "time_spent": "Time Spent",
                "completed_tasks": "Completed",
                "pending_tasks": "Pending",
                "efficiency": "Efficiency",
                "weekly_stats": "Weekly Stats",
                
                # Time
                "moscow_time": "Moscow Time",
                "current_time": "Current Time",
                "today": "Today",
                "this_week": "This Week",
                "hours": "hours",
                "minutes": "minutes",
                "seconds": "seconds",
                
                # Messages
                "task_added": "Task added",
                "task_completed": "Task completed",
                "task_deleted": "Task deleted",
                "no_tasks": "No tasks for today",
                "add_first_task": "Add your first task",
                
                # Buttons and actions
                "process_rust": "Process (Rust)",
                "calculate_cpp": "Calculate (C++)",
                "performance_test": "Performance Test",
                "language": "Language",
                "settings": "Settings",
                
                # Tabs
                "tab_dashboard": "Dashboard",
                "tab_tasks": "Tasks",
                "tab_performance": "Performance"
            },
            
            "de": {
                # Hauptschnittstelle
                "app_title": "Hybrid-Zeitplaner",
                "add_task": "Aufgabe hinzufügen",
                "task_name": "Aufgabenname",
                "start_time": "Startzeit",
                "end_time": "Endzeit",
                "description": "Beschreibung",
                "priority": "Priorität",
                "status": "Status",
                "save": "Speichern",
                "cancel": "Abbrechen",
                "delete": "Löschen",
                "edit": "Bearbeiten",
                "complete": "Abschließen",
                
                # Aufgabenstatus
                "status_planned": "Geplant",
                "status_in_progress": "In Bearbeitung",
                "status_completed": "Abgeschlossen",
                "status_cancelled": "Abgebrochen",
                
                # Prioritäten
                "priority_low": "Niedrig",
                "priority_medium": "Mittel",
                "priority_high": "Hoch",
                "priority_urgent": "Dringend",
                
                # Dashboard
                "dashboard": "Dashboard",
                "productivity": "Produktivität",
                "tasks_today": "Aufgaben heute",
                "time_spent": "Aufgewendete Zeit",
                "completed_tasks": "Abgeschlossen",
                "pending_tasks": "Ausstehend",
                "efficiency": "Effizienz",
                "weekly_stats": "Wochenstatistik",
                
                # Zeit
                "moscow_time": "Moskauer Zeit",
                "current_time": "Aktuelle Zeit",
                "today": "Heute",
                "this_week": "Diese Woche",
                "hours": "Stunden",
                "minutes": "Minuten",
                "seconds": "Sekunden",
                
                # Nachrichten
                "task_added": "Aufgabe hinzugefügt",
                "task_completed": "Aufgabe abgeschlossen",
                "task_deleted": "Aufgabe gelöscht",
                "no_tasks": "Keine Aufgaben für heute",
                "add_first_task": "Erste Aufgabe hinzufügen",
                
                # Schaltflächen und Aktionen
                "process_rust": "Verarbeiten (Rust)",
                "calculate_cpp": "Berechnen (C++)",
                "performance_test": "Leistungstest",
                "language": "Sprache",
                "settings": "Einstellungen",
                
                # Registerkarten
                "tab_dashboard": "Dashboard",
                "tab_tasks": "Aufgaben",
                "tab_performance": "Leistung"
            }
        }
    
    def get_text(self, key: str, *args) -> str:
        """Получение переведенного текста"""
        translation = self.translations.get(self.current_language, {})
        text = translation.get(key, key)
        
        # Форматирование с аргументами
        if args:
            try:
                text = text.format(*args)
            except:
                pass
        
        return text
    
    def set_language(self, lang_code: str) -> bool:
        """Установка языка"""
        if lang_code in self.supported_languages:
            self.current_language = lang_code
            return True
        return False
    
    def get_moscow_time(self) -> datetime:
        """Получение московского времени"""
        return datetime.now(self.moscow_tz)
    
    def format_moscow_time(self, format_str: str = "%H:%M:%S") -> str:
        """Форматирование московского времени"""
        return self.get_moscow_time().strftime(format_str)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Получение поддерживаемых языков"""
        return self.supported_languages.copy()

# Глобальный экземпляр
localization = LocalizationManager()

def _(key: str, *args) -> str:
    """Короткая функция для получения перевода"""
    return localization.get_text(key, *args)
