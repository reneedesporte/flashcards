"""Module containing main application."""

import sys
import os
import random
import string
from PySide6 import QtCore, QtWidgets
import flashcard

SAVED_CARDS = "cards"  # Directory wherein flashcard files are saved. TODO: make database instead


class Deck(QtWidgets.QWidget):
    """Widget to control Flashcard Deck."""
    def __init__(self):
        super().__init__()

        self.save_dir = SAVED_CARDS  # TODO: get user input
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.cards = []
        self.load_cards()
        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        if len(self.cards) == 0:
            self.text.setText("No flashcards loaded.")

        self.new_card_butn = QtWidgets.QPushButton("New Flashcard")
        self.delete_all_cards_butn = QtWidgets.QPushButton("Delete all Flashcards")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.new_card_butn)
        self.layout.addWidget(self.delete_all_cards_butn)

        self.new_card_butn.clicked.connect(self.new_card)
        self.delete_all_cards_butn.clicked.connect(self.delete_cards)

    def new_card(self):
        """Add a new flashcard to the deck."""
        rand_str = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])
        self.cards.append(flashcard.Flashcard(os.path.join(self.save_dir,
                                                           rand_str(64))))
        self.text.setText("Created new flashcard!")

    def delete_cards(self):
        """Delete all flashcards in `save_dir`."""
        for card in self.cards:
            card.delete_card()
        self.text.setText("Deleted all flashcards!")

    def load_cards(self):
        """Load cards from save directory.
        
        Returns
        -------
        list of Flashcards
        """
        for card in [f for f in os.listdir(self.save_dir) if os.path.isfile(os.path.join(self.save_dir, f))]:
            self.cards.append(flashcard.Flashcard(os.path.join(self.save_dir, card)))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Deck()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
