import datetime

from flask import Blueprint, jsonify, render_template, request, session, redirect, g, abort, url_for
from auth import login_required, role_required, login_session_required
from models import User, UserRole, Role, db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/user', methods=['GET' ])
@login_session_required
def user_list():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    users  = User.query.all()


    return render_template('user_list.html', users=users)


@admin_bp.route('/user/create', methods=['GET', 'POST' ])
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
            with db.session.begin(nested=True):
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
                db.session.commit()
                return redirect(url_for('admin.user_list'))
        except Exception as e:
            db.session.rollback()
            print(e)






    return render_template('create_user.html', roles=roles)

@admin_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST' ])
@login_session_required
def edit_user(user_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        role_ids = request.form.getlist('roles')

        if not role_ids:
            return render_template('create_user.html', user=user, roles=roles, error="Select at least one role")

        # DB transaction
        try:
            with db.session.begin(nested=True):# Due to two transactions so need the nested  to allow the second.
                #update user
                user.username = username
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.password = password

                #update user role
                UserRole.query.filter_by(user_id=user_id).delete()# we are deletig the user role from the database and then will update again with the new set

                for role_id in role_ids:
                    user_role = UserRole(user_id = user.id, role_id=int(role_id))
                    db.session.add(user_role)

                db.session.commit() # gets user.id

                return redirect(url_for('admin.user_list'))

        except Exception as e:
            db.session.rollback()
            print('Could not find the user ' + str(user_id))
            print(e)
# if  using get it wil drop to this section
    return render_template('create_user.html',user=user, roles=roles)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_session_required
def delete_user(user_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    #Update user role
    UserRole.query.filter_by(user_id= user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()# commit the change


    return redirect(url_for('admin.user_list'))