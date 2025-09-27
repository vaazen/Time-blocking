# animations.py - Современные анимации для PyQt
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup
from PyQt5.QtCore import pyqtProperty, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtGui import QColor

class FadeAnimation:
    """Анимация прозрачности"""
    def __init__(self, widget, duration=300):
        self.widget = widget
        self.effect = QGraphicsOpacityEffect(widget)
        self.widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def fade_in(self):
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
    
    def fade_out(self):
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

class SlideAnimation:
    """Анимация скольжения"""
    def __init__(self, widget, duration=400):
        self.widget = widget
        self.animation = QPropertyAnimation(widget, b"pos")
        self.animation.setDuration(duration)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
    
    def slide_in(self, target_pos):
        start_pos = QPoint(target_pos.x(), target_pos.y() - 50)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(target_pos)
        self.animation.start()
    
    def slide_out(self):
        current_pos = self.widget.pos()
        target_pos = QPoint(current_pos.x(), current_pos.y() - 50)
        self.animation.setStartValue(current_pos)
        self.animation.setEndValue(target_pos)
        self.animation.start()

class ScaleAnimation:
    """Анимация масштабирования"""
    def __init__(self, widget, duration=300):
        self.widget = widget
        self.animation = QPropertyAnimation(widget, b"size")
        self.animation.setDuration(duration)
        self.animation.setEasingCurve(QEasingCurve.OutElastic)
    
    def scale_up(self, factor=1.1):
        original_size = self.widget.size()
        target_size = QSize(int(original_size.width() * factor), 
                           int(original_size.height() * factor))
        self.animation.setStartValue(original_size)
        self.animation.setEndValue(target_size)
        self.animation.start()
    
    def scale_down(self, factor=0.9):
        original_size = self.widget.size()
        target_size = QSize(int(original_size.width() * factor), 
                           int(original_size.height() * factor))
        self.animation.setStartValue(original_size)
        self.animation.setEndValue(target_size)
        self.animation.start()

class ColorAnimation:
    """Анимация изменения цвета"""
    def __init__(self, widget, duration=500):
        self.widget = widget
        self._color = QColor(255, 43, 67)
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(duration)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
    
    @pyqtProperty(QColor)
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self.widget.setStyleSheet(f"background-color: {value.name()};")
    
    def animate_to(self, target_color):
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(target_color)
        self.animation.start()

class PremiumTimeBlockAnimator:
    """Продвинутый аниматор для временных блоков"""
    def __init__(self, time_block):
        self.time_block = time_block
        self.animations = {}
        
        # Создаем анимации
        self.setup_animations()
    
    def setup_animations(self):
        # Группа анимаций для появления
        self.appear_group = QParallelAnimationGroup()
        
        fade_anim = QPropertyAnimation(
            QGraphicsOpacityEffect(self.time_block), b"opacity"
        )
        fade_anim.setDuration(400)
        fade_anim.setStartValue(0.0)
        fade_anim.setEndValue(1.0)
        
        scale_anim = QPropertyAnimation(self.time_block, b"size")
        scale_anim.setDuration(400)
        scale_anim.setEasingCurve(QEasingCurve.OutBack)
        original_size = self.time_block.size()
        scale_anim.setStartValue(QSize(0, 0))
        scale_anim.setEndValue(original_size)
        
        self.appear_group.addAnimation(fade_anim)
        self.appear_group.addAnimation(scale_anim)
        
        # Анимация при наведении
        self.hover_anim = QPropertyAnimation(self.time_block, b"geometry")
        self.hover_anim.setDuration(200)
    
    def animate_appear(self):
        """Анимация появления блока"""
        self.appear_group.start()
    
    def animate_hover_enter(self):
        """Анимация при наведении курсора"""
        rect = self.time_block.geometry()
        self.hover_anim.setStartValue(rect)
        self.hover_anim.setEndValue(rect.adjusted(-2, -2, 2, 2))
        self.hover_anim.start()
    
    def animate_hover_leave(self):
        """Анимация при уходе курсора"""
        rect = self.time_block.geometry()
        self.hover_anim.setStartValue(rect)
        self.hover_anim.setEndValue(rect.adjusted(2, 2, -2, -2))
        self.hover_anim.start()

class NotificationAnimator:
    """Аниматор для уведомлений"""
    @staticmethod
    def show_notification(widget, message, duration=3000):
        """Показывает всплывающее уведомление"""
        # Создаем эффект прозрачности
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        # Анимация появления
        show_anim = QPropertyAnimation(effect, b"opacity")
        show_anim.setDuration(300)
        show_anim.setStartValue(0.0)
        show_anim.setEndValue(1.0)
        
        # Анимация исчезновения
        hide_anim = QPropertyAnimation(effect, b"opacity")
        hide_anim.setDuration(300)
        hide_anim.setStartValue(1.0)
        hide_anim.setEndValue(0.0)
        
        # Группируем анимации
        seq_group = QSequentialAnimationGroup()
        seq_group.addAnimation(show_anim)
        seq_group.addPause(duration)
        seq_group.addAnimation(hide_anim)
        
        seq_group.start()
        
        return seq_group

class RippleEffect:
    """Эффект ряби для кнопок"""
    def __init__(self, button):
        self.button = button
        self.ripple_widget = QWidget(button)
        self.ripple_widget.setStyleSheet("background: rgba(255, 255, 255, 100); border-radius: 50%;")
        self.ripple_widget.hide()
    
    def create_ripple(self, pos):
        """Создает эффект ряби от точки клика"""
        self.ripple_widget.move(pos.x() - 10, pos.y() - 10)
        self.ripple_widget.resize(20, 20)
        self.ripple_widget.show()
        
        # Анимация расширения ряби
        anim = QPropertyAnimation(self.ripple_widget, b"geometry")
        anim.setDuration(600)
        anim.setStartValue(self.ripple_widget.geometry())
        anim.setEndValue(self.ripple_widget.geometry().adjusted(-40, -40, 40, 40))
        
        # Анимация прозрачности
        opacity_effect = QGraphicsOpacityEffect(self.ripple_widget)
        self.ripple_widget.setGraphicsEffect(opacity_effect)
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(600)
        opacity_anim.setStartValue(0.8)
        opacity_anim.setEndValue(0.0)
        
        # Группа анимаций
        group = QParallelAnimationGroup()
        group.addAnimation(anim)
        group.addAnimation(opacity_anim)
        group.finished.connect(self.ripple_widget.hide)
        group.start()

# Декоратор для анимации методов
def animate_method(duration=300, easing=QEasingCurve.OutCubic):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Создаем анимацию перед выполнением метода
            anim = QPropertyAnimation(self, b"geometry")
            anim.setDuration(duration)
            anim.setEasingCurve(easing)
            anim.setStartValue(self.geometry())
            
            # Выполняем оригинальный метод
            result = func(self, *args, **kwargs)
            
            # Устанавливаем конечное значение и запускаем
            anim.setEndValue(self.geometry())
            anim.start()
            
            return result
        return wrapper
    return decorator