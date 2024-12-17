import random
import requests
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot


class WorkerThread(QThread):
    # Сигнал для передачи результата из потока в виджет
    prediction_result = pyqtSignal(int)

    def __init__(self, widget_id, product_id, machine_type, parent=None):
        super().__init__(parent)
        self.widget_id = widget_id
        self.product_id = product_id
        self.machine_type = machine_type
        self.running = True  # Флаг для управления запуском и остановкой

    def run(self):
        while self.running:
            # Генерация случайных значений для полей
            feature4 = random.uniform(295.3, 304.4)
            feature5 = random.uniform(305, 313)
            feature6 = random.randint(1200, 1800)
            feature7 = random.uniform(-20, 60)
            feature8 = random.randint(0, 253)
            feature9 = random.randint(0, 1)
            feature10 = random.randint(0, 1)
            feature11 = random.randint(0, 1)
            feature12 = random.randint(0, 1)
            feature13 = feature9 + feature10 + feature11 + feature12
            product_id_numeric = int(''.join(filter(str.isdigit, self.product_id)))  # Убираем буквы
            machine_type_numeric = {"L": 1, "H": 2, "M": 3}.get(self.machine_type, 0)  # Кодируем буквы

            # Формируем данные
            data = {
                "feature1": self.widget_id,
                "feature2": product_id_numeric,
                "feature3": machine_type_numeric,
                "feature4": feature4,
                "feature5": feature5,
                "feature6": feature6,
                "feature7": feature7,
                "feature8": feature8,
                "feature9": feature9,
                "feature10": feature10,
                "feature11": feature11,
                "feature12": feature12,
                "feature13": feature13,
            }
            print(data)

            try:
                # Отправка POST-запроса
                response = requests.post("http://127.0.0.1:8000/predict/", json=data)
                if response.status_code == 200:
                    prediction = response.json().get("prediction", [1])[0]
                    self.prediction_result.emit(prediction)  # Отправляем результат
                else:
                    print("Ошибка при запросе к API:", response.status_code, response.text)
            except Exception as e:
                print("Ошибка подключения к API:", e)

            self.msleep(1000)  # Ждем 1 секунду

    def stop(self):
        self.running = False  # Останавливаем поток


class TemperatureWidget(QWidget):
    def __init__(self, widget_id: int, product_id, machine_type, parent=None):
        super().__init__(parent)
        self.setFixedHeight(150)
        self.widget_id = widget_id
        self.product_id = product_id
        self.machine_type = machine_type

        # Устанавливаем зелёный цвет через стиль
        self.default_color = "#30FD3A"
        self.error_color = "#FF3A3A"
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.default_color};
                border-radius: 10px;
            }}
        """)

        # Создаём текстовый элемент (QLabel) для отображения ID
        self.label = QLabel(f"id: {widget_id}", self)
        self.label.setAlignment(Qt.AlignCenter)  # Выравниваем текст по центру
        self.label.setStyleSheet("""
            QLabel {
                color: #20273E;  
                font-size: 18px;
                font-weight: bold;
                font-family: Gilroy;
            }
        """)

        # Размещаем текст по центру виджета через QVBoxLayout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Создаем поток для работы с API
        self.worker_thread = WorkerThread(widget_id, product_id, machine_type)
        self.worker_thread.prediction_result.connect(self.update_color)
        self.worker_thread.start()

    @pyqtSlot(int)
    def update_color(self, prediction):
        """
        Обновление цвета виджета на основе предсказания.
        """
        if prediction == 0:
            # Если предсказание 0, меняем цвет на красный и останавливаем поток
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.error_color};
                    border-radius: 10px;
                }}
            """)
            self.worker_thread.stop()

            # После 1 секунды возвращаем цвет обратно и перезапускаем поток
            QTimer.singleShot(1000, self.reset_color)
        else:
            # Если предсказание 1, оставляем зеленый цвет
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.default_color};
                    border-radius: 10px;
                }}
            """)

    def reset_color(self):
        """
        Возвращает цвет виджета в зеленый и перезапускает поток.
        """
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.default_color};
                border-radius: 10px;
            }}
        """)
        self.worker_thread.start()  # Перезапускаем поток при необходимости

    def closeEvent(self, event):
        """
        Останавливаем поток при закрытии виджета.
        """
        self.worker_thread.stop()
        self.worker_thread.wait()
        event.accept()
