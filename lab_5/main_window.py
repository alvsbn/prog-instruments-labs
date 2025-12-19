import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox

from iterator import Iterator

class Window(QMainWindow):
    def __init__(self):
        """
        Конструктор
        """
        super().__init__()

        self.setWindowTitle('View dataset')
        self.setGeometry(300, 250, 800,500)

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

    def show_image(self)-> None:
        """
        Отображает текущее изображение
        """
        if os.path.exists(self.current_image):
            pixmap = QPixmap(self.current_image)
            pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
        else:
            QMessageBox.warning(self, 'Error', 'Image file does not exist.')

    def next_image(self) -> None:
        """
        Отображает следующее изображение
        """
        try:
            self.current_image = next(self.iterator)
            self.show_image()
        except StopIteration:
            QMessageBox.warning(self, 'Error', 'No more images')
            self.next_button.setEnabled(False)

    def open_folder(self) -> None:
        """
        Открывает диалог выбора файла
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "CSV Files (*.csv)")
        if file_path:
            if os.stat(file_path).st_size == 0:
                QMessageBox.warning(self, "Error", "The file is empty.")
                return

            self.iterator = Iterator(file_path)
            try:
                self.current_image = next(self.iterator)
                self.show_image()
                self.next_button.setEnabled(True)
            except StopIteration:
                QMessageBox.warning(self, "Error", f"The file is empty.")
                self.next_button.setEnabled(False)