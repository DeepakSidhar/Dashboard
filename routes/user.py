import datetime
import bcrypt#(Bodnar, 2024)
import re#(Python, 2009)
from flask import Blueprint,  render_template, request,  redirect, g, abort, url_for
from auth import login_session_required
from logger import logger
from models import User, UserRole, Role, db

user_bp = Blueprint('user', __name__)

def hash_password(plain_password):
    # The below is generating hashed password using salt, which is encoded with using utf-8.
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def is_valid_password(plain_password):

    # Must be at least 8 characters
    if len(plain_password) < 8:
        return False
     # Must be at least 1  uppercase
    if not re.search(r'[A-Z]', plain_password):
        return False
    # Must be at least 1 lowercase
    if not re.search(r'[a-z]', plain_password):
        return False
    # Must be at least 1 numer
    if not re.search(r'[0-9]', plain_password):
        return False
    # Must be at least speacial ?=.*!@#$%^&(),:{}|<> character"
    if not re.search(r'[?=.*!@#$%^&(),:{}|<>]', plain_password):
        return False

    return True

@user_bp.route('/', methods=['GET'])
@login_session_required
def user_list():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    users  = User.query.all()


    return render_template('user_list.html', users=users)


@user_bp.route('/create', methods=['GET', 'POST'])
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
        if not is_valid_password(password):
            return render_template('create_user.html', roles=roles, error="Must be at least 8 characters and include uppercase, lowercase, number, and special character")
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
                    password = hash_password(password),
                    created_at = datetime.datetime.now(datetime.timezone.utc),
                    updated_at =datetime.datetime.now(datetime.timezone.utc),
                )
                db.session.add(user)
                db.session.flush()
                for role_id in role_ids:
                    user_role = UserRole(user_id = user.id, role_id=int(role_id))
                    db.session.add(user_role)
                db.session.commit()
                return redirect(url_for('user.user_list'))
        except Exception as e:
            db.session.rollback()
            logger.error(e)
    return render_template('create_user.html', roles=roles)

@user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
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

        if not is_valid_password(password):
            return render_template('create_user.html', user=user, roles=roles, error="Must be at least 8 characters and include uppercase, lowercase, number, and special character")

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
                user.password = hash_password(password),
                user.updated_at = datetime.datetime.now(datetime.timezone.utc)

                #update user role
                UserRole.query.filter_by(user_id=user_id).delete()# we are deletig the user role from the database and then will update again with the new set

                for role_id in role_ids:
                    user_role = UserRole(user_id = user.id, role_id=int(role_id))
                    db.session.add(user_role)

                db.session.commit()

                return redirect(url_for('user.user_list'))

        except Exception as e:
            db.session.rollback()
            logger.error('Could not find the user ' + str(user_id))
            logger.error(e)
# if  using get it wil drop to this section
    return render_template('create_user.html',user=user, roles=roles)

@user_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_session_required
def delete_user(user_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    #Update user role
    UserRole.query.filter_by(user_id= user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()# commit the change


    return redirect(url_for('user.user_list'))