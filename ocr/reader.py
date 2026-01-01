import pytesseract
from PIL import Image
from PySide6.QtCore import QBuffer, QByteArray
import io

# Caminho fixo do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pixmap(pixmap):
    """
    Converte QPixmap para PIL Image usando QBuffer e executa OCR
    """

    # Criar buffer Qt
    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)

    # Salvar pixmap no buffer como PNG
    pixmap.save(buffer, "PNG")

    # Converter para bytes
    pil_image = Image.open(io.BytesIO(buffer.data()))

    # OCR
    text = pytesseract.image_to_string(pil_image)

    return text
