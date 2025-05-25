from flask import Blueprint, jsonify
from auth import login_required, role_required

example_bp = Blueprint('exxample', __name__)

@example_bp.route('/hello', methods=['GET'])
@login_required
@role_required('manager')
def hello():
    return jsonify({'Hello': 'World'})


