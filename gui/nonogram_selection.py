import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QListWidget, QListWidgetItem

from database import DATABASE
from nonogram import Nonogram
from nonogram_game import NonogramGame


class NonogramSelection(QDialog):
    def __init__(self, nonograms):
        super().__init__()

        self.nonograms = nonograms
        self.selected_nonogram = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select a Nonogram')
        self.setGeometry(700, 400, 400, 300)

        layout = QVBoxLayout()

        label = QLabel('Choose a nonogram:')
        self.nonogram_list = QListWidget()
        self.nonogram_list.itemDoubleClicked.connect(self.select_nonogram)

        for nonogram_name in self.nonograms:
            item = QListWidgetItem(nonogram_name)
            self.nonogram_list.addItem(item)

        select_button = QPushButton('Select Nonogram')
        select_button.clicked.connect(self.select_nonogram)

        layout.addWidget(label)
        layout.addWidget(self.nonogram_list)
        layout.addWidget(select_button)

        self.setLayout(layout)

    def select_nonogram(self):
        selected_item = self.nonogram_list.currentItem()
        if selected_item:
            nonogram_name = selected_item.text()
            if nonogram_name in self.nonograms:
                self.selected_nonogram = self.nonograms[nonogram_name]
                self.accept()


def main():
    app = QApplication(sys.argv)

    nonograms = {}
    for i in range(len(DATABASE)):
        nonograms[DATABASE[i].get('name')] = Nonogram(rows=DATABASE[i].get('rows'), columns=DATABASE[i].get('columns'), name=DATABASE[i].get('name'))

    nonogram_selection = NonogramSelection(nonograms)
    if nonogram_selection.exec_() == QDialog.Accepted:
        selected_nonogram = nonogram_selection.selected_nonogram

        # Create the game window with the selected nonogram
        game = NonogramGame(selected_nonogram)
        game.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
