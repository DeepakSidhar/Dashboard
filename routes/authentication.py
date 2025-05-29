from flask import Blueprint, jsonify, render_template, request, session, redirect
from auth import login_required, role_required
from models import User

authentication_bp = Blueprint('authentication', __name__)

@authentication_bp.route('/login', methods=['GET' ,'POST']) # post allows to receive  from the front end
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        #TODO:Set the session  successfully logged in
        return redirect('/')# need to change to the dashboard change
        #TODO:redirect the user to dashboard
        session['user'] = user
        #TODO:handle  authentication  failure




    return render_template('login.html')