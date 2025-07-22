from flask import Blueprint, jsonify, render_template, request, session, redirect, g
from sqlalchemy import func

from auth import login_required, role_required, login_session_required
from models import User, db, Vulnerability, Software

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET' ])
@login_session_required
def home():
    summary = (
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
    print(summary)
    print(dict(summary))
    return render_template('home.html', summary=dict(summary)) #Change the data structure
