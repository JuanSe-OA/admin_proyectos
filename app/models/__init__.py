from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .User import User
from .Project import Project
from .Sprint import Sprint
from .Task import Task
from .TimeLog import TimeLog
from .Notification import Notification

__all__ = ["db", "User", "Project", "Sprint", "Task", "TimeLog", "Notification"]
