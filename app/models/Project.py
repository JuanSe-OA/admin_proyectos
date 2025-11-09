from datetime import datetime
from . import db

class Project(db.Model):
    __tablename__ = "projects"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    start_date  = db.Column(db.DateTime, default=datetime.utcnow)
    end_date    = db.Column(db.DateTime)
    status      = db.Column(db.String(30), default="ongoing")  # ongoing|paused|done
    owner_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    sprints = db.relationship("Sprint", back_populates="project", cascade="all, delete-orphan")
    tasks   = db.relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project {self.name}>"
