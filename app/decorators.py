from functools import wraps
from flask import abort
from flask_login import current_user


def required_clearance(clearance_lvl:int):
    '''decorator for role-protected routes. Pass clearance_lvl (int) arg for specific resource to get access or get 403.
    1: admin
    2: manager
    3: pleb

    NOTE THE INVERTED LOGIC'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                if clearance_lvl < current_user.clearance:
                    print(f'\n{current_user.name} clearance lvl {current_user.clearance} is insufficient to get lvl {clearance_lvl} recourse. Request blocked by decorator\n')
                    abort(403)
                else:
                    return func(*args, **kwargs)
            else:
                abort(403)
        return wrapper
    return decorator
