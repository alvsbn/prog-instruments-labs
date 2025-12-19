import sys

from PyQt5.QtWidgets import QApplication

from main_window import Window


def main():
    try:
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
