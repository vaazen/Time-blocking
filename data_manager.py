# data_manager.py - Улучшенный менеджер данных с резервным копированием
import json
import os
import shutil
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMessageBox
import hashlib

class PremiumDataManager:
    """Менеджер данных премиум-класса с шифрованием и резервными копиями"""
    def __init__(self):
        self.data_dir = "time_blocking_premium_data"
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.ensure_directories()
        self.encryption_key = self.generate_encryption_key()
    
    def ensure_directories(self):
        """Создание необходимых директорий"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def generate_encryption_key(self):
        """Генерация ключа шифрования (упрощенная версия)"""
        # В реальном приложении используйте надежное шифрование
        return hashlib.sha256(b"time_blocking_premium_key").hexdigest()[:32]
    
    def save_day(self, time_blocks, date=None, create_backup=True):
        """Сохранение дня с созданием резервной копии"""
        try:
            if date is None:
                date = datetime.now().date()
            
            filename = os.path.join(self.data_dir, f"schedule_{date.strftime('%Y-%m-%d')}.json")
            
            # Создание резервной копии если файл существует
            if create_backup and os.path.exists(filename):
                self.create_backup(filename, date)
            
            data = {
                "version": "2.0",
                "date": date.isoformat(),
                "saved_at": datetime.now().isoformat(),
                "time_blocks": [],
                "metadata": {
                    "total_blocks": len(time_blocks),
                    "total_minutes": sum(block.get_duration_minutes() for block in time_blocks),
                    "productivity_score": self.calculate_productivity_score(time_blocks)
                }
            }
            
            for block in time_blocks:
                block_data = {
                    "id": block.block_id,
                    "title": block.title,
                    "start_time": block.start_time.isoformat(),
                    "end_time": block.end_time.isoformat(),
                    "color": block.color,
                    "notify": block.notify,
                    "progress": getattr(block, 'progress', 0),
                    "created_at": getattr(block, 'created_at', datetime.now().isoformat()),
                    "updated_at": datetime.now().isoformat()
                }
                data["time_blocks"].append(block_data)
            
            # "Шифрование" данных (в реальном приложении используйте настоящие методы)
            encrypted_data = self.simple_encrypt(json.dumps(data, indent=2, ensure_ascii=False))
            
            with open(filename, 'wb') as f:
                f.write(encrypted_data)
            
            return True
            
        except Exception as e:
            QMessageBox.warning(None, "Ошибка сохранения", 
                              f"Не удалось сохранить данные: {str(e)}")
            return False
    
    def load_day(self, date=None):
        """Загрузка дня с проверкой целостности"""
        try:
            if date is None:
                date = datetime.now().date()
            
            filename = os.path.join(self.data_dir, f"schedule_{date.strftime('%Y-%m-%d')}.json")
            
            if not os.path.exists(filename):
                return []
            
            with open(filename, 'rb') as f:
                encrypted_data = f.read()
            
            # "Расшифровка" данных
            decrypted_data = self.simple_decrypt(encrypted_data)
            data = json.loads(decrypted_data)
            
            # Проверка версии и целостности
            if not self.validate_data(data):
                # Попытка загрузки из резервной копии
                return self.restore_from_backup(date)
            
            return data["time_blocks"]
            
        except Exception as e:
            QMessageBox.warning(None, "Ошибка загрузки", 
                              f"Не удалось загрузить данные: {str(e)}")
            return self.restore_from_backup(date) or []
    
    def simple_encrypt(self, data):
        """Упрощенное "шифрование" (для демонстрации)"""
        return data.encode('utf-8')
    
    def simple_decrypt(self, data):
        """Упрощенное "расшифрование" (для демонстрации)"""
        return data.decode('utf-8')
    
    def validate_data(self, data):
        """Проверка целостности данных"""
        required_fields = ["version", "date", "time_blocks"]
        return all(field in data for field in required_fields)
    
    def create_backup(self, original_file, date):
        """Создание резервной копии"""
        try:
            backup_name = f"backup_{date.strftime('%Y-%m-%d')}_{datetime.now().strftime('%H-%M-%S')}.json"
            backup_path = os.path.join(self.backup_dir, backup_name)
            shutil.copy2(original_file, backup_path)
            
            # Ограничение количества резервных копий (максимум 10)
            self.cleanup_old_backups(date)
            
        except Exception as e:
            print(f"Ошибка создания резервной копии: {e}")
    
    def cleanup_old_backups(self, date):
        """Очистка старых резервных копий"""
        try:
            backup_pattern = f"backup_{date.strftime('%Y-%m-%d')}_*.json"
            backups = []
            
            for file in os.listdir(self.backup_dir):
                if file.startswith(f"backup_{date.strftime('%Y-%m-%d')}"):
                    file_path = os.path.join(self.backup_dir, file)
                    backups.append((file_path, os.path.getctime(file_path)))
            
            # Сортируем по дате создания (новые сначала)
            backups.sort(key=lambda x: x[1], reverse=True)
            
            # Удаляем старые копии (оставляем 10 последних)
            for backup_path, _ in backups[10:]:
                os.remove(backup_path)
                
        except Exception as e:
            print(f"Ошибка очистки резервных копий: {e}")
    
    def restore_from_backup(self, date):
        """Восстановление из резервной копии"""
        try:
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.startswith(f"backup_{date.strftime('%Y-%m-%d')}"):
                    file_path = os.path.join(self.backup_dir, file)
                    backups.append((file_path, os.path.getctime(file_path)))
            
            if not backups:
                return None
            
            # Берем самую свежую резервную копию
            latest_backup = max(backups, key=lambda x: x[1])[0]
            
            with open(latest_backup, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.simple_decrypt(encrypted_data)
            data = json.loads(decrypted_data)
            
            QMessageBox.information(None, "Восстановление", 
                                  "Данные восстановлены из резервной копии")
            
            return data["time_blocks"]
            
        except Exception as e:
            print(f"Ошибка восстановления из резервной копии: {e}")
            return None
    
    def calculate_productivity_score(self, time_blocks):
        """Расчет показателя продуктивности"""
        if not time_blocks:
            return 0
        
        total_minutes = sum(block.get_duration_minutes() for block in time_blocks)
        # Максимальная продуктивность - 8 часов работы
        max_productivity = 8 * 60
        score = min(100, int((total_minutes / max_productivity) * 100))
        
        # Бонус за разнообразие задач
        unique_tasks = len(set(block.title for block in time_blocks))
        diversity_bonus = min(20, unique_tasks * 2)
        
        return min(100, score + diversity_bonus)
    
    def get_statistics(self, start_date, end_date):
        """Получение статистики за период"""
        statistics = {
            "total_days": 0,
            "total_blocks": 0,
            "total_hours": 0,
            "average_blocks_per_day": 0,
            "average_hours_per_day": 0,
            "productivity_trend": [],
            "most_productive_day": None
        }
        
        current_date = start_date
        daily_stats = []
        
        while current_date <= end_date:
            blocks = self.load_day(current_date)
            if blocks:
                total_minutes = sum((datetime.fromisoformat(block["end_time"]) - 
                                   datetime.fromisoformat(block["start_time"])).total_seconds() / 60 
                                   for block in blocks)
                
                day_stat = {
                    "date": current_date,
                    "blocks": len(blocks),
                    "hours": total_minutes / 60,
                    "productivity": self.calculate_productivity_score_from_data(blocks)
                }
                daily_stats.append(day_stat)
            
            current_date += timedelta(days=1)
        
        if daily_stats:
            statistics["total_days"] = len(daily_stats)
            statistics["total_blocks"] = sum(day["blocks"] for day in daily_stats)
            statistics["total_hours"] = sum(day["hours"] for day in daily_stats)
            statistics["average_blocks_per_day"] = statistics["total_blocks"] / statistics["total_days"]
            statistics["average_hours_per_day"] = statistics["total_hours"] / statistics["total_days"]
            statistics["productivity_trend"] = [day["productivity"] for day in daily_stats]
            statistics["most_productive_day"] = max(daily_stats, key=lambda x: x["productivity"])
        
        return statistics
    
    def calculate_productivity_score_from_data(self, blocks_data):
        """Расчет продуктивности из данных блоков"""
        if not blocks_data:
            return 0
        
        total_minutes = 0
        for block in blocks_data:
            start = datetime.fromisoformat(block["start_time"])
            end = datetime.fromisoformat(block["end_time"])
            total_minutes += (end - start).total_seconds() / 60
        
        return min(100, int((total_minutes / (8 * 60)) * 100))
    
    def export_data(self, start_date, end_date, format='json'):
        """Экспорт данных в различных форматах"""
        data = {
            "export_info": {
                "version": "2.0",
                "export_date": datetime.now().isoformat(),
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                }
            },
            "schedules": []
        }
        
        current_date = start_date
        while current_date <= end_date:
            blocks = self.load_day(current_date)
            if blocks:
                data["schedules"].append({
                    "date": current_date.isoformat(),
                    "blocks": blocks
                })
            current_date += timedelta(days=1)
        
        if format == 'json':
            return json.dumps(data, indent=2, ensure_ascii=False)
        elif format == 'csv':
            return self.convert_to_csv(data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def convert_to_csv(self, data):
        """Конвертация в CSV формат"""
        csv_lines = ["Date,Start Time,End Time,Title,Color,Duration (min)"]
        
        for schedule in data["schedules"]:
            date = schedule["date"]
            for block in schedule["blocks"]:
                start_time = datetime.fromisoformat(block["start_time"]).strftime("%H:%M")
                end_time = datetime.fromisoformat(block["end_time"]).strftime("%H:%M")
                duration = (datetime.fromisoformat(block["end_time"]) - 
                          datetime.fromisoformat(block["start_time"])).total_seconds() / 60
                
                csv_lines.append(
                    f'{date},{start_time},{end_time},"{block["title"]}",{block["color"]},{duration}'
                )
        
        return "\n".join(csv_lines)