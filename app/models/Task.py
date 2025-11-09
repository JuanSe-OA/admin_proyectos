from datetime import datetime
from . import db

class Task(db.Model):
    __tablename__ = "tasks"
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(150), nullable=False)
    description    = db.Column(db.Text)
    state_kanban   = db.Column(db.String(30), default="to_do")   # to_do|in_progress|done
    priority       = db.Column(db.String(30), default="medium")  # low|medium|high
    estimated_hours= db.Column(db.Float)
    start_date     = db.Column(db.DateTime, default=datetime.utcnow)
    end_date       = db.Column(db.DateTime)

    project_id     = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sprint_id      = db.Column(db.Integer, db.ForeignKey("sprints.id"))

    project  = db.relationship("Project", back_populates="tasks")
    assignee = db.relationship("User", back_populates="tasks_assigned", foreign_keys=[assigned_to_id])
    sprint   = db.relationship("Sprint", back_populates="tasks")
    time_logs = db.relationship("TimeLog", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task {self.name}>"
