from datetime import datetime, timedelta
from . import db

class Notification(db.Model):
    __tablename__ = "notifications"
    id          = db.Column(db.Integer, primary_key=True)
    message     = db.Column(db.String(300), nullable=False)
    level       = db.Column(db.String(20), default="info")  # info|warning|danger
    is_read     = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
