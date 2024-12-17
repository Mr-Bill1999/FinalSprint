from itertools import product

from PyQt5.QtWidgets import (QApplication,QMainWindow,QPushButton,QVBoxLayout,QWidget,
    QHBoxLayout,QLabel,QLineEdit,QSizePolicy,QGridLayout,QSpacerItem, QDialog)
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap, QPen
import sys
from PathTool import resource_path
from CenterFrame import DynamicButtonWidget
from TemperatureTemplate import TemperatureWidget
import random

class MachineWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


        # Флаг для перетаскивания окна
        self._is_dragging = False
        self._drag_start_position = QPoint()

        # Основной виджет
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: #20273E;
                border-radius: 10px;
            }
        """)

        # Заголовок окна
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)

        # Кнопка закрытия
        btn_close = QPushButton()
        btn_close.setStyleSheet('background:transparent;')
        btn_close.setIcon(QIcon('assets/exit.png'))
        btn_close.setIconSize(QSize(16, 16))
        btn_close.clicked.connect(self.close)

        # Layout заголовка
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(5, 5, 5, 5)
        title_layout.addStretch()
        title_layout.addWidget(btn_close)

        self.title_bar.setLayout(title_layout)

        # Основной layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.central_widget)

        # Тестовый layout для содержимого
        content_layout = QVBoxLayout(self.central_widget)
        content_layout.setSpacing(0)

        # Поле ID
        self.id_label = QLabel("ID:")
        self.id_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF; font-family: Gilroy;")
        self.id_line_edit = QLineEdit()
        self.id_line_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2E364E;
                font-size: 18px;
                font-family: Gilroy;
                color: #FFFFFF;
                border: 1px solid #3C445C;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
            }
        """)
        content_layout.addWidget(self.id_label)
        content_layout.addWidget(self.id_line_edit)

        # Поле Product ID
        self.product_id_label = QLabel("Product ID:")
        self.product_id_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF; font-family: Gilroy;")
        self.product_id_line_edit = QLineEdit()
        self.product_id_line_edit.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                font-family: Gilroy;
                background-color: #2E364E;
                color: #FFFFFF;
                border: 1px solid #3C445C;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
            }
        """)
        content_layout.addWidget(self.product_id_label)
        content_layout.addWidget(self.product_id_line_edit)

        # Поле Type
        self.type_label = QLabel("Type:")
        self.type_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF; font-family: Gilroy;")
        self.type_line_edit = QLineEdit()
        self.type_line_edit.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                font-family: Gilroy;
                background-color: #2E364E;
                color: #FFFFFF;
                border: 1px solid #3C445C;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
            }
        """)
        content_layout.addWidget(self.type_label)
        content_layout.addWidget(self.type_line_edit)
        self.generate_random_values()

        # Кнопка в конце
        self.submit_button = QPushButton("Add new machine")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #20273E;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-family: Gilroy;
            }
            QPushButton:hover {
                background-color: #20273E;
                color: #FFFFFF;
            }
        """)
        content_layout.setSpacing(10)
        content_layout.addStretch()
        content_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.add_machine_widget)

        self.setFixedSize(400, 600)

    def add_machine_widget(self):
        """
        Добавляет новый виджет в central_area из CustomMainWindow.
        """
        if self.parent.central_area:
            machine_id = self.id_line_edit.text()
            type = self.type_line_edit.text()
            product_id = self.product_id_line_edit.text()
            new_widget = TemperatureWidget(int(machine_id),product_id,type)
            self.parent.central_area.add_widget(new_widget)
        self.close()


    def paintEvent(self, event):
        """
        Отрисовка фона с закруглёнными углами и обводкой.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Обводка
        border_color = QColor(255, 255, 255)
        border_width = 2

        pen = QPen(border_color)
        pen.setWidth(border_width)
        painter.setPen(pen)

        rect = self.rect().adjusted(border_width // 2, border_width // 2, -border_width // 2, -border_width // 2)
        painter.drawRoundedRect(rect, 10, 10)

        # Фон
        painter.setBrush(QColor(32, 39, 62))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 10, 10)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_in_title_bar(event.pos()):
            self._is_dragging = True
            self._drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self.move(event.globalPos() - self._drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            event.accept()

    def is_in_title_bar(self, pos):
        """Проверяет, находится ли курсор в области заголовка."""
        return 0 <= pos.y() <= self.title_bar.height()

    def generate_random_values(self):
        """
        Генерация случайных данных для ID, Product ID и Type.
        """
        random_id = f"{random.randint(10000000, 99999999)}"  # Рандомное 8-значное число
        random_letter = random.choice(['L', 'H', 'M'])  # Случайная буква
        random_product_id = f"{random_letter}{random.randint(10000000, 99999999)}"  # Буква + 8 цифр

        # Заполнение полей
        self.id_line_edit.setText(random_id)
        self.product_id_line_edit.setText(random_product_id)
        self.type_line_edit.setText(random_letter)  # Буква из Product ID





class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_maximized = False
        self.expanded = False

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: #20273E;
                border-radius: 10px;
            }
        """)
        self.setCentralWidget(self.central_widget)
        self._is_dragging = False
        self._drag_start_position = QPoint()
        self.setMinimumSize(1200, 900)
        self.setup_window_controls()
        self.resize(1200, 900)

    def setup_window_controls(self):
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)

        btn_minimize = QPushButton()
        icon_path = resource_path('assets/minimize.png')
        btn_minimize.setIcon(QIcon(icon_path))
        btn_minimize.setFixedSize(30, 30)
        btn_minimize.clicked.connect(self.showMinimized)

        self.btn_restore = QPushButton()
        self.btn_restore.setFixedSize(30, 30)
        icon_path = resource_path('assets/resize.png')
        self.btn_restore.setIcon(QIcon(icon_path))
        self.btn_restore.clicked.connect(self.toggle_restore)

        btn_close = QPushButton()
        btn_close.setFixedSize(30, 30)
        icon_path = resource_path('assets/exit.png')
        btn_close.setIcon(QIcon(icon_path))
        btn_close.clicked.connect(self.close)

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addStretch()
        layout.addWidget(btn_minimize)
        layout.addWidget(self.btn_restore)
        layout.addWidget(btn_close)

        self.title_bar.setLayout(layout)

        self.machine_button = QPushButton()
        self.machine_button.setIcon(QIcon('assets/add.png'))
        self.machine_button.setIconSize(QSize(150,30))
        self.machine_button.clicked.connect(self.open_machine_window)

        self.central_area = DynamicButtonWidget()

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 0, 10, 10)
        main_layout.setSpacing(15)

        main_layout.addWidget(self.title_bar, alignment=Qt.AlignTop | Qt.AlignRight)
        main_layout.addWidget(self.central_area)
        main_layout.addWidget(self.machine_button, alignment=Qt.AlignCenter)


    def toggle_restore(self):
        if self.isMaximized():
            self.showNormal()
            self.is_maximized = False
            icon_path = resource_path('assets/resize.png')
            self.btn_restore.setIcon(QIcon(icon_path))
        else:
            self.showMaximized()
            self.is_maximized = True
            icon_path = resource_path('assets/resize2.png')
            self.btn_restore.setIcon(QIcon(icon_path))

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def side_bar_show(self,obj):
        if self.side_widget.isVisible():
            self.side_widget.update_form(obj)
            self.side_widget.hide()
        else:
            self.side_widget.show()
            self.side_widget.update_form(obj)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)

    def open_machine_window(self):
        """
        Открывает новое окно (MachineWindow).
        """
        self.machine_window = MachineWindow(self)
        self.machine_window.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_in_title_bar(event.pos()):
            self._is_dragging = True
            self._drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self.move(event.globalPos() - self._drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            event.accept()

    def is_in_title_bar(self, pos):
        """Проверяет, находится ли курсор в области заголовка."""
        return 0 <= pos.y() <= self.title_bar.height()




app = QApplication(sys.argv)
window = CustomMainWindow()
window.show()
sys.exit(app.exec_())
