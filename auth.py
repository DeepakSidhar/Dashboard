from models import RolePermission, Permission, UserRole
from logger import logger

#https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
from functools import wraps
from flask import g, session, redirect, url_for



#session log in  for the UI
def login_session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):# a  number of argumennts and a number of key value arumennts
        user = session.get('user')
        if user is None:
            return redirect(url_for('authentication.login')) #if  the usr is none the return to the login page
        g.user = user # if the user is authenticated  then set global user request

        permission = (
            Permission.query
            .with_entities(Permission.name)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, RolePermission.role_id == UserRole.role_id)
            .filter(UserRole.user_id == user['id'])
        )
        # Flatten the result
        g.permissions = [pid for (pid,) in permission]
        logger.info(f"User {user['id']} has permission {g.permissions}")

        return f(*args, **kwargs)
    return decorated_function