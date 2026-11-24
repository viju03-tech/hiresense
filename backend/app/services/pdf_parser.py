import fitz


def extract_pdf_text(file_path: str) -> str:
    chunks = []
    with fitz.open(file_path) as document:
        for page in document:
            chunks.append(page.get_text())
    return "\n".join(chunks).strip()
