# styles.py
BLACK_RED_THEME = {
    "primary": "#1A1A1A",
    "secondary": "#2B2B2B", 
    "accent": "#FF2B2B",
    "accent_light": "#FF4C4C",
    "text_primary": "#FFFFFF",
    "text_secondary": "#CCCCCC",
    "text_muted": "#888888",
    "border": "#FF2B2B",
    "hover": "#FF3333",
    "success": "#00FF00",
    "warning": "#FFFF00",
    "error": "#FF0000",
    
    "time_blocks": [
        "#FF2B2B", "#FF4444", "#FF6B6B", "#FF8B8B",
        "#FF4C4C", "#FF6666", "#FF8C8C", "#FFAAAA"
    ]
}

STYLESHEET = f"""
/* Основные стили */
QMainWindow {{
    background-color: {BLACK_RED_THEME["primary"]};
    color: {BLACK_RED_THEME["text_primary"]};
    font-family: "Segoe UI", "Arial", sans-serif;
}}

QWidget {{
    background-color: {BLACK_RED_THEME["primary"]};
    color: {BLACK_RED_THEME["text_primary"]};
}}

QScrollArea {{
    border: 1px solid {BLACK_RED_THEME["border"]};
    border-radius: 4px;
    background-color: {BLACK_RED_THEME["secondary"]};
}}

QScrollBar:vertical {{
    background: {BLACK_RED_THEME["secondary"]};
    width: 15px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {BLACK_RED_THEME["accent"]};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {BLACK_RED_THEME["hover"]};
}}

/* Кнопки */
QPushButton {{
    background-color: {BLACK_RED_THEME["accent"]};
    color: {BLACK_RED_THEME["text_primary"]};
    border: 2px solid {BLACK_RED_THEME["border"]};
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: {BLACK_RED_THEME["hover"]};
    border-color: {BLACK_RED_THEME["hover"]};
}}

QPushButton:pressed {{
    background-color: {BLACK_RED_THEME["accent_light"]};
}}

QPushButton:disabled {{
    background-color: #555555;
    border-color: #777777;
    color: {BLACK_RED_THEME["text_muted"]};
}}

/* Текстовые поля */
QLineEdit, QTextEdit {{
    background-color: {BLACK_RED_THEME["secondary"]};
    color: {BLACK_RED_THEME["text_primary"]};
    border: 2px solid {BLACK_RED_THEME["border"]};
    padding: 8px;
    border-radius: 4px;
    font-size: 12px;
}}

QLineEdit:focus, QTextEdit:focus {{
    border-color: {BLACK_RED_THEME["accent_light"]};
}}

/* Меню */
QMenuBar {{
    background-color: {BLACK_RED_THEME["primary"]};
    color: {BLACK_RED_THEME["text_primary"]};
    border-bottom: 1px solid {BLACK_RED_THEME["border"]};
}}

QMenuBar::item {{
    padding: 8px 16px;
    background-color: transparent;
}}

QMenuBar::item:selected {{
    background-color: {BLACK_RED_THEME["accent"]};
}}

QMenu {{
    background-color: {BLACK_RED_THEME["secondary"]};
    color: {BLACK_RED_THEME["text_primary"]};
    border: 1px solid {BLACK_RED_THEME["border"]};
}}

QMenu::item {{
    padding: 8px 24px;
}}

QMenu::item:selected {{
    background-color: {BLACK_RED_THEME["accent"]};
}}

/* Диалоги */
QDialog {{
    background-color: {BLACK_RED_THEME["primary"]};
    color: {BLACK_RED_THEME["text_primary"]};
}}

QMessageBox {{
    background-color: {BLACK_RED_THEME["primary"]};
    color: {BLACK_RED_THEME["text_primary"]};
}}

QLabel#title {{
    font-size: 16px;
    font-weight: bold;
    color: {BLACK_RED_THEME["accent"]};
    padding: 10px;
}}

/* Чекбоксы */
QCheckBox {{
    color: {BLACK_RED_THEME["text_primary"]};
    font-size: 12px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
}}

QCheckBox::indicator:unchecked {{
    border: 2px solid {BLACK_RED_THEME["border"]};
    background-color: {BLACK_RED_THEME["secondary"]};
}}

QCheckBox::indicator:checked {{
    border: 2px solid {BLACK_RED_THEME["accent"]};
    background-color: {BLACK_RED_THEME["accent"]};
}}

/* Группы */
QGroupBox {{
    color: {BLACK_RED_THEME["accent"]};
    font-weight: bold;
    border: 2px solid {BLACK_RED_THEME["border"]};
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}}
"""