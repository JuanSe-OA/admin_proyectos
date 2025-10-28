from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='ongoing')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tasks = db.relationship('Task', backref='project', lazy=True)
    sprints = db.relationship('Sprint', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.name}>'
    
    def progreso_total(self):
        if not self.tareas:
            return 0
        completadas = len([t for t in self.tareas if t.estado_kanban == 'done'])
        return round((completadas / len(self.tareas)) * 100, 2)