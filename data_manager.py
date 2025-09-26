# data_manager.py
import json
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMessageBox

class DataManager:
    def __init__(self):
        self.data_dir = "time_blocking_data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_day(self, time_blocks, date=None):
        """Сохраняет расписание дня в JSON файл"""
        try:
            if date is None:
                date = datetime.now().date()
            
            filename = os.path.join(self.data_dir, f"schedule_{date.strftime('%Y-%m-%d')}.json")
            
            data = {
                "date": date.isoformat(),
                "created": datetime.now().isoformat(),
                "time_blocks": []
            }
            
            for block in time_blocks:
                block_data = {
                    "start_time": block.start_time.isoformat(),
                    "end_time": block.end_time.isoformat(),
                    "title": block.title,
                    "color": block.color,
                    "notify": block.notify
                }
                data["time_blocks"].append(block_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            QMessageBox.warning(None, "Ошибка сохранения", f"Не удалось сохранить данные: {str(e)}")
            return False
    
    def load_day(self, date=None):
        """Загружает расписание дня из JSON файла"""
        try:
            if date is None:
                date = datetime.now().date()
            
            filename = os.path.join(self.data_dir, f"schedule_{date.strftime('%Y-%m-%d')}.json")
            
            if not os.path.exists(filename):
                return []
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data["time_blocks"]
            
        except Exception as e:
            QMessageBox.warning(None, "Ошибка загрузки", f"Не удалось загрузить данные: {str(e)}")
            return []
    
    def get_saved_dates(self):
        """Возвращает список дат, для которых есть сохраненные данные"""
        try:
            dates = []
            for filename in os.listdir(self.data_dir):
                if filename.startswith("schedule_") and filename.endswith(".json"):
                    date_str = filename[9:19]  # format: schedule_YYYY-MM-DD.json
                    dates.append(datetime.strptime(date_str, "%Y-%m-%d").date())
            return sorted(dates)
        except:
            return []
    
    def export_to_json(self, time_blocks, filename):
        """Экспортирует данные в выбранный файл"""
        return self.save_day(time_blocks, datetime.now().date())
    
    def import_from_json(self, filename):
        """Импортирует данные из выбранного файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("time_blocks", [])
        except Exception as e:
            QMessageBox.warning(None, "Ошибка импорта", f"Не удалось импортировать данные: {str(e)}")
            return []