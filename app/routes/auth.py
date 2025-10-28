from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Usuario
from werkzeug.urls import url_parse

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Por favor completa todos los campos.', 'warning')
            return render_template('auth/login.html')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario is None or not usuario.check_password(password):
            flash('Email o contraseña incorrectos.', 'danger')
            return render_template('auth/login.html')
        
        if not usuario.activo:
            flash('Tu cuenta ha sido desactivada. Contacta al administrador.', 'warning')
            return render_template('auth/login.html')
        
        login_user(usuario, remember=remember)
        flash(f'¡Bienvenido, {usuario.nombre}!', 'success')
        
        # Redirigir a la página solicitada o al dashboard
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        
        return redirect(next_page)
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        rol = request.form.get('rol', 'desarrollador')
        
        if not all([nombre, email, password, password_confirm]):
            flash('Por favor completa todos los campos.', 'warning')
            return render_template('auth/register.html')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'warning')
            return render_template('auth/register.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('Este email ya está registrado.', 'warning')
            return render_template('auth/register.html')
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            rol=rol
        )
        nuevo_usuario.set_password(password)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error al registrar el usuario.', 'danger')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/perfil')
@login_required
def perfil():
    return render_template('auth/perfil.html', usuario=current_user)


@auth_bp.route('/cambiar-password', methods=['POST'])
@login_required
def cambiar_password():
    password_actual = request.form.get('password_actual')
    password_nueva = request.form.get('password_nueva')
    password_confirmar = request.form.get('password_confirmar')
    
    if not current_user.check_password(password_actual):
        flash('La contraseña actual es incorrecta.', 'danger')
        return redirect(url_for('auth.perfil'))
    
    if password_nueva != password_confirmar:
        flash('Las contraseñas nuevas no coinciden.', 'danger')
        return redirect(url_for('auth.perfil'))
    
    if len(password_nueva) < 6:
        flash('La nueva contraseña debe tener al menos 6 caracteres.', 'warning')
        return redirect(url_for('auth.perfil'))
    
    current_user.set_password(password_nueva)
    db.session.commit()
    flash('Contraseña actualizada exitosamente.', 'success')
    return redirect(url_for('auth.perfil'))