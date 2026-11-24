from docx import Document


def extract_docx_text(file_path: str) -> str:
    document = Document(file_path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs]
    table_text = [
        cell.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
    ]
    return "\n".join(paragraphs + table_text).strip()
