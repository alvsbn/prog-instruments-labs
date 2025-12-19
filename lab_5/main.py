import sys
import logging

from PyQt5.QtWidgets import QApplication

from main_window import Window


logger = logging.getLogger(__name__)


def setup_logging():
    """
    Настройка системы логирования
    """
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )

    file_handler = logging.FileHandler("application.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def main():
    setup_logging()

    try:
        logger.info("Запуск приложения 'View Dataset'")
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        logger.info("Приложение успешно запущено")
        exit_code = app.exec_()
        logger.info("Приложение завершено")
        sys.exit(exit_code)

    except Exception as e:
        logger.critical("Ошибка при запуске: %s", e)
        sys.exit(1)


if __name__ == '__main__':
    main()