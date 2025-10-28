
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
    
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    state_kanban = db.Column(db.String(50), nullable=False, default='to_do')
    priority = db.Column(db.String(50), nullable=False, default='medium')
    estimated_hours = db.Column(db.Float, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'), nullable=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    time_registered = db.relationship('TimeRegistration', backref='task', lazy=True)

    def horas_trabajadas(self):
        return sum([r.horas for r in self.registros_tiempo])
    
    def __repr__(self):
        return f'<Tarea {self.name}>'