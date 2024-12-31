import PyPDF2
from utils import prettify_text, remove_personal_details

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    extracted_text = "".join(page.extract_text() for page in pdf_reader.pages)
    return prettify_text(remove_personal_details(extracted_text))
