from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models import db
from .routes.auth import auth_bp
from .routes.Projects import projects_bp
from .routes.Tasks import tasks_bp
from .routes.Sprints import sprints_bp
from .routes.Time_logs import time_bp
from .routes.Reports import reports_bp
from .routes.Kpi import kpi_bp

def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # Blueprints (API v1)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(projects_bp, url_prefix="/api/v1/projects")
    app.register_blueprint(tasks_bp, url_prefix="/api/v1/tasks")
    app.register_blueprint(sprints_bp, url_prefix="/api/v1/sprints")
    app.register_blueprint(time_bp, url_prefix="/api/v1/time")
    app.register_blueprint(reports_bp, url_prefix="/api/v1/reports")
    app.register_blueprint(kpi_bp, url_prefix="/api/v1/kpi")

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
