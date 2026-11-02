from functools import wraps
from flask import session, redirect, url_for, request, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Unauthorized Access: Admin privileges required.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

