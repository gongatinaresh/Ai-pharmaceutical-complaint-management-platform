from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate


router = APIRouter(
    prefix="/api/complaints",
    tags=["Complaints"]
)


# ---------------------------------------------------------
# CREATE COMPLAINT
# ---------------------------------------------------------

@router.post("/")
def create_complaint(
    complaint_data: ComplaintCreate,
    db: Session = Depends(get_db)
):
    complaint = Complaint(
        **complaint_data.model_dump()
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return {
        "message": "Complaint created successfully",
        "complaint_id": complaint.id
    }


# ---------------------------------------------------------
# GET ALL COMPLAINTS
# ---------------------------------------------------------

@router.get("/")
def get_complaints(
    db: Session = Depends(get_db)
):
    complaints = db.query(Complaint).all()

    return complaints


# ---------------------------------------------------------
# GET ONE COMPLAINT
# ---------------------------------------------------------

@router.get("/{complaint_id}")
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    return complaint


# ---------------------------------------------------------
# UPDATE COMPLAINT
# ---------------------------------------------------------

@router.put("/{complaint_id}")
def update_complaint(
    complaint_id: int,
    complaint_data: ComplaintUpdate,
    db: Session = Depends(get_db)
):
    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    update_data = complaint_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(complaint, field, value)

    db.commit()
    db.refresh(complaint)

    return {
        "message": "Complaint updated successfully",
        "complaint_id": complaint.id
    }


# ---------------------------------------------------------
# DELETE COMPLAINT
# ---------------------------------------------------------

@router.delete("/{complaint_id}")
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    db.delete(complaint)
    db.commit()

    return {
        "message": "Complaint deleted successfully",
        "complaint_id": complaint_id
    }