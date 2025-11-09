from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Project, User

projects_bp = Blueprint("projects", __name__)

@projects_bp.post("")
@jwt_required()
def create_project():
    data = request.get_json() or {}
    ident = get_jwt_identity()
    owner_id = data.get("owner_id", ident["id"])
    if not User.query.get(owner_id):
        return {"error":"owner not found"}, 404
    p = Project(
        name=data["name"],
        description=data.get("description"),
        status=data.get("status","ongoing"),
        owner_id=owner_id
    )
    db.session.add(p)
    db.session.commit()
    return {"id": p.id, "name": p.name}, 201

@projects_bp.get("")
@jwt_required()
def list_projects():
    items = Project.query.all()
    return [{"id":p.id,"name":p.name,"status":p.status} for p in items]

@projects_bp.get("/<int:pid>")
@jwt_required()
def get_project(pid):
    p = Project.query.get_or_404(pid)
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "status": p.status,
        "owner_id": p.owner_id
    }

@projects_bp.put("/<int:pid>")
@jwt_required()
def update_project(pid):
    p = Project.query.get_or_404(pid)
    data = request.get_json() or {}
    for attr in ["name","description","status","start_date","end_date"]:
        if attr in data: setattr(p, attr, data[attr])
    db.session.commit()
    return {"ok": True}

@projects_bp.delete("/<int:pid>")
@jwt_required()
def delete_project(pid):
    p = Project.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return {"ok": True}
