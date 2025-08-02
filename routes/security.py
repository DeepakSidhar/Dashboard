from flask import Blueprint, render_template, abort, g, request
from auth import login_session_required
from models import db, Software, Hardware, Vulnerability, IncidentManagement

security_bp = Blueprint('security', __name__)

@security_bp.route('/', methods=['GET'])
@login_session_required
def vulnerability_list():
    if 'VIEW_SECURITY' not in g.permissions:
        return abort(403)
# Joining the Software- Hardware and Vulnerabilty table
    search = request.args.get('search')
    severity = request.args.get('severity')

    base_query = (
        db.session.query(Software, Hardware, Vulnerability, IncidentManagement) # The tables to be joined
        .join(
            Vulnerability, # vulnerability
            (Software.name == Vulnerability.product) & # software name - vul prod
            (Software.vendor == Vulnerability.vendor) &
            (Software.version == Vulnerability.version)
        )
        .join(
            Hardware,  # hardware
            Hardware.id == Software.hardware_id #  joining the forign key
        )
        .outerjoin( # All incidents to be displayed
            IncidentManagement,
            IncidentManagement.cve_id == Vulnerability.cve_id
        )

    )

    if search:
        base_query = base_query.filter(Vulnerability.product.ilike(f'%{search}%')) # ilike ignore the case the % is a wild card before and after.  This search can be incresed to use OR  if more  fields are needed

    if severity:
        base_query = base_query.filter(Vulnerability.severity == severity) # search by severity

    results = (
        base_query
        .order_by(
            db.case(

                    (Vulnerability.severity == 'CRITICAL', 1),
                    (Vulnerability.severity == 'HIGH', 2),
                    (Vulnerability.severity == 'MEDIUM', 3),
                    (Vulnerability.severity == 'LOW', 4),
                    else_ = 5
            )
        )
        .all()

    )

    return render_template('security.html', results=results)

