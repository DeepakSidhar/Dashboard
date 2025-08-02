import datetime

from flask import Blueprint,  render_template, g, abort
from auth import login_session_required

from models import db,  Hardware

hardware_bp = Blueprint('hardware', __name__)

@hardware_bp.route('/', methods=['GET'])
@login_session_required
def hardware_list():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    hardwares  = Hardware.query.all()






    return render_template('hardware_list.html', hardwares=hardwares)


