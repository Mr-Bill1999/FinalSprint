from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFrame, QScrollArea,
    QSpacerItem, QSizePolicy, QGridLayout, QPushButton
)
from PyQt5.QtCore import Qt
from TemperatureTemplate import TemperatureWidget


class DynamicButtonWidget(QWidget):
    def __init__(self, parent_widget=None):
        super().__init__(parent=parent_widget)

        self.parent_widget = parent_widget
        self.temp_list = []

        # Основной layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Обёртка для ScrollArea
        self.scroll_area_wrapper = QFrame()
        self.scroll_area_wrapper.setStyleSheet("""
            QFrame {
                background: #20273E; /* Фон для обёртки */
                border: none;
            }
        """)
        self.scroll_area_wrapper_layout = QVBoxLayout(self.scroll_area_wrapper)
        self.scroll_area_wrapper_layout.setContentsMargins(10, 0, 10, 5)  # Отступы внутри обёртки
        self.scroll_area_wrapper_layout.setSpacing(0)

        # Создаём область прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Настраиваем стиль ScrollArea
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                border-radius: 16px; /* Закругление ScrollArea */
                background: #20273E;
            }
            QScrollBar:vertical {
                width: 10px;
                background: #20273E;
            }
            QScrollBar:horizontal {
                height: 10px;
                background: #20273E;
            }
            QScrollBar::handle {
                background: #FFFFFF;
                border-radius: 5px;
            }
            QScrollBar::handle:hover {
                background: #FFFFFF;
            }
            QScrollBar::add-page {
                background: none;
                margin: 0;
            }
            QScrollBar::sub-page {
                background: none;
                margin: 0;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
                border: none;
            }
        """)
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            QFrame {
                background: #20273E;
                border-radius: 16px;
            }
        """)

        self.content_layout = QGridLayout(self.content_frame)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(5)

        self.row_count = 0
        self.col_count = 0
        self.columns = 4

        self.scroll_area.setWidget(self.content_frame)
        self.scroll_area_wrapper_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.scroll_area_wrapper)

        self.setLayout(self.main_layout)

    def add_widget(self, widget):
        """
        Добавляет виджет в сетку.
        """
        self.content_layout.addWidget(widget, self.row_count, self.col_count)
        self.col_count += 1
        if self.col_count >= self.columns:
            self.col_count = 0
            self.row_count += 1


if __name__ == "__main__":
    app = QApplication([])
    window = DynamicButtonWidget()

    for i in range(40):
        btn = TemperatureWidget(i+1)
        window.add_widget(btn)

    window.setWindowTitle("Список с обёрткой")
    window.resize(400, 600)

    window.show()
    app.exec_()
