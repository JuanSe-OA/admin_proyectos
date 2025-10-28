from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Sprint(db.Model):
    __tablename__ = 'sprints'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    objective = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='planned')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    tasks = db.relationship('Task', backref=db.backref('sprint', lazy=True))

    def __repr__(self):
        return f'<Sprint {self.name}>'