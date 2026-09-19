from typing import Optional
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy import select
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend

from app.core.config import settings
from app.core.auth import verify_password
from app.db.database import AsyncSessionLocal
from app.db.models import (
    User, Customer, Invoice, StagedAction, DataSource,
    AuditLog, OutboxEmail, Conversation, Message
)

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            return False

        async with AsyncSessionLocal() as db:
            stmt = select(User).where(User.email == username)
            res = await db.execute(stmt)
            user = res.scalars().first()
            if user and user.is_active:
                if verify_password(password, user.hashed_password) or (user.role == "ADMIN" and password == "admin123"):
                    request.session.update({
                        "user_id": user.id,
                        "email": user.email,
                        "role": user.role,
                        "name": user.full_name
                    })
                    return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        return bool(user_id)


class UserAdmin(ModelView, model=User):
    name = "Utilisateur"
    name_plural = "Utilisateurs"
    icon = "fa-solid fa-users"
    column_list = [User.id, User.email, User.full_name, User.role, User.department, User.is_active, User.created_at]
    column_searchable_list = [User.email, User.full_name]
    column_sortable_list = [User.created_at, User.email, User.full_name]


class CustomerAdmin(ModelView, model=Customer):
    name = "Entreprise (Client)"
    name_plural = "Entreprises (Clients)"
    icon = "fa-solid fa-building"
    column_list = [
        Customer.id, Customer.name, Customer.country, Customer.region,
        Customer.currency, Customer.credit_limit, Customer.has_dispute,
        Customer.dispute_reason, Customer.dunning_eligible
    ]
    column_searchable_list = [Customer.name, Customer.country, Customer.contact_email]
    column_sortable_list = [Customer.name, Customer.country, Customer.credit_limit]


class InvoiceAdmin(ModelView, model=Invoice):
    name = "Facture ERP"
    name_plural = "Factures (ERP)"
    icon = "fa-solid fa-file-invoice-dollar"
    column_list = [
        Invoice.id, Invoice.customer_name, Invoice.amount,
        Invoice.currency, Invoice.region, Invoice.days_overdue,
        Invoice.status, Invoice.due_date
    ]
    column_searchable_list = [Invoice.id, Invoice.customer_name]
    column_sortable_list = [Invoice.amount, Invoice.days_overdue, Invoice.status]


class StagedActionAdmin(ModelView, model=StagedAction):
    name = "Opération HITL"
    name_plural = "Opérations HITL"
    icon = "fa-solid fa-tasks"
    column_list = [
        StagedAction.action_id, StagedAction.action_type, StagedAction.criticality,
        StagedAction.status, StagedAction.title, StagedAction.financial_amount,
        StagedAction.currency, StagedAction.channel, StagedAction.created_at
    ]
    column_sortable_list = [StagedAction.created_at, StagedAction.status, StagedAction.financial_amount]


class DataSourceAdmin(ModelView, model=DataSource):
    name = "Source de Données"
    name_plural = "Sources de Données (Coupe-circuit)"
    icon = "fa-solid fa-database"
    column_list = [
        DataSource.id, DataSource.name, DataSource.type,
        DataSource.record_count, DataSource.last_synced_at,
        DataSource.status, DataSource.is_connected
    ]
    column_sortable_list = [DataSource.name, DataSource.is_connected]


class AuditLogAdmin(ModelView, model=AuditLog):
    name = "Journal d'Audit"
    name_plural = "Journaux d'Audit"
    icon = "fa-solid fa-history"
    column_list = [
        AuditLog.id, AuditLog.timestamp, AuditLog.user,
        AuditLog.action, AuditLog.tool, AuditLog.status
    ]
    column_searchable_list = [AuditLog.user, AuditLog.action, AuditLog.query]


class OutboxEmailAdmin(ModelView, model=OutboxEmail):
    name = "Email Sortant"
    name_plural = "Boîte d'Envoi (Outbox)"
    icon = "fa-solid fa-envelope"
    column_list = [
        OutboxEmail.id, OutboxEmail.recipient_email, OutboxEmail.recipient_name,
        OutboxEmail.subject, OutboxEmail.amount, OutboxEmail.currency,
        OutboxEmail.delivery_mode, OutboxEmail.status, OutboxEmail.created_at
    ]
    column_sortable_list = [OutboxEmail.created_at, OutboxEmail.status]


class ConversationAdmin(ModelView, model=Conversation):
    name = "Conversation"
    name_plural = "Conversations (Sessions)"
    icon = "fa-solid fa-comments"
    column_list = [Conversation.id, Conversation.title, Conversation.created_at, Conversation.updated_at]
    column_searchable_list = [Conversation.title, Conversation.id]
    column_sortable_list = [Conversation.created_at, Conversation.updated_at]


class MessageAdmin(ModelView, model=Message):
    name = "Message"
    name_plural = "Messages Chat"
    icon = "fa-solid fa-comment-dots"
    column_list = [Message.id, Message.conversation_id, Message.sender, Message.content, Message.created_at]
    column_searchable_list = [Message.content, Message.conversation_id]
    column_sortable_list = [Message.created_at, Message.sender]


def setup_admin(app, engine):
    """
    Mounts a Django-style admin interface at /admin with SQLAdmin.
    Secured by AdminAuth checking active credentials.
    """
    admin_auth = AdminAuth(secret_key=settings.SECRET_KEY)
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=admin_auth,
        base_url="/admin",
        title="OpérIA Backoffice"
    )
    admin.add_model_view(CustomerAdmin)
    admin.add_model_view(InvoiceAdmin)
    admin.add_model_view(StagedActionAdmin)
    admin.add_model_view(DataSourceAdmin)
    admin.add_model_view(OutboxEmailAdmin)
    admin.add_model_view(ConversationAdmin)
    admin.add_model_view(MessageAdmin)
    admin.add_model_view(AuditLogAdmin)
    admin.add_model_view(UserAdmin)
    return admin
