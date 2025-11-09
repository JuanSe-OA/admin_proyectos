from datetime import datetime
from . import db

class Sprint(db.Model):
    __tablename__ = "sprints"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), nullable=False)
    objective   = db.Column(db.Text)
    start_date  = db.Column(db.DateTime, default=datetime.utcnow)
    end_date    = db.Column(db.DateTime)
    status      = db.Column(db.String(30), default="planned")  # planned|active|closed
    project_id  = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    project = db.relationship("Project", back_populates="sprints")
    tasks   = db.relationship("Task", back_populates="sprint")

    def __repr__(self):
        return f"<Sprint {self.name}>"
    def is_active(self):
        return self.status == "active"