import os
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox

from iterator import Iterator


logger = logging.getLogger(__name__)


class Window(QMainWindow):
    def __init__(self):
        """
        Конструктор
        """
        super().__init__()
        logger.info("Инициализация главного окна просмотра данных")

        self.setWindowTitle('View dataset')
        self.setGeometry(300, 250, 800, 500)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.open_button = QPushButton('dataset folder', self)
        self.open_button.clicked.connect(self.open_folder)

        self.next_button = QPushButton('next', self)
        self.next_button.clicked.connect(self.next_image)
        self.next_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.next_button)
        layout.addWidget(self.open_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.iterator = None
        self.current_image = None

        logger.debug("Компоненты интерфейса созданы и настроены")

    def show_image(self) -> None:
        """
        Отображает текущее изображение
        """
        logger.debug("Вызов метода отображения изображения")

        if self.current_image and os.path.exists(self.current_image):
            logger.info("Отображение изображения: %s", self.current_image)
            try:
                pixmap = QPixmap(self.current_image)
                if pixmap.isNull():
                    logger.warning("Не удалось загрузить изображение: %s", self.current_image)
                    QMessageBox.warning(self, 'Ошибка', 'Не удалось загрузить изображение.')
                    return

                pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)
                logger.debug("Изображение успешно отображено")

            except Exception as e:
                logger.error("Ошибка при загрузке изображения: %s", e, exc_info=True)
                QMessageBox.warning(self, 'Ошибка', f'Ошибка загрузки изображения: {str(e)}')
        else:
            logger.warning("Файл изображения не существует: %s", self.current_image)
            QMessageBox.warning(self, 'Ошибка', 'Файл изображения не существует.')

    def next_image(self) -> None:
        """
        Отображает следующее изображение
        """
        logger.debug("Запрос следующего изображения")

        try:
            self.current_image = next(self.iterator)
            self.show_image()
        except StopIteration:
            logger.info("Достигнут конец набора изображений")
            QMessageBox.warning(self, 'Ошибка', 'Нет больше доступных изображений.')
            self.next_button.setEnabled(False)
        except Exception as e:
            logger.error("Ошибка при переходе: %s", e)
            QMessageBox.warning(self, 'Error', f'Error: {str(e)}')

    def open_folder(self) -> None:
        """
        Открывает диалог выбора файла
        """
        logger.info("Открытие диалога выбора файла аннотаций")

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл аннотаций",
            "",
            "CSV файлы (*.csv)"
        )

        if file_path:
            logger.info("Пользователь выбрал файл: %s", file_path)

            try:
                if os.stat(file_path).st_size == 0:
                    logger.warning("Выбранный файл пуст: %s", file_path)
                    QMessageBox.warning(self, "Ошибка", "Выбранный файл пустой.")
                    return
                logger.debug("Размер файла: %d байт", os.stat(file_path).st_size)
            except Exception as e:
                logger.error("Ошибка при проверке файла: %s", e, exc_info=True)
                QMessageBox.warning(self, "Ошибка", f"Ошибка проверки файла: {str(e)}")
                return

            try:
                self.iterator = Iterator(file_path)
                logger.debug("Итератор успешно создан")

                self.current_image = next(self.iterator)
                logger.info("Загружено первое изображение: %s", self.current_image)

                self.show_image()
                self.next_button.setEnabled(True)
                logger.info("Готов к просмотру набора изображений")

            except StopIteration:
                logger.error("Файл аннотаций не содержит данных: %s", file_path)
                QMessageBox.warning(self, "Ошибка", "Файл аннотации не содержит корректных данных.")
                self.next_button.setEnabled(False)
            except Exception as e:
                logger.error("Ошибка при обработке файла аннотаций: %s", e, exc_info=True)
                QMessageBox.warning(self, "Ошибка", f"Ошибка загрузки файла: {str(e)}")
                self.next_button.setEnabled(False)
        else:
            logger.debug("Пользователь отменил выбор файла")
