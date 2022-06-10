from flask import Blueprint, jsonify, render_template, redirect, url_for, request, abort
from flask_login import current_user, login_required, login_user, logout_user
from ..app_utils import required_clearance
from ..models import db, User

roles_bp = Blueprint('roles_bp', __name__, template_folder='../templates/users', url_prefix='/users')


@roles_bp.route('/')
@login_required
def users():
    registered_users = User.query.all()
    return render_template('users.html', registered_users=registered_users)

@roles_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        clearance = request.form['clearance']
        user = User(name=name, password=password, clearance=clearance)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('roles_bp.login'))    
    return render_template('register.html')

@roles_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        user_about_to_login = db.session.query(User).filter_by(name=name).first()
        if user_about_to_login:
            if user_about_to_login.password == password:
                login_user(user_about_to_login)
                return redirect(url_for('roles_bp.users'))
            else:
                return jsonify({'msg':'Wrong password'})
        else:
            return jsonify({'msg':'No such user, register first'})
    # GET
    if current_user.is_authenticated:
        print(f'\nAlready logged in as: {current_user.name}\n')
        return redirect(url_for('roles_bp.users'))

    return render_template('login.html')

@roles_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('site.index'))
    else:
        return f'''<p>You are not logged in!</p><br><a href="{url_for('site.index')}">Home</a>'''

@roles_bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id):
    target_user = db.session.query(User).filter_by(id=user_id).first_or_404()
    if request.method == 'POST':
        # allow edit for admin and self
        if current_user.id == user_id or current_user.clearance == 1:
            new_username = request.form['username']
            target_user.name = new_username
            db.session.commit()
            return redirect(url_for('roles_bp.admin_dashboard'))
        else:
            abort(403)
    # GET - eject if request coming from different user
    if current_user.clearance == 1 or current_user.id == target_user.id:
        return render_template('user.html', user=target_user)
    else:
        abort(403)

@roles_bp.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@required_clearance(2)
def delete_user(user_id):
    target_user = db.session.query(User).filter_by(id=user_id).first_or_404()
    if request.method == 'POST':
        # skipping asking for confirmation in production...
        if current_user.clearance == 1 or (current_user.clearance == 2 and target_user.clearance == 3):
            db.session.delete(target_user)
            db.session.commit()
            return redirect(url_for('roles_bp.admin_dashboard'))
        else:
            abort(403)
    else:
        return jsonify({'msg':'get request on delete endpoint...'})

@roles_bp.route('/managers_only')
@required_clearance(2)
def managers_only():
    non_admin_users = db.session.query(User).filter(User.clearance!=1).all()
    return render_template('managers_only.html', registered_users=non_admin_users)

@roles_bp.route('/admin_dashboard')
@required_clearance(1)
def admin_dashboard():
    registered_users = User.query.all()
    return render_template('admin_dashboard.html', registered_users=registered_users)

@roles_bp.route('/promote/<int:user_id>', methods=['POST'])
@required_clearance(2)
def promote(user_id):
    target_user = User.query.get_or_404(user_id)
    if target_user.clearance == 3:
        target_user.clearance -= 1
        db.session.commit()
        return redirect(url_for('roles_bp.managers_only'))
    else:
        return jsonify({'msg':'Nice try promoting to admin...'})

@roles_bp.route('/demote/<int:user_id>', methods=['POST'])
@required_clearance(2)
def demote(user_id):
    target_user = User.query.get_or_404(user_id)
    if target_user.clearance == 2:
        target_user.clearance += 1
        db.session.commit()
        return redirect(url_for('roles_bp.managers_only'))
    else:
        return jsonify({'msg':'Nice try promoting to admin...'})
