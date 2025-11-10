from app import create_app
from app.models import db, User, Project, Task, Sprint, TimeLog

app = create_app()

with app.app_context():
    db.create_all()

    if User.query.filter_by(email="admin@gestion.com").first():
        print("Seed ya existente, saliendo.")
        raise SystemExit(0)

    admin = User(username="admin", email="admin@gestion.com", role="admin")
    admin.set_password("admin123")
    leader = User(username="leader", email="leader@gestion.com", role="leader")
    leader.set_password("lider123")
    dev1 = User(username="dev1", email="dev1@gestion.com", role="user")
    dev1.set_password("dev123")
    dev2 = User(username="dev2", email="dev2@gestion.com", role="user")
    dev2.set_password("dev123")

    db.session.add_all([admin, leader, dev1, dev2])
    db.session.flush()

    p = Project(
        name="Proyecto Ágil", description="Demo Kanban y KPI", owner_id=leader.id
    )
    db.session.add(p)
    db.session.flush()

    s1 = Sprint(name="Sprint 1", objective="MVP", project_id=p.id, status="active")
    db.session.add(s1)
    db.session.flush()

    t1 = Task(
        name="Configurar CI",
        priority="high",
        project_id=p.id,
        assigned_to_id=dev1.id,
        sprint_id=s1.id,
        estimated_hours=5,
    )
    t2 = Task(
        name="CRUD Tareas",
        priority="medium",
        project_id=p.id,
        assigned_to_id=dev2.id,
        sprint_id=s1.id,
        estimated_hours=10,
        state_kanban="in_progress",
    )
    t3 = Task(
        name="Burndown KPI",
        priority="low",
        project_id=p.id,
        assigned_to_id=dev1.id,
        sprint_id=s1.id,
        estimated_hours=3,
        state_kanban="done",
    )
    db.session.add_all([t1, t2, t3])
    db.session.flush()

    db.session.add_all(
        [
            TimeLog(
                hours_logged=2.0,
                user_id=dev1.id,
                task_id=t1.id,
                description="Workflow básico",
            ),
            TimeLog(
                hours_logged=4.0,
                user_id=dev2.id,
                task_id=t2.id,
                description="Endpoints",
            ),
            TimeLog(
                hours_logged=3.0,
                user_id=dev1.id,
                task_id=t3.id,
                description="Cálculo KPI",
            ),
        ]
    )
    db.session.commit()
    print("Seed OK")
