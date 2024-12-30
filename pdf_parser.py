import PyPDF2
import re

def prettify_text(text):
    """Format text for better readability."""
    text = re.sub(r'\s+', ' ', text)  # Remove excessive whitespace
    text = re.sub(r'(\.\s)', r'.\n\n', text)  # Add line breaks after sentences
    lines = [line.strip() for line in text.split('\n')]  # Trim extra spaces
    return '\n'.join(lines)

def remove_personal_details(text):
    """Remove personal details using predefined regex patterns."""
    patterns = [
        re.compile(r"Patient Name\s*:\s*[A-Za-z\s]+"),
        re.compile(r"Patient UID No\s*:\s*\w+"),
        re.compile(r"Age and Gender\s*:\s*\d+\s*Years\s*/\s*[A-Za-z]+"),
        # Add more patterns as needed
    ]
    for pattern in patterns:
        text = pattern.sub('', text)
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove blank lines
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extract, clean, and prettify text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''.join([page.extract_text() for page in reader.pages])
        # Remove personal details and prettify the text
        cleaned_text = remove_personal_details(text)
        return prettify_text(cleaned_text)
    except Exception as e:
        raise ValueError(f"Failed to process PDF: {e}")
