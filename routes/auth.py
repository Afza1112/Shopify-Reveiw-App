from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        admin_user = current_app.config['ADMIN_USERNAME']
        admin_pass = current_app.config['ADMIN_PASSWORD']
        if username == admin_user and password == admin_pass:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin_panel'))
        else:
            flash("Invalid credentials", "error")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("Logged out.", "info")
    return redirect(url_for('auth.login'))
