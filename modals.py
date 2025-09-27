from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTimeEdit, QComboBox,
                             QMessageBox)
from PyQt5.QtCore import Qt, QTime

class EditBlockModal(QDialog):
    def __init__(self, parent=None, block_data=None):
        super().__init__(parent)
        self.block_data = block_data or {}
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Редактировать блок")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        # Название блока
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        self.name_input.setText(self.block_data.get('name', ''))
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Время начала
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Начало:"))
        self.start_time = QTimeEdit()
        start_time = self.block_data.get('start_time', QTime(9, 0))
        if isinstance(start_time, str):
            start_time = QTime.fromString(start_time, 'hh:mm')
        self.start_time.setTime(start_time)
        start_layout.addWidget(self.start_time)
        layout.addLayout(start_layout)
        
        # Время окончания
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("Окончание:"))
        self.end_time = QTimeEdit()
        end_time = self.block_data.get('end_time', QTime(10, 0))
        if isinstance(end_time, str):
            end_time = QTime.fromString(end_time, 'hh:mm')
        self.end_time.setTime(end_time)
        end_layout.addWidget(self.end_time)
        layout.addLayout(end_layout)
        
        # Цвет
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Цвет:"))
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Красный", "Синий", "Зеленый", "Желтый", "Фиолетовый"])
        self.color_combo.setCurrentText(self.block_data.get('color', 'Красный'))
        color_layout.addWidget(self.color_combo)
        layout.addLayout(color_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название блока")
            return
            
        self.block_data = {
            'name': self.name_input.text(),
            'start_time': self.start_time.time().toString('hh:mm'),
            'end_time': self.end_time.time().toString('hh:mm'),
            'color': self.color_combo.currentText()
        }
        self.accept()

class ConfirmModal(QDialog):
    def __init__(self, parent=None, message="Вы уверены?"):
        super().__init__(parent)
        self.setup_ui(message)
        
    def setup_ui(self, message):
        self.setWindowTitle("Подтверждение")
        self.setFixedSize(250, 100)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        
        button_layout = QHBoxLayout()
        yes_btn = QPushButton("Да")
        yes_btn.clicked.connect(self.accept)
        no_btn = QPushButton("Нет")
        no_btn.clicked.connect(self.reject)
        button_layout.addWidget(yes_btn)
        button_layout.addWidget(no_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

# Добавьте другие модальные окна по мере необходимости