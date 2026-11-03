import pymupdf

def extract_pdf(file_path):
    with pymupdf.open(file_path) as pdf:
        text = ""

        for page in pdf:
            text += page.get_text()

    return text