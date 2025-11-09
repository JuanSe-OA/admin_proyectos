from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = "users"
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(120), unique=True, nullable=False)
    email       = db.Column(db.String(160), unique=True, nullable=False)
    password    = db.Column(db.String(255), nullable=False)
    role        = db.Column(db.String(30), nullable=False, default="user")  # admin|leader|user
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    tasks_assigned = db.relationship("Task", back_populates="assignee", cascade="all, delete-orphan", foreign_keys="Task.assigned_to_id")
    time_logs      = db.relationship("TimeLog", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def __repr__(self):
        return f"<User {self.username}>"
