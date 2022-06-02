from functools import wraps
from flask import session, abort
from .extensions import db
from .models import User


def required_clearance(clearance_lvl:int):
    '''pass required resource clearance lvl as int:
    1: admin
    2: manager
    3: pleb

    NOTE THE INVERTED LOGIC'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'username' in session:
                user = db.session.query(User).filter_by(name=session['username']).first_or_404()
                if clearance_lvl < user.clearance:
                    # insufficient clearance
                    print(f'\nYour clearance level {user.clearance} is insufficient to get lvl {clearance_lvl} recourse\n')
                    abort(403)
                else:
                    return func(*args, **kwargs)
            else:
                abort(403)

        return wrapper
    return decorator
