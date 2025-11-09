from datetime import datetime
from . import db

class TimeLog(db.Model):
    __tablename__ = "time_logs"
    id           = db.Column(db.Integer, primary_key=True)
    hours_logged = db.Column(db.Float, nullable=False)
    date         = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description  = db.Column(db.Text)

    task_id      = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    task = db.relationship("Task", back_populates="time_logs")
    user = db.relationship("User", back_populates="time_logs")

    def __repr__(self):
        return f"<TimeLog {self.hours_logged}h task={self.task_id}>"
