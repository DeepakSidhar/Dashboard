import datetime

from flask import Blueprint,  render_template, request,  redirect, g, abort, url_for
from auth import login_session_required
from models import  db, ChangeManagement

change_bp = Blueprint('change', __name__)

@change_bp.route('/', methods=['GET'])
@login_session_required
def change_list():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    changes  = ChangeManagement.query.all()


    return render_template('change_list.html', changes=changes)


@change_bp.route('/create', methods=['GET', 'POST'])
@login_session_required
def create_change():
    if 'VIEW_CHANGE' not in g.permissions:
        return abort(403)

    if request.method == 'POST':
        title = request.form['name']
        description = request.form['description']
        status = request.form['status']
        priority = request.form['priority']
        impact = request.form['impact']
        change_type = request.form['change_type']
        requested_by_id = request.form['requested_by_id']
        proposed_time = request.form['proposed_time']
        executed_time = request.form['executed_time']
        software_id = request.form['software_id']
        hardware_id = request.form['hardware_id']


        # DB transaction
        try:
            with db.session.begin(nested=True):
                change = ChangeManagement(
                    title = title,
                    description = description,
                    status = status,
                    priority = priority,
                    impact = impact,
                    change_type =  change_type,
                    requested_by_id = requested_by_id,
                    proposed_time =  proposed_time,
                    executed_time = executed_time,
                    software_id = software_id,
                    hardware_id = hardware_id,
                    created_at = datetime.datetime.now(datetime.timezone.utc),
                    updated_at =datetime.datetime.now(datetime.timezone.utc)
                )
                db.session.add(change)

                db.session.commit()
                return redirect(url_for('change.change_list'))
        except Exception as e:
            db.session.rollback()
            print(e)






    return render_template('create_change.html')

@change_bp.route('/<int:change_id>/edit', methods=['GET', 'POST'])
@login_session_required
def edit_change(change_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)
    change = ChangeManagement.query.get_or_404(change_id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description'],
        status = request.form['status'],
        priority = request.form['priority'],
        impact = request.form['impact'],
        change_type = request.form['change_type'],
        requested_by_id = request.form['requested_by_id'],
        proposed_time = request.form['proposed_time'],
        executed_time = request.form['executed_time'],
        software_id = request.form['software_id'],
        hardware_id = request.form['hardware_id']


        # DB transaction
        try:
            with db.session.begin(nested=True):# Due to two transactions so need the nested  to allow the second.
                #update change
                change.title = title
                change.description = description
                change.status = status,
                change.priority = priority,
                change.impact = impact,
                change.change_type = change_type,
                change.requested_by_id = requested_by_id,
                change.proposed_time = proposed_time,
                change.executed_time = executed_time,
                change.software_id = software_id,
                change.hardware_id = hardware_id,
                change.updated_at = datetime.datetime.now(datetime.timezone.utc),

                db.session.commit() # gets user.id

                return redirect(url_for('change.change_list'))

        except Exception as e:
            db.session.rollback()
            print('Could not find the change ' + str(change_id))
            print(e)
# if  using get it wil drop to this section
    return render_template('create_change.html',change=change)

@change_bp.route('/<int:change_id>/delete', methods=['POST'])
@login_session_required
def delete_change(change_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    #Update change
    ChangeManagement.query.filter_by(id= change_id).delete()
    db.session.commit()# commit the change


    return redirect(url_for('change.change_list'))