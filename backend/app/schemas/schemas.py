from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = "conv-factures"
    query: str
    experience_level: Optional[str] = Field(
        default="SENIOR_EXPERT",
        description="Niveau d'expertise de l'agent: JUNIOR, STANDARD, SENIOR_EXPERT"
    )

class StagedActionDTO(BaseModel):
    action_id: str
    action_type: str
    criticality: str
    status: str
    title: str
    description: Optional[str] = None
    consequence_warning: str
    target_count: int
    financial_amount: Optional[float] = None
    channel: str
    requested_by: str
    payload: Dict[str, Any] = {}

class ActionDecisionRequest(BaseModel):
    reason: Optional[str] = None

class BatchValidationRequest(BaseModel):
    action_ids: List[str]

class DataSourceDTO(BaseModel):
    id: str
    name: str
    type: str
    record_count: int
    last_synced_at: str
    status: str
    is_connected: bool = True

class AuditLogDTO(BaseModel):
    id: str
    timestamp: str
    user: str
    query: str
    tool: str
    action: str
    status: str
    details: Dict[str, Any] = {}

class SettingsDTO(BaseModel):
    require_hitl_emails: bool = True
    require_hitl_data_mutation: bool = True
    require_hitl_exports: bool = True
    financial_base_connected: bool = True
    messaging_connected: bool = True

class ConnectivityStatus(BaseModel):
    mode: str # "local" or "online"
    gemini_active: bool
    resend_active: bool
    database_type: str
    is_online: bool

class DashboardStatsDTO(BaseModel):
    queries_count: int
    actions_count: int
    pending_count: int
    completed_count: int

class DsoMetricsDTO(BaseModel):
    current_dso_days: float
    prior_dso_days: float
    target_dso_days: float
    cash_freed_eur: float
    days_reduced: float
    average_overdue_days: float
    unpaid_total_amount: float

class ParetoDecileDTO(BaseModel):
    decile_label: str
    clients_count: int
    amount_eur: float
    percentage_of_total: float
    cumulative_percentage: float

class TopRiskClientDTO(BaseModel):
    name: str
    amount: float
    cumulative_percentage: float
    invoices_count: int

class AdvancedAnalyticsDTO(BaseModel):
    dso: DsoMetricsDTO
    pareto: List[ParetoDecileDTO]
    top_risk_clients: List[TopRiskClientDTO]
    pareto_insight: str
