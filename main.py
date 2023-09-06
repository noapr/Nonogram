import sys
from PyQt5.QtWidgets import QApplication

from gui.start_window import WelcomeWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())
