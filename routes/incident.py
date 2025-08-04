import datetime

from flask import Blueprint,  render_template, request,  redirect, g, abort, url_for
from auth import login_session_required
from logger import logger
from models import db, IncidentManagement, User, Hardware, Software, Vulnerability

incident_bp = Blueprint('incident', __name__)

@incident_bp.route('/', methods=['GET'])
@login_session_required
def incident_list():
    if 'VIEW_INCIDENTS' not in g.permissions:
        return abort(403)

    incidents = (
        IncidentManagement.query
        .join(User)
        .outerjoin(Hardware)
        .outerjoin(Software)
        .all()
    )


    return render_template('incident_list.html', incidents=incidents)


@incident_bp.route('/create', methods=['GET', 'POST'])
@login_session_required
def create_incident():
    if 'VIEW_INCIDENTS' not in g.permissions:
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
        cve_id = request.form.get('cve_id')
        #this is resolving the problem  of an empty string. when resolved time is blanks.
        if resolved_time == "":
            resolved_time = None
        hardware_id = None
        software_id = None
        hardware_software_type, hardware_software_id = hardware_software.split(":")
        if hardware_software_type == "SOFTWARE":
            software_id = hardware_software_id
        else :
            hardware_id = hardware_software_id
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
                    cve_id=cve_id,
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
    cve_id = request.args.get('cve_id')
    vulnerability = Vulnerability.query.get(cve_id)
    prefill = {
        "title": vulnerability.cve_id if vulnerability else None,
        "description": vulnerability.description if vulnerability else None,
        "software_id": request.args.get("prefill_software_id", type=int),
        "cve_id": cve_id
    }




    return render_template(
        'create_incident.html',
        users=users,
        hardware_list=hardware_list,
        software_list = software_list,
        prefill=prefill


    )


@incident_bp.route('/<int:incident_id>/edit', methods=['GET', 'POST'])
@login_session_required
def edit_incident(incident_id):
    if 'VIEW_INCIDENTS' not in g.permissions:
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
        hardware_software = request.form['hardware_software']
        reported_time = request.form['reported_time']
        resolved_time = request.form.get('resolved_time', None)
        # this is resolving the problem  of an empty string. when resolved time is blanks.
        if resolved_time == "":
            resolved_time = None

        hardware_id = None
        software_id = None

        hardware_software_type, hardware_software_id = hardware_software.split(":")
        if hardware_software_type == "SOFTWARE":
            software_id = hardware_software_id
        else:
            hardware_id = hardware_software_id

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
            logger.error(f'Could not find the incident ' + str(incident_id))

    users = User.query.all()
    hardware_list = Hardware.query.all()
    software_list = Software.query.all()

# if  using get it wil drop to this section
   # return render_template('create_incident.html',incident=incident_type)
    return render_template(
        'create_incident.html',
        users=users,
        hardware_list=hardware_list,
        software_list = software_list,
        incident = incident

    )

@incident_bp.route('/<int:incident_id>/delete', methods=['POST'])
@login_session_required
def delete_incident(incident_id):
    if 'VIEW_INCIDENTS' not in g.permissions:
        return abort(403)

    #Update incident
    IncidentManagement.query.filter_by(id= incident_id).delete()
    db.session.commit()# commit the change


    return redirect(url_for('incident.incident_list'))