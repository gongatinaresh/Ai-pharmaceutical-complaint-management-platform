from pathlib import Path
import fitz


def extract_text_from_pdf(file_path: str) -> str:
    document = fitz.open(file_path)

    try:
        pages = []

        for page in document:
            text = page.get_text()

            if text:
                pages.append(text)

        return "\n".join(pages).strip()

    finally:
        document.close()


def extract_text_from_txt(file_path: str) -> str:
    return Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    ).strip()


def extract_text_from_eml(file_path: str) -> str:
    from email import policy
    from email.parser import BytesParser

    with open(file_path, "rb") as file:
        message = BytesParser(
            policy=policy.default
        ).parse(file)

    parts = []

    if message["subject"]:
        parts.append(
            f"Subject: {message['subject']}"
        )

    if message["from"]:
        parts.append(
            f"From: {message['from']}"
        )

    if message["to"]:
        parts.append(
            f"To: {message['to']}"
        )

    if message.is_multipart():

        for part in message.walk():

            if part.get_content_type() == "text/plain":

                content = part.get_content()

                if content:
                    parts.append(content)

    else:

        content = message.get_content()

        if content:
            parts.append(content)

    return "\n".join(parts).strip()


def extract_text_from_docx(file_path: str) -> str:
    from docx import Document

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()


def extract_text(
    file_path: str,
    file_extension: str
) -> str:

    extension = file_extension.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".txt":
        return extract_text_from_txt(file_path)

    if extension == ".eml":
        return extract_text_from_eml(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(
        "Unsupported file type. "
        "Supported formats: PDF, DOCX, TXT, EML."
    )