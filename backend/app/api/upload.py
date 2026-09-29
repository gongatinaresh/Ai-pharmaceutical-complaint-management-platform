import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ai.graph import complaint_graph
from app.services.document_service import extract_text


router = APIRouter(
    prefix="/api/upload",
    tags=["AI Complaint Intake"]
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".eml",
}


MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/complaint")
async def upload_complaint_document(
    file: UploadFile = File(...)
):
    """
    Upload a complaint document and process it
    through the AI complaint workflow.
    """

    filename = file.filename or ""

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload PDF, TXT, or EML."
            )
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10 MB."
        )

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temp_file.write(content)
            temp_path = temp_file.name

        complaint_text = extract_text(
            temp_path,
            extension
        )

        if not complaint_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the document."
            )

        result = complaint_graph.invoke(
            {
                "complaint_text": complaint_text
            }
        )

        return {
            "filename": filename,
            "extracted_text": complaint_text,
            "ai_result": result,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Complaint processing failed: {str(exc)}"
        )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)