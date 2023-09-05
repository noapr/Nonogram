import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from database import DATABASE
from gui.create_nonogram_from_photo import CreateNonogramFromPhotoWindow
from gui.nonogram_selection import NonogramSelection
from nonogram import Nonogram

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Nonogram Game')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        title_label = QLabel('Welcome to Nonogram Game', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title_label)

        create_button = QPushButton('Create Nonogram from a Photo', self)
        select_button = QPushButton('Select Nonogram from a List', self)

        # Set button styles
        create_button.setStyleSheet(
            'QPushButton {background-color: #3498db; color: white; font-size: 16px; padding: 10px; border: none;}'
            'QPushButton:hover {background-color: #2980b9;}'
        )
        select_button.setStyleSheet(
            'QPushButton {background-color: #2ecc71; color: white; font-size: 16px; padding: 10px; border: none;}'
            'QPushButton:hover {background-color: #27ae60;}'
        )

        # Connect buttons to actions
        create_button.clicked.connect(self.create_nonogram)
        select_button.clicked.connect(self.open_nonogram_selection_window)

        # Add buttons to layout
        layout.addWidget(create_button)
        layout.addWidget(select_button)

        central_widget.setLayout(layout)

    def create_nonogram(self):
        self.close()
        create_nonogram = CreateNonogramFromPhotoWindow()
        create_nonogram.exec_()

    def open_nonogram_selection_window(self):
        self.close()
        nonograms = {}
        for i in range(len(DATABASE)):
            nonograms[DATABASE[i].get('name')] = Nonogram(rows=DATABASE[i].get('rows'), columns=DATABASE[i].get('columns'), name=DATABASE[i].get('name'))
        nonogram_selection = NonogramSelection(nonograms)
        nonogram_selection.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())
