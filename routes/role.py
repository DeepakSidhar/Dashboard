import datetime

from flask import Blueprint,  render_template, request,  redirect, g, abort, url_for
from auth import login_session_required
from models import  Role, db

role_bp = Blueprint('role', __name__)

@role_bp.route('/', methods=['GET'])
@login_session_required
def role_list():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    roles  = Role.query.all()


    return render_template('role_list.html', roles=roles)


@role_bp.route('/create', methods=['GET', 'POST'])
@login_session_required
def create_role():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']


        # DB transaction
        try:
            with db.session.begin(nested=True):
                role = Role(
                    name = name,
                    description = description,
                    created_at = datetime.datetime.now(datetime.timezone.utc),
                    updated_at =datetime.datetime.now(datetime.timezone.utc),
                )
                db.session.add(role)

                db.session.commit()
                return redirect(url_for('role.role_list'))
        except Exception as e:
            db.session.rollback()
            print(e)






    return render_template('create_role.html')

@role_bp.route('/<int:role_id>/edit', methods=['GET', 'POST'])
@login_session_required
def edit_role(role_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)
    role = Role.query.get_or_404(role_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        # DB transaction
        try:
            with db.session.begin(nested=True):# Due to two transactions so need the nested  to allow the second.
                #update user
                role.name = name
                role.description = description
                role.updated_at = datetime.datetime.now(datetime.timezone.utc)

                db.session.commit() # gets user.id

                return redirect(url_for('role.role_list'))

        except Exception as e:
            db.session.rollback()
            print('Could not find the role ' + str(role_id))
            print(e)
# if  using get it wil drop to this section
    return render_template('create_role.html',role=role)

@role_bp.route('/<int:role_id>/delete', methods=['POST'])
@login_session_required
def delete_role(role_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    #Update user role
    Role.query.filter_by(id= role_id).delete()
    db.session.commit()# commit the change


    return redirect(url_for('role.role_list'))