from flask import Blueprint, render_template, abort, g
from auth import login_session_required
from models import db, Software, Hardware, Vulnerability, IncidentManagement

security_bp = Blueprint('security', __name__)

@security_bp.route('/', methods=['GET'])
@login_session_required
def vulnerabilty_list():
    if 'VIEW_SECURITY' not in g.permissions:
        return abort(403)
# Joiuning the Software- Hardware and Vulnerabilty table
    results = (
        db.session.query(Software, Hardware, Vulnerability, IncidentManagement)
        .join(
            Vulnerability,
            (Software.name == Vulnerability.product) &
            (Software.vendor == Vulnerability.vendor) &
            (Software.version == Vulnerability.version)
        )
        .join(
            Hardware,
            Hardware.id == Software.hardware_id
        )
        .outerjoin(
            IncidentManagement,
            IncidentManagement.software_id == Software.id
        )
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

