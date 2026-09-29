from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.graph import complaint_graph


router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)


class ComplaintTextRequest(BaseModel):
    complaint_text: str


@router.post("/process")
def process_complaint_text(
    request: ComplaintTextRequest
):
    if not request.complaint_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Complaint text cannot be empty."
        )

    try:
        result = complaint_graph.invoke(
            {
                "complaint_text": request.complaint_text
            }
        )

        return {
            "ai_result": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI complaint processing failed: {str(exc)}"
        )