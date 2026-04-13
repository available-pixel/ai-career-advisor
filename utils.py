# utils.py
from PyPDF2 import PdfReader
import tempfile

def extract_text_from_pdf(file):
    """
    Works with both:
    - file path (string)
    - Streamlit UploadedFile
    """

    # If Streamlit upload (UploadedFile)
    if hasattr(file, "read"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        file = tmp_path

    reader = PdfReader(file)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text