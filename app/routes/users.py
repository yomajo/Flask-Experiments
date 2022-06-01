from flask import Blueprint, jsonify, render_template, redirect, url_for, request
from ..models import db, User

roles_bp = Blueprint('roles_bp', __name__, template_folder='../templates/users')


@roles_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        clearance = request.form['clearance']
        user = User(name=name, password=password, clearance=clearance)
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg':'registered!'})
    
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
                return redirect(url_for('roles_bp.members_only'))
            else:
                return jsonify({'msg':'Wrong password'})
        else:
            return jsonify({'msg':'No such user, register first'})

    return render_template('login.html')

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
