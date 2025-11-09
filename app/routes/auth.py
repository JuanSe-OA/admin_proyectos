from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    required = {"username","email","password","role"}
    if not required.issubset(data):
        return {"error":"missing fields"}, 400

    if User.query.filter((User.username==data["username"]) | (User.email==data["email"])).first():
        return {"error":"user exists"}, 409

    u = User(username=data["username"], email=data["email"], role=data.get("role","user"))
    u.set_password(data["password"])
    db.session.add(u)
    db.session.commit()
    return {"id": u.id, "username": u.username, "email": u.email, "role": u.role}, 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password","")):
        return {"error":"invalid credentials"}, 401
    token = create_access_token(identity={"id": user.id, "role": user.role})
    return {"access_token": token, "user": {"id": user.id, "username": user.username, "role": user.role}}

@auth_bp.get("/me")
@jwt_required()
def me():
    ident = get_jwt_identity()
    user = User.query.get_or_404(ident["id"])
    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
