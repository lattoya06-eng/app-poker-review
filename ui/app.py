import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout,
    QComboBox, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QGuiApplication

from ocr.reader import extract_text_from_pixmap
from parser.hand_parser import extract_numbers
from analysis.pot_odds import calculate_pot_odds
from database.db import save_hand


class PokerReviewApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poker Hand Review")
        self.resize(650, 700)

        self.last_data = None
        self.current_image = None

        layout = QVBoxLayout()

        # --- Image buttons ---
        self.paste_button = QPushButton("📋 Colar print da mesa")
        self.paste_button.clicked.connect(self.paste_image)

        self.open_button = QPushButton("📂 Abrir imagem")
        self.open_button.clicked.connect(self.open_image)

        self.ocr_button = QPushButton("🔍 Ler texto do print")
        self.ocr_button.clicked.connect(self.run_ocr)

        self.image_label = QLabel("Nenhuma imagem carregada")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(260)
        self.image_label.setStyleSheet("border: 1px solid gray")

        # --- Inputs ---
        self.bb_input = QLineEdit()
        self.bb_input.setPlaceholderText("Valor do BB (ex: 1)")

        self.stack_input = QLineEdit()
        self.stack_input.setPlaceholderText("Stack do herói (BB)")

        self.pot_input = QLineEdit()
        self.pot_input.setPlaceholderText("Pot size (BB)")

        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("Aposta do vilão (BB)")

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
        layout.addWidget(self.open_button)
        layout.addWidget(self.ocr_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.bb_input)
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
            self.result_label.setText("Nenhuma imagem no clipboard.")
            return

        pixmap = QPixmap.fromImage(image)
        self.set_current_image(pixmap)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg)"
        )

        if not file_path:
            return

        pixmap = QPixmap(file_path)
        self.set_current_image(pixmap)

    def set_current_image(self, pixmap):
        self.current_image = pixmap
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.KeepAspectRatio
            )
        )

    def run_ocr(self):
        if self.current_image is None:
            self.result_label.setText("Carregue uma imagem primeiro.")
            return

        text = extract_text_from_pixmap(self.current_image)
        data = extract_numbers(text)

        try:
            bb_value = float(self.bb_input.text())
        except ValueError:
            bb_value = 1.0

        # Stack já vem em BB
        if data["stack"] is not None:
            self.stack_input.setText(f"{data['stack']:.1f}")

        # Pot e Bet podem vir em fichas → converter para BB
        if data["pot"] is not None:
            self.pot_input.setText(f"{data['pot'] / bb_value:.1f}")

        if data["bet"] is not None:
            self.bet_input.setText(f"{data['bet'] / bb_value:.1f}")

        self.result_label.setText("📊 Valores normalizados em BB")

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
