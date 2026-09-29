import json

from app.ai.state import ComplaintState
from app.ai.prompts import (
    COMPLAINT_EXTRACTION_SYSTEM_PROMPT,
    COMPLAINT_EXTRACTION_USER_PROMPT,
)
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.complaint import Complaint

from groq import Groq


client = Groq(api_key=settings.GROQ_API_KEY)


# ============================================================
# COMPLAINT EXTRACTION SCHEMA
# ============================================================

COMPLAINT_SCHEMA = {
    "type": "object",
    "properties": {
        "complaint_source": {"type": ["string", "null"]},
        "customer_name": {"type": ["string", "null"]},
        "product_name": {"type": ["string", "null"]},
        "product_strength_grade": {"type": ["string", "null"]},
        "batch_number": {"type": ["string", "null"]},
        "manufacturing_date": {"type": ["string", "null"]},
        "expiry_date": {"type": ["string", "null"]},
        "quantity_affected": {"type": ["integer", "null"]},
        "complaint_type": {"type": ["string", "null"]},
        "complaint_date": {"type": ["string", "null"]},
        "detailed_description": {"type": ["string", "null"]},
        "initial_severity": {"type": ["string", "null"]},
        "priority": {"type": ["string", "null"]},
    },
    "required": [
        "complaint_source",
        "customer_name",
        "product_name",
        "product_strength_grade",
        "batch_number",
        "manufacturing_date",
        "expiry_date",
        "quantity_affected",
        "complaint_type",
        "complaint_date",
        "detailed_description",
        "initial_severity",
        "priority",
    ],
    "additionalProperties": False,
}


# ============================================================
# 1. EXTRACT COMPLAINT
# ============================================================

def extract_complaint(state: ComplaintState) -> ComplaintState:
    """
    Extract structured complaint information from the supplied text.
    """

    complaint_text = state.get("complaint_text", "").strip()

    if not complaint_text:
        return {
            **state,
            "error": "Complaint text is empty.",
        }

    user_prompt = COMPLAINT_EXTRACTION_USER_PROMPT.format(
        complaint_text=complaint_text
    )

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": COMPLAINT_EXTRACTION_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "complaint_extraction",
                    "strict": True,
                    "schema": COMPLAINT_SCHEMA,
                },
            },
            temperature=0,
        )

        content = response.choices[0].message.content

        extracted_data = json.loads(content)

        return {
            **state,
            "extracted_data": extracted_data,
            "error": None,
        }

    except Exception as exc:
        return {
            **state,
            "error": f"Complaint extraction failed: {str(exc)}",
        }


# ============================================================
# 2. COMPLETENESS CHECKER
# ============================================================

def check_completeness(state: ComplaintState) -> ComplaintState:
    """
    Check whether the extracted complaint contains the
    minimum information required for complaint intake.
    """

    extracted_data = state.get("extracted_data", {})

    required_fields = [
        "customer_name",
        "product_name",
        "batch_number",
        "complaint_type",
        "complaint_date",
        "detailed_description",
    ]

    missing_fields = []

    for field in required_fields:
        value = extracted_data.get(field)

        if value is None or str(value).strip() == "":
            missing_fields.append(field)

    return {
        **state,
        "missing_fields": missing_fields,
        "is_complete": len(missing_fields) == 0,
        "error": None,
    }


# ============================================================
# 3. COMPLAINT CLASSIFICATION
# ============================================================

def classify_complaint(state: ComplaintState) -> ComplaintState:
    """
    Classify the complaint based on the extracted complaint information.
    """

    extracted_data = state.get("extracted_data", {})

    complaint_type = extracted_data.get("complaint_type")
    description = extracted_data.get("detailed_description")

    if not complaint_type and not description:
        return {
            **state,
            "error": "Not enough information to classify complaint.",
        }

    text = f"""
Complaint Type: {complaint_type}
Description: {description}
"""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
You are a pharmaceutical customer complaint classification assistant.

Classify the complaint into one of these categories:

- Product Quality
- Packaging
- Labeling
- Delivery
- Documentation
- Adverse Event
- Other

Also determine:

Severity:
- Minor
- Major
- Critical

Priority:
- Low
- Medium
- High
- Critical

Rules:
1. Use only information contained in the complaint.
2. Do not invent facts.
3. If the information is insufficient, choose the most conservative
   reasonable classification.
4. Return only the requested structured data.
""",
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "complaint_classification",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "complaint_category": {
                                "type": "string",
                                "enum": [
                                    "Product Quality",
                                    "Packaging",
                                    "Labeling",
                                    "Delivery",
                                    "Documentation",
                                    "Adverse Event",
                                    "Other",
                                ],
                            },
                            "severity": {
                                "type": "string",
                                "enum": [
                                    "Minor",
                                    "Major",
                                    "Critical",
                                ],
                            },
                            "priority": {
                                "type": "string",
                                "enum": [
                                    "Low",
                                    "Medium",
                                    "High",
                                    "Critical",
                                ],
                            },
                        },
                        "required": [
                            "complaint_category",
                            "severity",
                            "priority",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            temperature=0,
        )

        classification = json.loads(
            response.choices[0].message.content
        )

        return {
            **state,
            "complaint_category": classification["complaint_category"],
            "severity": classification["severity"],
            "priority": classification["priority"],
            "error": None,
        }

    except Exception as exc:
        return {
            **state,
            "error": f"Complaint classification failed: {str(exc)}",
        }


# ============================================================
# 4. RISK ASSESSMENT
# ============================================================

def assess_risk(state: ComplaintState) -> ComplaintState:
    """
    Assess the complaint risk based on extracted information
    and the AI classification.
    """

    extracted_data = state.get("extracted_data", {})

    complaint_category = state.get("complaint_category")
    severity = state.get("severity")
    priority = state.get("priority")

    description = extracted_data.get("detailed_description")

    if not description:
        return {
            **state,
            "error": "Complaint description is missing for risk assessment.",
        }

    complaint_context = f"""
Complaint Category: {complaint_category}
Severity: {severity}
Priority: {priority}
Complaint Description: {description}
"""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI Risk Assessment Assistant for a pharmaceutical
customer complaint management system.

Assess the potential risk of the complaint.

Risk levels:
- LOW
- MEDIUM
- HIGH
- CRITICAL

Provide:
1. risk_level
2. risk_reason
3. recommended_investigation

Important rules:
- Base the assessment only on information provided.
- Do not invent medical, regulatory, or product facts.
- This is an AI recommendation for human review.
- Do not make a final regulatory or quality decision.
- Explain why the selected risk level was assigned.
""",
                },
                {
                    "role": "user",
                    "content": complaint_context,
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "risk_assessment",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "risk_level": {
                                "type": "string",
                                "enum": [
                                    "LOW",
                                    "MEDIUM",
                                    "HIGH",
                                    "CRITICAL",
                                ],
                            },
                            "risk_reason": {
                                "type": "string",
                            },
                            "recommended_investigation": {
                                "type": "string",
                            },
                        },
                        "required": [
                            "risk_level",
                            "risk_reason",
                            "recommended_investigation",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            temperature=0,
        )

        risk_data = json.loads(
            response.choices[0].message.content
        )

        return {
            **state,
            "risk_level": risk_data["risk_level"],
            "risk_reason": risk_data["risk_reason"],
            "error": None,
        }

    except Exception as exc:
        return {
            **state,
            "error": f"Risk assessment failed: {str(exc)}",
        }


# ============================================================
# 5. COMPLAINT SUMMARY
# ============================================================

def generate_summary(state: ComplaintState) -> ComplaintState:
    """
    Generate a concise summary of the customer complaint.
    """

    extracted_data = state.get("extracted_data", {})

    description = extracted_data.get("detailed_description")

    if not description:
        return {
            **state,
            "error": "Complaint description is missing for summary.",
        }

    complaint_context = f"""
Customer: {extracted_data.get("customer_name")}
Product: {extracted_data.get("product_name")}
Strength/Grade: {extracted_data.get("product_strength_grade")}
Batch: {extracted_data.get("batch_number")}
Complaint Type: {state.get("complaint_category")}
Severity: {state.get("severity")}
Priority: {state.get("priority")}
Risk: {state.get("risk_level")}

Description:
{description}
"""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI complaint summary assistant for a pharmaceutical
customer complaint management system.

Create a concise factual summary of the complaint.

Rules:
1. Use only information provided.
2. Do not invent facts.
3. Include the product, batch, complaint issue, and reported impact
   when available.
4. Keep the summary professional and suitable for a quality-management
   workflow.
5. Do not make a final regulatory or quality decision.
""",
                },
                {
                    "role": "user",
                    "content": complaint_context,
                },
            ],
            temperature=0,
        )

        summary = response.choices[0].message.content.strip()

        return {
            **state,
            "summary": summary,
            "error": None,
        }

    except Exception as exc:
        return {
            **state,
            "error": f"Complaint summary failed: {str(exc)}",
        }


# ============================================================
# 6. DUPLICATE COMPLAINT DETECTION
# ============================================================

def detect_duplicate_complaints(state: ComplaintState) -> ComplaintState:
    """
    Detect possible duplicate complaints using existing complaints
    stored in PostgreSQL.

    Matching is based on product name and batch number.
    """

    extracted_data = state.get("extracted_data", {})

    product_name = extracted_data.get("product_name")
    batch_number = extracted_data.get("batch_number")
    description = extracted_data.get("detailed_description")

    if not description:
        return {
            **state,
            "possible_duplicate": False,
            "duplicate_complaint_ids": [],
            "duplicate_reason": "Complaint description is missing.",
            "error": None,
        }

    db = SessionLocal()

    try:
        query = db.query(Complaint)

        # Match product when available
        if product_name:
            query = query.filter(
                Complaint.product_name == product_name
            )

        # Match batch when available
        if batch_number:
            query = query.filter(
                Complaint.batch_number == batch_number
            )

        existing_complaints = query.all()

        if not existing_complaints:
            return {
                **state,
                "possible_duplicate": False,
                "duplicate_complaint_ids": [],
                "duplicate_reason": (
                    "No existing complaint with matching "
                    "product and batch was found."
                ),
                "error": None,
            }

        duplicate_ids = [
            complaint.id
            for complaint in existing_complaints
        ]

        return {
            **state,
            "possible_duplicate": True,
            "duplicate_complaint_ids": duplicate_ids,
            "duplicate_reason": (
                "An existing complaint was found with matching "
                "product and batch information. Human review is "
                "recommended to determine whether the complaints "
                "are duplicates."
            ),
            "error": None,
        }

    except Exception as exc:
        return {
            **state,
            "possible_duplicate": False,
            "duplicate_complaint_ids": [],
            "duplicate_reason": "",
            "error": f"Duplicate detection failed: {str(exc)}",
        }

    finally:
        db.close()