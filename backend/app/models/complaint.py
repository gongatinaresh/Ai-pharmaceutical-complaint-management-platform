from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Pending Triage"
    )

    # Origin & Customer Details
    complaint_source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    customer_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    # Product & Batch Identification
    product_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    product_strength_grade: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    batch_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    manufacturing_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    quantity_affected: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # Complaint Details
    complaint_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    complaint_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    detailed_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # Initial Assessment
    initial_severity: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    priority: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )