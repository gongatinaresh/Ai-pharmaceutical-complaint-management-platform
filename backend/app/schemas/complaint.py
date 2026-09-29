from datetime import date

from pydantic import BaseModel


class ComplaintCreate(BaseModel):
    complaint_source: str | None = None
    customer_name: str | None = None

    product_name: str | None = None
    product_strength_grade: str | None = None
    batch_number: str | None = None
    manufacturing_date: date | None = None
    expiry_date: date | None = None
    quantity_affected: int | None = None

    complaint_type: str | None = None
    complaint_date: date | None = None
    detailed_description: str | None = None

    initial_severity: str | None = None
    priority: str | None = None


class ComplaintUpdate(BaseModel):
    complaint_source: str | None = None
    customer_name: str | None = None

    product_name: str | None = None
    product_strength_grade: str | None = None
    batch_number: str | None = None
    manufacturing_date: date | None = None
    expiry_date: date | None = None
    quantity_affected: int | None = None

    complaint_type: str | None = None
    complaint_date: date | None = None
    detailed_description: str | None = None

    initial_severity: str | None = None
    priority: str | None = None

    status: str | None = None