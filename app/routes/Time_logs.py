from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, TimeLog, Task

time_bp = Blueprint("time", __name__)

@time_bp.post("")
@jwt_required()
def log_time():
    data = request.get_json() or {}
    ident = get_jwt_identity()
    if data.get("task_id") and not Task.query.get(data["task_id"]):
        return {"error":"task not found"}, 404
    tl = TimeLog(
        hours_logged = data["hours_logged"],
        description  = data.get("description"),
        task_id      = data.get("task_id"),
        user_id      = ident["id"]
    )
    db.session.add(tl)
    db.session.commit()
    return {"id": tl.id}, 201

@time_bp.get("")
@jwt_required()
def list_time():
    items = TimeLog.query.all()
    return [{"id":i.id,"hours":i.hours_logged,"task_id":i.task_id,"user_id":i.user_id,"date":i.date.isoformat()} for i in items]
