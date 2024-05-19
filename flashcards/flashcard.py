"""Module containing the Flashcard classes."""

import os
from datetime import datetime
from PySide6 import QtCore, QtWidgets

class Flashcard(QtWidgets.QWidget):
    """Class that contains a single flashcard's data.

    Parameters
    ----------
    card_id : pathline
        Path to flashcard file.
    
    Attributes
    ----------
    card_id : pathline
        Path to flashcard file.
    front : string
        Text on the front of flashcard.
    back : string
        Text on the back of flashcard.
    labels : list of strings
        Card label(s).
    created_date : datetime
        Date and time of flashcard (file) creation.
    """
    def __init__(self, card_id):
        super().__init__()

        self.front = QtWidgets.QLineEdit("", alignment=QtCore.Qt.AlignCenter)
        font = self.front.font()
        font.setPointSize(24)
        self.front.setFont(font)
        self.back = QtWidgets.QLineEdit("", alignment=QtCore.Qt.AlignCenter)
        font = self.back.font()
        font.setPointSize(24)
        self.back.setFont(font)

        self.labels = [""]
        self.created_date = ""

        self.card_id = card_id
        self.create_card()
        try:
            self.read_card_data()
        except AssertionError:
            print(f"{self.card_id} isn't formatted correctly. Consider deleting this card.")
    
        self.setWindowTitle(f"Created: {self.created_date}")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.front)
        self.layout.addWidget(self.back)

    def read_card_data(self):
        """Read the flashcard's data.
        
        Returns
        -------
        string
            Text on front of card.
        string
            Text on back of card.
        list of strings
            Card label(s).
        """
        with open(self.card_id, "r", encoding="utf-8") as f:
            card_data = f.readlines()
        assert len(card_data) == 4, "Flashcard file should contain exactly 4 lines."

        self.created_date = card_data[0]
        self.front.setText(card_data[1])
        self.back.setText(card_data[2])
        self.labels = card_data[3]

    def write_card_data(self, front, back, labels):
        """Alter flashcard's data.
        
        Parameters
        ----------
        front : string
            Text on front of card.
        back : string
            Text on back of card.
        labels : list of strings
            Card label(s).
        """
        with open(self.card_id, "w", encoding="utf-8") as f:
            f.write(f"{self.created_date}\n")
            f.write(f"{front}\n")
            f.write(f"{back}\n")
            f.write(f"{labels}\n")

        self.read_card_data()

    def delete_card(self):
        """Delete the flashcard file."""
        os.remove(self.card_id)

    def create_card(self):
        """Create an empty flashcard."""
        if os.path.exists(self.card_id):
            print(f"Card already exists at {self.card_id}!")
            return
        with open(self.card_id, "w", encoding="utf-8") as f:
            f.write("")
        self.created_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.write_card_data("", "", "")

    def closeEvent(self, event):
        """Overwritten function to define custom action on window close.
        
        Parameters
        ----------
        event : QtGui.QCloseEvent
        """
        self.write_card_data(self.front.text().split("\n")[0], self.back.text().split("\n")[0], self.labels)

    # def keyPressEvent(self, event):
    #     if event.key() != QtCore.Qt.Key_Enter:
    #         return
    #     if self.back == "" or self.front == "":
    #         empty_input = QtWidgets.QDialogButtonBox("Empty input box!")
    #         empty_input.show()
