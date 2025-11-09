from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..models import db, Sprint, Project

sprints_bp = Blueprint("sprints", __name__)

@sprints_bp.post("")
@jwt_required()
def create():
    data = request.get_json() or {}
    if not Project.query.get(data.get("project_id")):
        return {"error":"project not found"}, 404
    s = Sprint(
        name=data["name"],
        objective=data.get("objective"),
        status=data.get("status","planned"),
        project_id=data["project_id"]
    )
    db.session.add(s)
    db.session.commit()
    return {"id": s.id, "name": s.name}, 201

@sprints_bp.get("")
@jwt_required()
def list_():
    sprints = Sprint.query.all()
    return [{"id":s.id,"name":s.name,"status":s.status,"project_id":s.project_id} for s in sprints]
