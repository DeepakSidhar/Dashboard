import datetime

from flask import Blueprint,  render_template, request,  redirect, g, abort, url_for
from auth import login_session_required
from logger import logger
from models import db, Hardware, Software

software_bp = Blueprint('software', __name__)

@software_bp.route('/', methods=['GET'])
@login_session_required
def software_list():

    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    softwares  = Software.query \
        .join(Hardware, Hardware.id == Software.hardware_id) \
        .all()
    print(softwares[0])




    return render_template('software_list.html', softwares=softwares)


