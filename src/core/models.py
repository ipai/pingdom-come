from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CloudflareMetrics(BaseModel):
    """Model to store daily Cloudflare analytics data."""

    __tablename__ = "cloudflare_metrics"

    date = Column(Date, nullable=False, unique=True)
    total_requests = Column(Integer, nullable=False)
    bandwidth_used = Column(Integer, nullable=False)  # in bytes
    top_countries = Column(JSONB)
    top_pages = Column(JSONB)

    __table_args__ = (Index("idx_metrics_date", "date"),)


class ReportSchedule(BaseModel):
    """Model to store report generation schedules."""

    __tablename__ = "report_schedules"

    report_type = Column(String(50), nullable=False)  # daily, weekly
    enabled = Column(Boolean, default=True)
    day_of_week = Column(String(10))  # For weekly reports
    time_of_day = Column(String(5), nullable=False)  # HH:MM format
    recipients = Column(JSONB)  # List of email addresses

    __table_args__ = (UniqueConstraint("report_type", name="uq_report_type"),)
