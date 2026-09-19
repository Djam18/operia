from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.models import StagedAction, AuditLog, Customer
from app.mcp.tools import execute_bulk_relance, generate_csv_export

def get_now_formatted():
    now = datetime.now(timezone.utc)
    return now.strftime("%d %b · %H:%M")

class OperationsService:
    @staticmethod
    async def get_all_operations(db: AsyncSession, status_filter: Optional[str] = None) -> List[StagedAction]:
        query = select(StagedAction).order_by(StagedAction.created_at.desc())
        if status_filter and status_filter.upper() != "TOUTES":
            status_map = {
                "EN ATTENTE": "PENDING",
                "TERMINÉES": "COMPLETED",
                "PENDING": "PENDING",
                "COMPLETED": "COMPLETED",
                "REFUSED": "REFUSED"
            }
            mapped_status = status_map.get(status_filter.upper(), status_filter.upper())
            query = query.where(StagedAction.status == mapped_status)
            
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def validate_operation(
        db: AsyncSession,
        action_id: str,
        validator_name: str = "Alex Martin",
        confirm_override: bool = False
    ) -> Dict[str, Any]:
        result = await db.execute(select(StagedAction).where(StagedAction.action_id == action_id))
        action = result.scalars().first()
        if not action:
            raise ValueError(f"Action {action_id} non trouvée.")
        
        if action.status == "COMPLETED":
            return {"action_id": action_id, "status": "COMPLETED", "message": "Action déjà exécutée."}

        # 1. Execute sensitive operation based on type
        exec_result = {}
        payload = action.payload or {}

        if action.action_type == "RELANCE_EMAIL":
            exec_result = await execute_bulk_relance(payload, db=db)
            if exec_result.get("circuit_breaker") == "OPEN":
                return {
                    "action_id": action_id,
                    "status": "BLOCKED",
                    "error": exec_result.get("error"),
                    "message": exec_result.get("message")
                }

        elif action.action_type == "EXPORT_CSV":
            exec_result = await generate_csv_export(db, payload)
            if exec_result.get("circuit_breaker") == "OPEN":
                return {
                    "action_id": action_id,
                    "status": "BLOCKED",
                    "error": exec_result.get("error"),
                    "message": exec_result.get("message")
                }

        elif action.action_type == "AJUSTEMENT_ENCOURS":
            client_name = payload.get("client") or payload.get("customer_name")
            new_limit = payload.get("new_limit") or action.financial_amount
            
            # Double validation requirement for high amounts (> 50 000 € / XOF equivalent)
            if action.financial_amount and action.financial_amount > 50000.0 and not confirm_override:
                return {
                    "action_id": action_id,
                    "status": "REQUIRES_DOUBLE_VALIDATION",
                    "threshold": 50000.0,
                    "amount": action.financial_amount,
                    "message": "Double validation requise : Ce montant dépasse 50 000 €. Veuillez confirmer la validation de niveau 2."
                }

            if client_name and new_limit is not None:
                cust_res = await db.execute(select(Customer).where(Customer.name.ilike(f"%{client_name}%")))
                cust = cust_res.scalars().first()
                if cust:
                    old_limit = cust.credit_limit
                    cust.credit_limit = float(new_limit)
                    exec_result = {
                        "status": "success",
                        "customer": cust.name,
                        "old_credit_limit": old_limit,
                        "new_credit_limit": cust.credit_limit,
                        "message": f"Plafond d'encours de '{cust.name}' mis à jour : {old_limit} -> {cust.credit_limit} {cust.currency}."
                    }
                else:
                    exec_result = {"status": "warning", "message": f"Entreprise '{client_name}' non trouvée dans le CRM."}
            else:
                exec_result = {"status": "success", "message": "Ajustement d'encours validé."}

        else:
            exec_result = {"status": "success", "mode": "local", "details": payload}

        # 2. Update action status
        action.status = "COMPLETED"
        action.resolved_at = datetime.now(timezone.utc)

        # 3. Create immutable Audit Log
        audit = AuditLog(
            timestamp=get_now_formatted(),
            user=validator_name,
            query=f"Validation HITL : {action.title}",
            tool=action.channel,
            action=action.title,
            status="COMPLETED",
            details=exec_result
        )
        db.add(audit)
        await db.commit()
        await db.refresh(action)

        return {
            "action_id": action.action_id,
            "status": action.status,
            "title": action.title,
            "execution": exec_result
        }

    @staticmethod
    async def refuse_operation(db: AsyncSession, action_id: str, reason: Optional[str] = None, validator_name: str = "Alex Martin") -> Dict[str, Any]:
        result = await db.execute(select(StagedAction).where(StagedAction.action_id == action_id))
        action = result.scalars().first()
        if not action:
            raise ValueError(f"Action {action_id} non trouvée.")

        action.status = "REFUSED"
        action.resolved_at = datetime.now(timezone.utc)

        audit = AuditLog(
            timestamp=get_now_formatted(),
            user=validator_name,
            query=f"Refus de l'action {action.title}",
            tool="Contrôle humain",
            action=f"Refusé ({reason or 'Sans motif'})",
            status="REFUSED",
            details={"reason": reason}
        )
        db.add(audit)
        await db.commit()
        await db.refresh(action)

        return {"action_id": action.action_id, "status": "REFUSED"}

    @staticmethod
    async def batch_validate(db: AsyncSession, action_ids: List[str], validator_name: str = "Alex Martin") -> Dict[str, Any]:
        results = []
        for aid in action_ids:
            try:
                res = await OperationsService.validate_operation(db, aid, validator_name)
                results.append(res)
            except Exception as e:
                results.append({"action_id": aid, "error": str(e)})
        return {"validated_count": len([r for r in results if "error" not in r and r.get("status") == "COMPLETED"]), "results": results}
