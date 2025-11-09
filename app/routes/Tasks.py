from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..models import db, Task, Project, User, Sprint

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.post("")
@jwt_required()
def create():
    data = request.get_json() or {}
    if not Project.query.get(data.get("project_id")):
        return {"error":"project not found"}, 404
    if data.get("assigned_to_id") and not User.query.get(data["assigned_to_id"]):
        return {"error":"assignee not found"}, 404
    if data.get("sprint_id") and not Sprint.query.get(data["sprint_id"]):
        return {"error":"sprint not found"}, 404
    t = Task(
        name=data["name"],
        description=data.get("description"),
        state_kanban=data.get("state_kanban","to_do"),
        priority=data.get("priority","medium"),
        estimated_hours=data.get("estimated_hours"),
        project_id=data["project_id"],
        assigned_to_id=data.get("assigned_to_id"),
        sprint_id=data.get("sprint_id"),
    )
    db.session.add(t)
    db.session.commit()
    return {"id": t.id, "name": t.name}, 201

@tasks_bp.get("")
@jwt_required()
def list_():
    q = Task.query
    project_id = request.args.get("project_id", type=int)
    if project_id: q = q.filter_by(project_id=project_id)
    return [{
        "id":t.id, "name":t.name, "state":t.state_kanban, "priority":t.priority,
        "project_id":t.project_id, "assigned_to_id":t.assigned_to_id, "sprint_id":t.sprint_id
    } for t in q.all()]

@tasks_bp.put("/<int:tid>")
@jwt_required()
def update(tid):
    t = Task.query.get_or_404(tid)
    data = request.get_json() or {}
    for attr in ["name","description","state_kanban","priority","estimated_hours","assigned_to_id","sprint_id","start_date","end_date"]:
        if attr in data: setattr(t, attr, data[attr])
    db.session.commit()
    return {"ok": True}

# Kanban: mover de columna
@tasks_bp.post("/<int:tid>/move")
@jwt_required()
def move_kanban(tid):
    t = Task.query.get_or_404(tid)
    data = request.get_json() or {}
    new_state = data.get("state")
    if new_state not in {"to_do","in_progress","done"}:
        return {"error":"invalid state"}, 400
    t.state_kanban = new_state
    db.session.commit()
    return {"id": t.id, "state": t.state_kanban}
