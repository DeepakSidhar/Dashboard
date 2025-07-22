import bcrypt
from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for
from auth import login_required, role_required
from models import User

authentication_bp = Blueprint('authentication', __name__)

@authentication_bp.route('/login', methods=['GET' ,'POST']) # post allows to receive  from the front end
def login():
    error = None # Variable created for the scope of Login function.
    if request.method =='POST':
        username = request.form['username']
        plaintext_password = request.form['password'] # Plain Text


        user = User.query.filter_by(username=username).first()

        if not bcrypt.checkpw(plaintext_password.encode('utf-8'), user.password.encode('utf-8')):
            return render_template('login.html', error='invalid username or password')


        if user:
            # TODO:redirect the user to dashboard
            session['user'] = user.to_dict()
            # TODO:Set the session  successfully logged in
            return redirect(url_for('home.home'))  # need to change to the dashboard change
        else:
            # TODO:handle  authentication  failure
            error = 'Invalid user name of password'

    return render_template('login.html', error=error)


@authentication_bp.route('/logout', methods=['GET'])
def logout():
    session.clear() #clear session
    return render_template('login.html')