from flask import Blueprint, jsonify, render_template, redirect, url_for, request, session, g
from ..models import db, User

roles_bp = Blueprint('roles_bp', __name__, template_folder='../templates/users', url_prefix='/users')


@roles_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        clearance = request.form['clearance']
        user = User(name=name, password=password, clearance=clearance)
        db.session.add(user)
        db.session.commit()
        print(f'\nregistered new user {name}\n')
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
                # set cookie? session stuff?
                session['username'] = name
                
                return redirect(url_for('roles_bp.members_only'))
            else:
                return jsonify({'msg':'Wrong password'})
        else:
            return jsonify({'msg':'No such user, register first'})
    # GET
    if 'username' in session:
        logged_in_as = session['username']
        print(f'\nAlready logged in as: {logged_in_as}\n')
        return redirect(url_for('roles_bp.members_only'))

    return render_template('login.html')

@roles_bp.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        return f'''<p>logged out. Check cookies</p><br><a href="{url_for('roles_bp.users')}">Users</a>'''
    else:
        return f'''<p>You are not logged in!</p><br><a href="{url_for('roles_bp.login')}">Users</a>'''

@roles_bp.route('/users')
def users():
    # registered_users = User.query.all()
    return render_template('users.html')

@roles_bp.route('/users/<id>')
def user(id:int):
    return render_template('user.html')

@roles_bp.route('/users/members_only')
def members_only():
    registered_users = User.query.all()
    return render_template('members_only.html', registered_users=registered_users)

@roles_bp.route('/users/admin_dashboard')
def admin_dashboard():
    return jsonify({'msg':'If you are not admin, we have failed'})
