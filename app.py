import sys
from PyQt5.QtWidgets import (
	QApplication,
	QWidget,
	QPushButton,
	QGridLayout,
	QVBoxLayout,
	QLabel,
	QMessageBox,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class TicTacToe(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Tic Tac Toe")
		self.setFixedSize(360, 420)

		self.current_player = "X"
		self.game_active = True

		# track the order of moves for each player so we can remove the first one later
		self.move_history = {"X": [], "O": []}

		main_layout = QVBoxLayout()
		self.status_label = QLabel("Turn: X")
		self.status_label.setAlignment(Qt.AlignCenter)
		self.status_label.setFont(QFont("Arial", 14, QFont.Bold))

		main_layout.addWidget(self.status_label)

		grid = QGridLayout()
		grid.setSpacing(6)

		self.buttons = []
		btn_font = QFont("Arial", 28, QFont.Bold)

		for row in range(3):
			for col in range(3):
				btn = QPushButton("")
				btn.setFixedSize(100, 100)
				btn.setFont(btn_font)
				btn.setFocusPolicy(Qt.NoFocus)
				index = row * 3 + col
				btn.clicked.connect(lambda _, i=index: self.on_button_clicked(i))
				self.buttons.append(btn)
				grid.addWidget(btn, row, col)

		main_layout.addLayout(grid)

		self.reset_button = QPushButton("Reset")
		self.reset_button.setFixedHeight(40)
		self.reset_button.clicked.connect(self.reset_board)
		main_layout.addWidget(self.reset_button)

		self.setLayout(main_layout)

	def on_button_clicked(self, index: int):
		if not self.game_active:
			return

		btn = self.buttons[index]
		if btn.text():
			return


		if all(b.text() for b in self.buttons):
			# Prevent a draw as a fallback: remove the earliest move of each player (if any) so the game can continue.
			removed_any = False
			for player in ("X", "O"):
				hist = self.move_history.get(player, [])
				if hist:
					idx_to_remove = hist.pop(0)
					self.buttons[idx_to_remove].setText("")
					self.buttons[idx_to_remove].setEnabled(True)
					self.buttons[idx_to_remove].setStyleSheet("")
					removed_any = True
			if not removed_any:
				# fallback: truly a draw (no history to remove)
				self.game_active = False
				self.status_label.setText("Draw")
				QMessageBox.information(self, "Game Over", "It's a draw!")
				return

		# Personal rule: if the current player already has 3 marks on the board
		# (i.e. this will be their 4th), remove their earliest mark before placing.
		player_hist = self.move_history.get(self.current_player, [])
		if len(player_hist) == 3:
			first_idx = player_hist.pop(0)
			# clear that button
			self.buttons[first_idx].setText("")
			self.buttons[first_idx].setEnabled(True)
			self.buttons[first_idx].setStyleSheet("")

		# place the current player's mark
		btn.setText(self.current_player)
		btn.setEnabled(False)
		# record this move in history
		self.move_history[self.current_player].append(index)

		winner = self.check_winner()
		if winner:
			self.game_active = False
			self.status_label.setText(f"Winner: {winner}")
			QMessageBox.information(self, "Game Over", f"{winner} wins!")
			self.highlight_winner(winner)
			return

		self.toggle_player()

	def toggle_player(self):
		self.current_player = "O" if self.current_player == "X" else "X"
		self.status_label.setText(f"Turn: {self.current_player}")

	def check_winner(self):
		lines = [
			(0, 1, 2),
			(3, 4, 5),
			(6, 7, 8),
			(0, 3, 6),
			(1, 4, 7),
			(2, 5, 8),
			(0, 4, 8),
			(2, 4, 6),
		]

		for a, b, c in lines:
			ta, tb, tc = self.buttons[a].text(), self.buttons[b].text(), self.buttons[c].text()
			if ta and ta == tb == tc:
				return ta
		return None

	def highlight_winner(self, winner_symbol: str):
		# Highlight winning line(s)
		lines = [
			(0, 1, 2),
			(3, 4, 5),
			(6, 7, 8),
			(0, 3, 6),
			(1, 4, 7),
			(2, 5, 8),
			(0, 4, 8),
			(2, 4, 6),
		]
		for a, b, c in lines:
			if (
				self.buttons[a].text()
				and self.buttons[a].text() == self.buttons[b].text() == self.buttons[c].text() == winner_symbol
			):
				for i in (a, b, c):
					self.buttons[i].setStyleSheet(
						"background-color: #90ee90; color: #006400; border: 2px solid #006400;"
					)

		# disable all buttons after win
		for btn in self.buttons:
			btn.setEnabled(False)

	def reset_board(self):
		for btn in self.buttons:
			btn.setText("")
			btn.setEnabled(True)
			btn.setStyleSheet("")
		self.current_player = "X"
		self.game_active = True
		self.status_label.setText("Turn: X")
		# clear move history
		self.move_history = {"X": [], "O": []}


def main():
	app = QApplication(sys.argv)
	win = TicTacToe()
	win.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

