import datetime

from flask import Blueprint,  render_template, request,  redirect, g, abort, url_for
from auth import login_session_required
from models import db, IncidentManagement, User, Hardware, Software

incident_bp = Blueprint('incident', __name__)

@incident_bp.route('/', methods=['GET'])
@login_session_required
def incident_list():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    incidents  = IncidentManagement.query.all()


    return render_template('incident_list.html', incidents=incidents)


@incident_bp.route('/create', methods=['GET', 'POST'])
@login_session_required
def create_incident():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        priority = request.form['priority']
        impact = request.form['impact']
        assignee_id = request.form['assignee_id']
        incident_type = request.form['incident_type']
        hardware_software = request.form['hardware_software']
        reported_time = request.form['reported_time']
        resolved_time = request.form.get('resolved_time', None)
        #this is resolving the problem  of an empty string. when resolved time is blanks.
        if resolved_time == "":
            resolved_time = None

        hardware_id = None
        software_id = None

        software = Software.query.get(hardware_software)
        if software:
            software_id = hardware_software
        else :
            hardware_id = hardware_software



        # DB transaction
        try:
            with db.session.begin(nested=True):
                incident = IncidentManagement(
                    title = title,
                    description = description,
                    status = status,
                    priority = priority,
                    impact = impact,
                    assignee_id =  assignee_id,
                    incident_type = incident_type,
                    software_id =  software_id,
                    hardware_id = hardware_id,
                    reported_time = reported_time,
                    resolved_time = resolved_time,
                    created_at = datetime.datetime.now(datetime.timezone.utc),
                    updated_at =datetime.datetime.now(datetime.timezone.utc),
                )
                db.session.add(incident)

                db.session.commit()
                return redirect(url_for('incident.incident_list'))
        except Exception as e:
            db.session.rollback()
            print(e)


    users = User.query.all()
    hardware_list = Hardware.query.all()
    software_list = Software.query.all()




    return render_template('create_incident.html', users=users, hardware_list=hardware_list, software_list = software_list)

@incident_bp.route('/<int:incident_id>/edit', methods=['GET', 'POST'])
@login_session_required
def edit_incident(incident_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)
    incident = IncidentManagement.query.get_or_404(incident_id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        priority = request.form['priority']
        impact = request.form['impact']
        assignee_id = request.form['assignee_id']
        incident_type = request.form['incident_type']
        software_id = request.form['software_id']
        hardware_id = request.form['hardware_id']
        reported_time = request.form['reported_time']
        resolved_time = request.form['resolved_time']
        # DB transaction
        try:
            with db.session.begin(nested=True):# Due to two transactions so need the nested  to allow the second.
                #update incident
                incident.title = title
                incident.description = description
                incident.status = status,
                incident.priority = priority,
                incident.impact = impact,
                incident.assignee_id = assignee_id,
                incident.incident_type = incident_type,
                incident.software_id = software_id,
                incident.hardware_id = hardware_id,
                incident.reported_time = reported_time,
                incident.resolved_time = resolved_time,
                incident.updated_at = datetime.datetime.now(datetime.timezone.utc)

                db.session.commit()

                return redirect(url_for('incident.incident_list'))

        except Exception as e:
            db.session.rollback()
            print('Could not find the incident ' + str(incident_id))
            print(e)
# if  using get it wil drop to this section
    return render_template('create_incident.html',incident=incident)

@incident_bp.route('/<int:incident_id>/delete', methods=['POST'])
@login_session_required
def delete_incident(incident_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    #Update incident
    IncidentManagement.query.filter_by(id= incident_id).delete()
    db.session.commit()# commit the change


    return redirect(url_for('incident.incident_list'))