from flask import Blueprint, jsonify, render_template, request, session, redirect, g
from auth import login_required, role_required, login_session_required
from models import User

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET' ])
@login_session_required
def home():
    return render_template('home.html', user=g.user)