from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from ..models import db, Task, TimeLog

kpi_bp = Blueprint("kpi", __name__)

@kpi_bp.get("/burndown")
@jwt_required()
def burndown():
    # Total estimado vs. horas registradas (simple burndown global)
    total_est = db.session.query(func.coalesce(func.sum(Task.estimated_hours),0.0)).scalar() or 0.0
    total_logged = db.session.query(func.coalesce(func.sum(TimeLog.hours_logged),0.0)).scalar() or 0.0
    return {"estimated_total": float(total_est), "logged_total": float(total_logged), "remaining": float(max(total_est - total_logged, 0.0))}

@kpi_bp.get("/throughput")
@jwt_required()
def throughput():
    # Conteo de tareas por estado (throughput)
    counts = (
        db.session.query(Task.state_kanban, func.count(Task.id))
        .group_by(Task.state_kanban)
        .all()
    )
    return {state:int(c) for state,c in counts}
