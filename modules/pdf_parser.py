from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(uploaded_file):
    text = ""

    try:
        pdf_stream = io.BytesIO(uploaded_file.read())
        reader = PdfReader(pdf_stream)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        return f"Error: {str(e)}"