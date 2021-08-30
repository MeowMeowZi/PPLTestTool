from ui_controller import MainUI
import sys
import threading
from PyQt5.QtWidgets import QApplication


class Run():
    def __init__(self):
        self.ui = MainUI()
        self.app = QApplication(sys.argv)
        threading.Thread(target=self.run_ui)

        print('123')

    def run_ui(self):
        self.ui.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    run = Run()





