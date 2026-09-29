from typing import Any, TypedDict


class ComplaintState(TypedDict, total=False):
    # Original complaint text
    complaint_text: str

    # AI-extracted complaint fields
    extracted_data: dict[str, Any]

    # Fields that are missing or incomplete
    missing_fields: list[str]

    # Whether the complaint contains enough information
    is_complete: bool

    # AI classification
    complaint_category: str
    severity: str
    priority: str

    # AI risk assessment
    risk_level: str
    risk_reason: str

    # Final AI-generated summary
    summary: str

    # Errors encountered during processing
    error: str | None
    # Duplicate complaint detection
    possible_duplicate: bool
    duplicate_complaint_ids: list[int]
    duplicate_reason: str