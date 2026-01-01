import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QGuiApplication

from analysis.pot_odds import calculate_pot_odds
from database.db import save_hand


class PokerReviewApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poker Hand Review")
        self.resize(600, 600)

        self.last_data = None
        self.current_image = None

        layout = QVBoxLayout()

        # --- Print ---
        self.paste_button = QPushButton("📋 Colar print da mesa")
        self.paste_button.clicked.connect(self.paste_image)

        self.image_label = QLabel("Nenhum print colado")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(250)
        self.image_label.setStyleSheet("border: 1px solid gray")

        # --- Inputs ---
        self.stack_input = QLineEdit()
        self.stack_input.setPlaceholderText("Stack do herói (BB)")

        self.pot_input = QLineEdit()
        self.pot_input.setPlaceholderText("Pot size")

        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("Aposta do vilão")

        self.hand_strength = QComboBox()
        self.hand_strength.addItems(["forte", "media", "fraca"])

        self.analyze_button = QPushButton("Analisar")
        self.analyze_button.clicked.connect(self.analyze_hand)

        self.save_button = QPushButton("Salvar mão")
        self.save_button.clicked.connect(self.save_current_hand)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)

        # --- Layout ---
        layout.addWidget(self.paste_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.stack_input)
        layout.addWidget(self.pot_input)
        layout.addWidget(self.bet_input)
        layout.addWidget(QLabel("Força da mão:"))
        layout.addWidget(self.hand_strength)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def paste_image(self):
        clipboard = QGuiApplication.clipboard()
        image = clipboard.image()

        if image.isNull():
            self.image_label.setText("Nenhuma imagem encontrada no clipboard")
            return

        pixmap = QPixmap.fromImage(image)
        self.current_image = pixmap

        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.KeepAspectRatio
            )
        )

    def analyze_hand(self):
        try:
            stack_bb = float(self.stack_input.text())
            pot = float(self.pot_input.text())
            bet = float(self.bet_input.text())
            strength = self.hand_strength.currentText()

            pot_odds = calculate_pot_odds(pot, bet)

            equity = 0.6 if strength == "forte" else 0.3 if strength == "media" else 0.1
            decision = "CALL" if equity >= pot_odds else "FOLD"

            notes = f"Pot odds: {pot_odds:.2%} | Equidade: {equity:.0%}"

            self.last_data = (stack_bb, pot, bet, decision, notes)

            self.result_label.setText(
                f"Pot odds: {pot_odds:.2%}\n"
                f"Equidade: {equity:.0%}\n"
                f"Decisão: {decision}"
            )

        except ValueError:
            self.result_label.setText("Preencha todos os campos corretamente.")

    def save_current_hand(self):
        if not self.last_data:
            self.result_label.setText("Faça a análise antes de salvar.")
            return

        save_hand(*self.last_data)
        self.result_label.setText("✅ Mão salva com sucesso!")


app = QApplication(sys.argv)
window = PokerReviewApp()
window.show()
sys.exit(app.exec())
