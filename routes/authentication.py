import bcrypt#(Bodnar, 2024)
from flask import Blueprint, render_template, request, session, redirect, url_for
from logger import logger
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
            # Set the session  successfully logged in
            session['user'] = user.to_dict()
            # nredirect the user to dashboard
            return redirect(url_for('home.home'))  # need to change to the dashboard change
        else:
            # handle  authentication  failure
            error = 'Invalid user name of password'
            logger.info(f"Invalid user name or password: {username}")

    return render_template('login.html', error=error)


@authentication_bp.route('/logout', methods=['GET'])
def logout():
    session.clear() #clear session cookie
    return redirect(url_for('authentication.login'))