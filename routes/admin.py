import datetime

from flask import Blueprint, jsonify, render_template, request, session, redirect, g, abort, url_for
from auth import login_required, role_required, login_session_required
from models import User, UserRole, Role, db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET' ])
@login_session_required
def admin_home():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    users  = User.query.all()#


    return render_template('admin_home.html', users=users)


@admin_bp.route('/create', methods=['GET', 'POST' ])
@login_session_required
def create_user():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)
    roles = Role.query.all()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        role_ids = request.form.getlist('roles')

        if not role_ids:
            return render_template('create_user.html', roles=roles, error="Select at least one role")

        # DB transaction
        try:
            with db.session.begin():
                user = User(
                    username = username,
                    email_text = email,
                    first_name = first_name,
                    last_name = last_name,
                    password = password,
                    created_at = datetime.datetime.now(datetime.timezone.utc),
                    updated_at =datetime.datetime.now(datetime.timezone.utc),
                )
                db.session.add(user)
                db.session.flush() # gets user.id

                for role_id in role_ids:
                    user_role = UserRole(user_id = user.id, role_id=int(role_id))
                    db.session.add(user_role)
                return redirect(url_for('admin.admin_home'))
        except Exception as e:
            db.session.rollback()
            print(e)






    return render_template('create_user.html', roles=roles)
