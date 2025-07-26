from flask import Blueprint,  render_template
from sqlalchemy import func

from auth import login_session_required
from models import User, db, Vulnerability, Software, IncidentManagement

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET' ])
@login_session_required
def home():
    security_summary = (
        db.session.query(
            Vulnerability.severity,
            func.count(Vulnerability.cve_id)
        )
        .join(
            Software,
            (Software.name == Vulnerability.product) &
            (Software.vendor == Vulnerability.vendor) &
            (Software.version == Vulnerability.version)
        )
        .group_by(Vulnerability.severity)
        .all()
    )

    incident_summary = (
        db.session.query(
            IncidentManagement.priority,
            func.count(IncidentManagement.id)
        )

        .group_by(IncidentManagement.priority)
        .all()
    )

    return render_template('home.html', security_summary=dict(security_summary), incident_summary=dict(incident_summary)) #Change the data structure
