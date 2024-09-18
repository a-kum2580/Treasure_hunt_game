import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout

class TreasureHunt(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Treasure Hunt Game")
        self.grid = QGridLayout()  # Create grid layout for the game board
        self.setLayout(self.grid)
        self.treasures = []
        self.guesses = 0
        self.found_treasures = 0
        self.total_treasures = 5
        self.feedback_label = QLabel("Guess the treasures!")
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.feedback_label)
        self.setLayout(self.layout)

        # Initialize grid with buttons
        self.buttons = {}
        for x in range(10):
            for y in range(10):
                button = QPushButton("")
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda ch, x=x, y=y: self.check_guess(x, y))
                self.grid.addWidget(button, x, y)
                self.buttons[(x, y)] = button

        # Generate random treasures
        self.generate_treasures()

    def generate_treasures(self):
        while len(self.treasures) < self.total_treasures:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if (x, y) not in self.treasures:
                self.treasures.append((x, y))

    def check_guess(self, x, y):
        self.guesses += 1
        if (x, y) in self.treasures:
            self.feedback_label.setText(f"Treasure Found at ({x+1}, {y+1})! Total treasures found: {self.found_treasures + 1}")
            self.buttons[(x, y)].setStyleSheet("background-color: gold")  # Mark the treasure location
            self.buttons[(x, y)].setEnabled(False)
            self.found_treasures += 1
            if self.found_treasures == self.total_treasures:
                self.feedback_label.setText(f"Congratulations! You found all treasures in {self.guesses} guesses!")
        else:
            # Calculate minimum distance from any treasure
            distances = [abs(x - tx) + abs(y - ty) for tx, ty in self.treasures]
            min_distance = min(distances)
            if min_distance <= 2:
                self.feedback_label.setText(f"Hot! You are close to a treasure at ({x+1}, {y+1}).")
                self.buttons[(x, y)].setStyleSheet("background-color: red")
            else:
                self.feedback_label.setText(f"Cold! No treasure nearby at ({x+1}, {y+1}).")
                self.buttons[(x, y)].setStyleSheet("background-color: blue")
            self.buttons[(x, y)].setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = TreasureHunt()
    game.show()
    sys.exit(app.exec_())
