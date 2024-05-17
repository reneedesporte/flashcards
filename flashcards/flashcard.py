"""Module containing the Flashcard classes."""

import os
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

        self.card_id = card_id
        if not os.path.exists(self.card_id):
            self.create_card()

        self.front = QtWidgets.QLineEdit("", alignment=QtCore.Qt.AlignCenter)
        self.back = QtWidgets.QLineEdit("", alignment=QtCore.Qt.AlignCenter)
        self.labels = [""]
        self.created_date = os.path.getctime(self.card_id)

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
        assert len(card_data) == 3, "Flashcard file should contain exactly 3 lines."

        self.front.setText(card_data[0])
        self.back.setText(card_data[1])
        self.labels = card_data[2]

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
            f.write(f"{front}\n")
            f.write(f"{back}\n")
            f.write(f"{labels}")

        self.read_card_data()  # Confirm only 3 lines were written to file, and save attributes.

    def delete_card(self):
        """Delete the flashcard file."""
        os.remove(self.card_id)

    def create_card(self):
        """Create an empty flashcard."""
        with open(self.card_id, "w", encoding="utf-8") as f:
            f.write("")

    def closeEvent(self, event):
        """Overwritten function to define custom action on window close.
        
        Parameters
        ----------
        event : QtGui.QCloseEvent
        """
        self.write_card_data(self.front.text(), self.back.text(), self.labels)
