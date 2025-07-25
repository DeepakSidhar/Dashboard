import datetime

from flask import Blueprint,  render_template, request,  redirect, g, abort, url_for
from auth import login_session_required
from models import Role, db, Permission, RolePermission
from logger import logger

role_bp = Blueprint('role', __name__)

@role_bp.route('/', methods=['GET'])
@login_session_required
def role_list():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    roles  = Role.query.all()


    return render_template('role_list.html', roles=roles, selected_permission=[])


@role_bp.route('/create', methods=['GET', 'POST'])
@login_session_required
def create_role():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        permission_ids = request.form.getlist('permissions')

        if not permission_ids:
            return redirect(url_for('role.create_role'))



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
                db.session.flush()
                for pid in permission_ids:
                    role_permission = RolePermission(
                        role_id=role.id,
                        permission_id= pid
                    )
                    db.session.add(role_permission)

                db.session.commit()
                return redirect(url_for('role.role_list'))
        except Exception as e:
            db.session.rollback()
            logger.error(e)





    all_permissions = Permission.query.all()

    return render_template('create_role.html' , all_permissions=all_permissions)

@role_bp.route('/<int:role_id>/edit', methods=['GET', 'POST'])
@login_session_required
def edit_role(role_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)
    role = Role.query.get_or_404(role_id)
    all_permissions = Permission.query.all()
    selected_permission = (RolePermission.query
                           .with_entities(RolePermission.permission_id)
                           .filter_by(role_id=role.id).all())
    #  as we have selected a coloumn we are returned a list within a list which is causing an error
    print(f"Selected permission() not flat  : {selected_permission}")
    #creating a flattened list
    selected_permission = [pid for (pid,) in selected_permission]

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        permission_ids = request.form.getlist('permissions')

        if not permission_ids:
            return redirect(url_for('role.edit_role', role_id=role_id))


        # DB transaction
        try:
            with db.session.begin(nested=True):# Due to two transactions so need the nested  to allow the second.
                #update user
                role.name = name
                role.description = description
                role.updated_at = datetime.datetime.now(datetime.timezone.utc)

                #update permission
                RolePermission.query.filter_by(role_id=role.id).delete()
                for pid in permission_ids:
                    role_permission = RolePermission(
                        role_id=role.id,
                        permission_id=pid
                    )
                    db.session.add(role_permission)

                db.session.commit()

                return redirect(url_for('role.role_list'))
        except Exception as e:
            db.session.rollback()
            logger.error('Could not find the role ' + str(role_id))
            logger.error(e)
# if using get it wil drop to this section
    return render_template('create_role.html',
                           role=role,
                           all_permissions=all_permissions,
                           selected_permission=selected_permission)

@role_bp.route('/<int:role_id>/delete', methods=['POST'])
@login_session_required
def delete_role(role_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    #Update user role
    Role.query.filter_by(id= role_id).delete()
    db.session.commit()# commit the change


    return redirect(url_for('role.role_list'))