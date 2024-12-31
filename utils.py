import re

def prettify_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove excessive whitespace
    text = re.sub(r'(\.\s)', r'.\n\n', text)  # Add line breaks after sentences
    lines = [line.strip() for line in text.split('\n')]  # Trim extra spaces
    return '\n'.join(lines)

def remove_personal_details(text):
    patterns = [
        r"Patient Name\s*:\s*[A-Za-z\s]+",
        r"Patient UID No\s*:\s*\w+",
        r"Age and Gender\s*:\s*\d+\s*Years\s*/\s*[A-Za-z]+",
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text)
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove blank lines
    return text.strip()
