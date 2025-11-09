from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from ..models import db, Project, Task, TimeLog

reports_bp = Blueprint("reports", __name__)

@reports_bp.get("/summary")
@jwt_required()
def summary():
    # Horas por proyecto y tareas completadas por proyecto
    hours_by_project = (
        db.session.query(Project.id, Project.name, func.coalesce(func.sum(TimeLog.hours_logged),0.0))
        .outerjoin(Task, Task.project_id == Project.id)
        .outerjoin(TimeLog, TimeLog.task_id == Task.id)
        .group_by(Project.id, Project.name)
        .all()
    )
    done_by_project = (
        db.session.query(Project.id, func.count(Task.id))
        .outerjoin(Task, Task.project_id == Project.id)
        .filter(Task.state_kanban == "done")
        .group_by(Project.id)
        .all()
    )
    done_map = {pid:c for pid,c in done_by_project}
    return [{
        "project_id": pid,
        "project": name,
        "hours_logged": float(hours),
        "tasks_done": int(done_map.get(pid, 0))
    } for pid,name,hours in hours_by_project]
