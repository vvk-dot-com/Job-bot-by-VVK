
from pathlib import Path
import fitz  # PyMuPDF


def extract_resume_text(pdf_path: str) -> dict:
    """
    Extract text from a PDF resume using PyMuPDF.
    Returns extracted text and page count.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume not found: {path.resolve()}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF resumes are supported currently.")

    document = fitz.open(path)

    try:
        pages = []

        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text("text")
            pages.append(
                f"--- PAGE {page_number} ---\n{page_text}"
            )

        full_text = "\n".join(pages).strip()

        if not full_text:
            raise ValueError(
                "No text extracted. The PDF may be scanned."
            )

        return {
            "file_name": path.name,
            "page_count": len(document),
            "text": full_text,
        }

    finally:
        document.close()


def save_extracted_text(text: str, output_path: str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
