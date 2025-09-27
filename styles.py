# styles.py - Презентабельные стили
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class PremiumTheme:
    # Цветовая палитра премиум уровня
    COLORS = {
        "dark": {
            "primary": "#0D0D0D",
            "secondary": "#1A1A1A", 
            "tertiary": "#262626",
            "accent": "#FF2B2B",
            "accent_light": "#FF4C4C",
            "accent_dark": "#CC0000",
            "text_primary": "#FFFFFF",
            "text_secondary": "#E0E0E0",
            "text_muted": "#A0A0A0",
            "success": "#00CC88",
            "warning": "#FFAA00",
            "error": "#FF4444",
            "info": "#4488FF"
        },
        "red": {
            "primary": "#1A0000",
            "secondary": "#260000",
            "accent": "#FF2B2B",
            "text_primary": "#FFFFFF"
        }
    }

    @staticmethod
    def get_stylesheet(theme="dark"):
        colors = PremiumTheme.COLORS[theme]
        
        return f"""
/* === ОСНОВНЫЕ СТИЛИ === */
QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors["primary"]}, stop:1 {colors["secondary"]});
    color: {colors["text_primary"]};
    font-family: "Segoe UI", "Inter", sans-serif;
}}

QWidget {{
    background: transparent;
    color: {colors["text_primary"]};
}}

/* === КАРТОЧКИ И ПАНЕЛИ === */
QFrame[frameShape="4"] {{ /* StyledPanel */
    background: {colors["secondary"]};
    border: 1px solid {colors["tertiary"]};
    border-radius: 12px;
    padding: 0px;
}}

QFrame#glass_panel {{
    background: rgba(26, 26, 26, 0.8);
    border: 1px solid rgba(255, 43, 43, 0.3);
    border-radius: 16px;
    backdrop-filter: blur(10px);
}}

/* === КНОПКИ ПРЕМИУМ === */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {colors["accent"]}, stop:1 {colors["accent_dark"]});
    color: {colors["text_primary"]};
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 12px;
    min-height: 40px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {colors["accent_light"]}, stop:1 {colors["accent"]});
    transform: translateY(-1px);
}}

QPushButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {colors["accent_dark"]}, stop:1 {colors["accent"]});
    transform: translateY(0px);
}}

QPushButton:disabled {{
    background: {colors["tertiary"]};
    color: {colors["text_muted"]};
}}

/* Кнопки с иконками */
QPushButton[icon="true"] {{
    padding: 12px;
    min-width: 40px;
}}

/* Вторичные кнопки */
QPushButton.secondary {{
    background: transparent;
    border: 2px solid {colors["accent"]};
    color: {colors["accent"]};
}}

QPushButton.secondary:hover {{
    background: {colors["accent"]};
    color: {colors["text_primary"]};
}}

/* === ПОЛЯ ВВОДА === */
QLineEdit, QTextEdit {{
    background: {colors["tertiary"]};
    color: {colors["text_primary"]};
    border: 2px solid {colors["tertiary"]};
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 12px;
    selection-background-color: {colors["accent"]};
}}

QLineEdit:focus, QTextEdit:focus {{
    border-color: {colors["accent"]};
    background: {colors["secondary"]};
}}

QLineEdit::placeholder, QTextEdit::placeholder {{
    color: {colors["text_muted"]};
}}

/* === МЕНЮ И ПАНЕЛИ ИНСТРУМЕНТОВ === */
QMenuBar {{
    background: transparent;
    color: {colors["text_primary"]};
    border-bottom: 1px solid {colors["tertiary"]};
    padding: 8px;
}}

QMenuBar::item {{
    padding: 8px 16px;
    border-radius: 6px;
    margin: 2px;
}}

QMenuBar::item:selected {{
    background: {colors["accent"]};
}}

QMenu {{
    background: {colors["secondary"]};
    color: {colors["text_primary"]};
    border: 1px solid {colors["tertiary"]};
    border-radius: 8px;
    padding: 8px;
}}

QMenu::item {{
    padding: 8px 24px;
    border-radius: 4px;
    margin: 2px;
}}

QMenu::item:selected {{
    background: {colors["accent"]};
}}

QToolBar {{
    background: {colors["secondary"]};
    border: none;
    spacing: 8px;
    padding: 8px;
}}

/* === ПОЛОСЫ ПРОКРУТКИ === */
QScrollBar:vertical {{
    background: {colors["tertiary"]};
    width: 12px;
    border-radius: 6px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {colors["accent"]};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {colors["accent_light"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* === CHECKBOX & RADIO BUTTON === */
QCheckBox, QRadioButton {{
    color: {colors["text_primary"]};
    spacing: 12px;
}}

QCheckBox::indicator, QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {colors["text_muted"]};
}}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
    background: {colors["accent"]};
    border-color: {colors["accent"]};
}}

QRadioButton::indicator {{
    border-radius: 9px;
}}

QRadioButton::indicator:checked {{
    background: {colors["accent"]};
    border-color: {colors["accent"]};
}}

/* === SLIDER === */
QSlider::groove:horizontal {{
    background: {colors["tertiary"]};
    height: 4px;
    border-radius: 2px;
}}

QSlider::handle:horizontal {{
    background: {colors["accent"]};
    width: 18px;
    height: 18px;
    border-radius: 9px;
    margin: -7px 0;
}}

QSlider::handle:horizontal:hover {{
    background: {colors["accent_light"]};
    width: 20px;
    height: 20px;
}}

/* === PROGRESS BAR === */
QProgressBar {{
    background: {colors["tertiary"]};
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["accent"]}, stop:1 {colors["accent_light"]});
    border-radius: 4px;
}}

/* === GROUP BOX === */
QGroupBox {{
    color: {colors["accent"]};
    font-weight: 600;
    font-size: 14px;
    border: 2px solid {colors["tertiary"]};
    border-radius: 8px;
    margin-top: 20px;
    padding-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    background: {colors["secondary"]};
}}

/* === TAB WIDGET === */
QTabWidget::pane {{
    background: {colors["secondary"]};
    border: 1px solid {colors["tertiary"]};
    border-radius: 8px;
}}

QTabBar::tab {{
    background: {colors["tertiary"]};
    color: {colors["text_secondary"]};
    padding: 8px 16px;
    margin: 2px;
    border-radius: 4px;
}}

QTabBar::tab:selected {{
    background: {colors["accent"]};
    color: {colors["text_primary"]};
}}

QTabBar::tab:hover {{
    background: {colors["accent_light"]};
}}

/* === TOOLTIP === */
QToolTip {{
    background: {colors["secondary"]};
    color: {colors["text_primary"]};
    border: 1px solid {colors["accent"]};
    border-radius: 4px;
    padding: 8px;
}}

/* === CUSTOM CLASSES === */
.TimeBlock {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(255, 43, 67, 0.2), stop:1 rgba(255, 43, 67, 0.1));
    border: 2px solid #FF2B43;
    border-radius: 8px;
    padding: 8px;
}}

.TimeBlock:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(255, 43, 67, 0.3), stop:1 rgba(255, 43, 67, 0.2));
    border-color: #FF4C63;
}}

.TimeScale {{
    background: {colors["secondary"]};
    border-right: 1px solid {colors["tertiary"]};
}}

.StatisticsPanel {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["secondary"]}, stop:1 {colors["tertiary"]});
    border-top: 1px solid {colors["tertiary"]};
    padding: 16px;
}}

/* === АНИМАЦИИ И ЭФФЕКТЫ === */
QPushButton, QLineEdit, QComboBox, QCheckBox {{
    transition: all 0.2s ease;
}}

/* Специальные стили для разных состояний */
.success {{
    color: {colors["success"]};
}}

.warning {{
    color: {colors["warning"]};
}}

.error {{
    color: {colors["error"]};
}}

.info {{
    color: {colors["info"]};
}}

/* Градиентные тексты */
.gradient-text {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["accent"]}, stop:1 {colors["accent_light"]});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
"""

    @staticmethod
    def apply_dark_palette(app):
        """Применяет темную палитру к приложению"""
        palette = QPalette()
        colors = PremiumTheme.COLORS["dark"]
        
        # Устанавливаем цвета палитры
        palette.setColor(QPalette.Window, QColor(colors["primary"]))
        palette.setColor(QPalette.WindowText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.Base, QColor(colors["secondary"]))
        palette.setColor(QPalette.AlternateBase, QColor(colors["tertiary"]))
        palette.setColor(QPalette.ToolTipBase, QColor(colors["secondary"]))
        palette.setColor(QPalette.ToolTipText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.Text, QColor(colors["text_primary"]))
        palette.setColor(QPalette.Button, QColor(colors["tertiary"]))
        palette.setColor(QPalette.ButtonText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.BrightText, QColor(colors["accent"]))
        palette.setColor(QPalette.Link, QColor(colors["accent"]))
        palette.setColor(QPalette.Highlight, QColor(colors["accent"]))
        palette.setColor(QPalette.HighlightedText, QColor(colors["text_primary"]))
        
        app.setPalette(palette)