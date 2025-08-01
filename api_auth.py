import base64
import bcrypt

from models import RolePermission, Permission, UserRole, \
    User  # This is importing the user.py User class to get the user table
from logger import logger

#https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
from functools import wraps
from flask import g, session, redirect, url_for, request, jsonify

# permission  for servers API  authentication
def authenticate():

    auth_header = request.headers.get('Authorization')#header basic auth username and password split by :

# If no header return nothing.
    if not auth_header:
        return None

    try:
        # Creating two variables  and splitting the auth_header by space.
        auth_type, credentials = auth_header.split()

        # if  the auth_header is not Basic then we will reject
        if auth_type != 'Basic':
            return None
        #This is taking the base64 encoded and using base64  decoder  to find the full user namme  and password.
        decoded = base64.b64decode(credentials).decode()
        # not once we have decoded  we are spliting by :
        username, password = decoded.split(':')

        # We now need to  run a query agaisnt the database and should look like this in the  sql
        # SELECT * from user where  username = ${username} AND password = ${password }
        # for Flask we have a feature to query the  models from user.py User class and look for the column names, such as  username and password.
        # as the username and password is  unique we just need to pull the first one
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            logger.info(f'Invalid API credentials for : {username}')
            return None
    except Exception :
        return None

# wrapper function works as a middleware
# https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/
# Http Header ==> Authorastion : Basic

# permission  for servers API  authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = authenticate()
        if user is None:

            return jsonify({'message': 'Authentication required'}), 401 # give a message to ensure the user knows that authentication is needed with the correct error code
        g.user = user # if the user is authenticated  then we continue with access
        return f(*args, **kwargs)
    return decorated_function

# permission  for servers API  authentication
def permission_required(permission_name):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g,'user'):  # or g.user.role != role:# check the global store has the user stored and the role  is matched Removed as the role col is removed
                logger.info(f'Permission denied for user : {g.user.username}, permission : {permission_name}')
                return jsonify({'message': 'Access denied'}), 403
            # Join query rolePermission  --> Permission
            permissions = Permission.query\
                .join(RolePermission, RolePermission.permission_id == Permission.id)\
                .join(UserRole, RolePermission.role_id == UserRole.role_id)\
                .filter(UserRole.user_id == g.user.id)\
                .all()



            for permission in permissions:
                if permission.name == permission_name:  # checking if the role matches  and if its suceesful pass  and return
                    return f(*args, **kwargs)

            return jsonify({'message': 'Access denied'}), 403  # if not matching access is denided

        return decorated_function

    return wrapper
