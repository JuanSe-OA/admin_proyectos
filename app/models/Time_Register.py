from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class TimeRegister(db.Model):
    __tablename__ = 'time_registers'
    id = db.Column(db.Integer, primary_key=True)
    hours_logged = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.Text, nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<RegistroTiempo {self.hours_logged}h en Tarea#{self.task_id}>'