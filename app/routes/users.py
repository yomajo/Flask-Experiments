import json
from flask import Blueprint, jsonify, render_template, redirect, url_for, request, session, abort
from ..decorators import required_clearance
from ..models import db, User

roles_bp = Blueprint('roles_bp', __name__, template_folder='../templates/users', url_prefix='/users')

#replace @required_clearance(3) with login_required after flask-login integration  

@roles_bp.route('/')
@required_clearance(3)
def users():
    if 'username' in session:
        logged_in_as = db.session.query(User).filter_by(name=session['username']).first()
    registered_users = User.query.all()
    return render_template('users.html', logged_in_as=logged_in_as, registered_users=registered_users)

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
                # set cookie? session stuff?
                session['username'] = name
                
                return redirect(url_for('roles_bp.users'))
            else:
                return jsonify({'msg':'Wrong password'})
        else:
            return jsonify({'msg':'No such user, register first'})
    # GET
    if 'username' in session:
        logged_in_as = session['username']
        print(f'\nAlready logged in as: {logged_in_as}\n')
        return redirect(url_for('roles_bp.users'))

    return render_template('login.html')

@roles_bp.route('/logout')
@required_clearance(3)
def logout():
    if 'username' in session:
        session.pop('username')
        return f'''<p>logged out. Check cookies</p><br><a href="{url_for('roles_bp.login')}">To Login</a>'''
    else:
        return f'''<p>You are not logged in!</p><br><a href="{url_for('site.index')}">Home</a>'''

@roles_bp.route('/user/<id>', methods=['GET', 'POST'])
@required_clearance(3)
def user(id:int):
    if 'username' in session:
        logged_in_as = db.session.query(User).filter_by(name=session['username']).first()
        target_user = db.session.query(User).filter_by(id=id).first_or_404()

    if request.method == 'POST':
        # allow edit for admin and self
        if logged_in_as.id == id or logged_in_as.clearance == 1:
            user_to_edit = db.session.query(User).filter_by(id=id).first_or_404()
            new_username = request.form['username']
            user_to_edit.name = new_username
            db.session.commit()
            return redirect(url_for('roles_bp.admin_dashboard'))
        else:
            abort(403)
    # GET - eject if request coming from different user
    if logged_in_as.clearance == 1 or logged_in_as.id == target_user.id:
        return render_template('user.html', user=target_user)
    else:
        abort(403)

@roles_bp.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@required_clearance(2)
def delete_user(user_id):
    logged_in_as = db.session.query(User).filter_by(name=session['username']).first()
    target_user = db.session.query(User).filter_by(id=user_id).first_or_404()
    if request.method == 'POST':
        # skipping asking for confirmation in production...
        if logged_in_as.clearance == 1 or (logged_in_as.clearance == 2 and target_user.clearance == 3):
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
    if 'username' in session:
        logged_in_as = db.session.query(User).filter_by(name=session['username']).first_or_404()
    non_admin_users = db.session.query(User).filter(User.clearance!=1).all()
    return render_template('managers_only.html', logged_in_as=logged_in_as, registered_users=non_admin_users)

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
    logged_in_as = db.session.query(User).filter_by(name=session['username']).first()
    target_user = User.query.get_or_404(user_id)
    if target_user.clearance == 2:
        target_user.clearance += 1
        db.session.commit()
        return redirect(url_for('roles_bp.managers_only'))
    else:
        return jsonify({'msg':'Nice try promoting to admin...'})
