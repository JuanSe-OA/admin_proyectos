import os
from app import create_app, db
from app.models import Usuario, Proyecto, Tarea, Sprint, RegistroTiempo

# Crear instancia de la aplicación
app = create_app(os.getenv('FLASK_ENV') or 'default')

# Comando para crear tablas en la base de datos
@app.cli.command()
def create_db():
    """Crea todas las tablas en la base de datos."""
    db.create_all()
    print("✅ Base de datos creada exitosamente.")

# Comando para eliminar todas las tablas
@app.cli.command()
def drop_db():
    """Elimina todas las tablas de la base de datos."""
    if input("¿Estás seguro? Esto eliminará todos los datos (s/n): ").lower() == 's':
        db.drop_all()
        print("❌ Base de datos eliminada.")
    else:
        print("Operación cancelada.")

# Comando para insertar datos de prueba
@app.cli.command()
def seed_db():
    """Inserta datos de prueba en la base de datos."""
    from datetime import date, timedelta
    
    # Crear usuarios de prueba
    admin = Usuario(
        nombre='Administrador',
        email='admin@gestion.com',
        rol='admin'
    )
    admin.set_password('admin123')
    
    lider = Usuario(
        nombre='Juan Camilo Astudillo',
        email='juan.astudillo@gestion.com',
        rol='lider'
    )
    lider.set_password('lider123')
    
    dev1 = Usuario(
        nombre='Juan Camilo Sánchez',
        email='juan.sanchez@gestion.com',
        rol='desarrollador'
    )
    dev1.set_password('dev123')
    
    dev2 = Usuario(
        nombre='María Pérez',
        email='maria@gestion.com',
        rol='desarrollador'
    )
    dev2.set_password('dev123')
    
    db.session.add_all([admin, lider, dev1, dev2])
    db.session.commit()
    
    # Crear proyecto de prueba
    proyecto = Proyecto(
        nombre='Sistema de Gestión de Proyectos',
        descripcion='Herramienta para gestionar proyectos de desarrollo de software',
        fecha_inicio=date.today(),
        fecha_fin=date.today() + timedelta(days=60),
        estado='en_curso',
        lider_id=lider.id
    )
    
    db.session.add(proyecto)
    db.session.commit()
    
    # Crear sprint de prueba
    sprint = Sprint(
        nombre='Sprint 1 - Autenticación',
        objetivo='Implementar sistema de login y registro',
        fecha_inicio=date.today(),
        fecha_fin=date.today() + timedelta(days=14),
        estado='en_curso',
        proyecto_id=proyecto.id
    )
    
    db.session.add(sprint)
    db.session.commit()
    
    # Crear tareas de prueba
    tareas = [
        Tarea(
            titulo='Diseñar modelo de base de datos',
            descripcion='Crear esquema de tablas usuarios, proyectos, tareas',
            estado_kanban='done',
            prioridad='alta',
            estimacion_horas=8,
            proyecto_id=proyecto.id,
            asignado_a_id=dev1.id,
            sprint_id=sprint.id
        ),
        Tarea(
            titulo='Implementar sistema de login',
            descripcion='Desarrollar funcionalidad de autenticación con Flask-Login',
            estado_kanban='in_progress',
            prioridad='alta',
            estimacion_horas=12,
            proyecto_id=proyecto.id,
            asignado_a_id=dev1.id,
            sprint_id=sprint.id
        ),
        Tarea(
            titulo='Crear interfaz de registro',
            descripcion='Diseñar formulario de registro con Bootstrap',
            estado_kanban='todo',
            prioridad='media',
            estimacion_horas=6,
            proyecto_id=proyecto.id,
            asignado_a_id=dev2.id,
            sprint_id=sprint.id
        ),
        Tarea(
            titulo='Implementar dashboard principal',
            descripcion='Vista general con métricas de proyectos',
            estado_kanban='todo',
            prioridad='media',
            estimacion_horas=16,
            proyecto_id=proyecto.id,
            asignado_a_id=dev2.id,
            sprint_id=sprint.id
        )
    ]
    
    db.session.add_all(tareas)
    db.session.commit()
    
    # Crear registros de tiempo
    registro = RegistroTiempo(
        horas=5.5,
        fecha=date.today(),
        descripcion='Diseño inicial del esquema',
        tarea_id=tareas[0].id,
        usuario_id=dev1.id
    )
    
    db.session.add(registro)
    db.session.commit()
    
    print("✅ Datos de prueba insertados exitosamente.")
    print("\n📋 Usuarios creados:")
    print(f"   Admin: admin@gestion.com / admin123")
    print(f"   Líder: juan.astudillo@gestion.com / lider123")
    print(f"   Dev 1: juan.sanchez@gestion.com / dev123")
    print(f"   Dev 2: maria@gestion.com / dev123")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)