from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PIL import Image
from gui.nonogram_game import NonogramGame
from nonogram_generator import NonogramGenerator


class CreateNonogramFromPhotoWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Create Nonogram from Photo')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.width_label = QLabel('Width (5-20):')
        self.width_input = QLineEdit()
        layout.addWidget(self.width_label)
        layout.addWidget(self.width_input)

        self.height_label = QLabel('Height (5-20):')
        self.height_input = QLineEdit()
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        self.photo_label = QLabel('Select a Photo:')
        self.photo_path = None
        self.photo_label.setWordWrap(True)
        layout.addWidget(self.photo_label)

        self.select_photo_button = QPushButton('Select Photo')
        self.select_photo_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.select_photo_button)

        self.create_button = QPushButton('Create Nonogram')
        self.create_button.clicked.connect(self.create_nonogram)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        photo_path, _ = QFileDialog.getOpenFileName(self, 'Select a Photo', '', 'Images (*.jpg *.png);;All Files (*)', options=options)

        if photo_path:
            # Check if the selected file is a valid photo
            if self.is_valid_photo(photo_path):
                # Display the selected photo's path
                self.photo_path = photo_path
                self.photo_label.setText(f'Selected Photo: {photo_path}')
            else:
                QMessageBox.warning(self, 'Warning', 'The selected file is not a valid photo.')

    def is_valid_photo(self, file_path):
        try:
            # Use Pillow (PIL) to open the file and check its format
            with Image.open(file_path) as img:
                return img.format in ('JPEG', 'PNG')
        except Exception:
            return False

    def create_nonogram(self):
        # Get user input for width and height
        width = self.width_input.text()
        height = self.height_input.text()

        try:
            width = int(width)
            height = int(height)

            # Check if width and height are within the allowed range
            if 5 <= width <= 20 and 5 <= height <= 20:
                if self.photo_path:
                    nonogram_generator = NonogramGenerator(self.photo_path, width, height)
                    if not nonogram_generator.is_nonogram_solvable():
                        QMessageBox.warning(self, 'Warning', "I can't create a game from these parameters. Please change parameters and try again.")
                    else:
                        self.close()
                        game = NonogramGame(nonogram_generator.get_nonogram())
                        game.show()

                    # Once the nonogram is created, you can close the window or perform any other action
                    self.accept()
                else:
                    QMessageBox.warning(self, 'Warning', 'Please select a photo.')
            else:
                QMessageBox.warning(self, 'Warning', 'Width and Height must be between 5 and 20.')
        except ValueError:
            QMessageBox.warning(self, 'Warning', 'Width and Height must be integers.')
