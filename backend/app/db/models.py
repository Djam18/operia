import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.database import Base

def get_utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False, default="")
    full_name = Column(String, nullable=False)
    role = Column(String, default="OPERATOR")
    department = Column(String, default="Direction financière")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_utc_now)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    contact_email = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    country = Column(String, default="Côte d'Ivoire", index=True)
    city = Column(String, default="Abidjan")
    region = Column(String, default="Afrique de l'Ouest", index=True) # Afrique de l'Ouest, Afrique du Nord, Afrique Centrale, Afrique de l'Est, Europe
    currency = Column(String, default="XOF", index=True) # XOF, MAD, XAF, NGN, KES, EUR, USD
    has_dispute = Column(Boolean, default=False)
    dispute_reason = Column(String, nullable=True)
    dunning_eligible = Column(Boolean, default=True)
    credit_limit = Column(Float, default=50000.0)
    payment_terms_days = Column(Integer, default=30)

class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = (
        Index("idx_invoices_status_days", "status", "days_overdue"),
        Index("idx_invoices_region_curr", "region", "currency"),
    )
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"), index=True)
    customer_name = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="EUR", index=True)
    region = Column(String, default="Europe", index=True)
    days_overdue = Column(Integer, nullable=False, index=True)
    status = Column(String, default="impaye", index=True) # impaye, partiel, paye
    issue_date = Column(String)
    due_date = Column(String)

class StagedAction(Base):
    __tablename__ = "staged_actions"
    __table_args__ = (
        Index("idx_staged_actions_status", "status"),
    )
    action_id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=True)
    action_type = Column(String, nullable=False) # RELANCE_EMAIL, EXPORT_CSV, REPORT, UPDATE_PRIORITY
    criticality = Column(String, default="SENSITIVE") # SENSITIVE, STANDARD
    status = Column(String, default="PENDING") # PENDING, COMPLETED, REFUSED, FAILED
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    consequence_warning = Column(Text, nullable=False)
    target_count = Column(Integer, default=1)
    financial_amount = Column(Float, nullable=True)
    currency = Column(String, default="EUR")
    channel = Column(String, default="Email")
    requested_by = Column(String, default="Alex Martin")
    payload = Column(JSON, default={})
    created_at = Column(DateTime, default=get_utc_now)
    resolved_at = Column(DateTime, nullable=True)

class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    record_count = Column(Integer, default=0)
    last_synced_at = Column(String, nullable=False)
    status = Column(String, default="COMPLETED") # COMPLETED, IN_PROGRESS, ERROR
    is_connected = Column(Boolean, default=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_audit_logs_timestamp", "timestamp"),
    )
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(String, nullable=False)
    user = Column(String, nullable=False)
    query = Column(String, nullable=False)
    tool = Column(String, nullable=False)
    action = Column(String, nullable=False)
    status = Column(String, default="PENDING") # PENDING, COMPLETED, FAILED, REFUSED
    details = Column(JSON, default={})

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now)

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    sender = Column(String, nullable=False) # user, assistant, system
    content = Column(Text, nullable=False)
    meta = Column(JSON, default={})
    created_at = Column(DateTime, default=get_utc_now)

class OutboxEmail(Base):
    __tablename__ = "outbox_emails"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    recipient_email = Column(String, nullable=False)
    recipient_name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body_html = Column(Text, nullable=False)
    amount = Column(Float, nullable=True)
    currency = Column(String, default="EUR")
    delivery_mode = Column(String, default="local_sandbox") # local_sandbox, local_smtp, resend
    status = Column(String, default="DELIVERED_LOCAL")
    created_at = Column(DateTime, default=get_utc_now)

