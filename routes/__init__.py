from .authentication import authentication_bp
from .home import home_bp
from .user import user_bp
from .role import role_bp
from .problem import problem_bp
from .incident import incident_bp
from .change import change_bp
from.security import security_bp
def register_routes(app):
    app.register_blueprint(authentication_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp, url_prefix='/admin/user')
    app.register_blueprint(role_bp, url_prefix='/admin/role')
    app.register_blueprint(problem_bp, url_prefix='/problem')
    app.register_blueprint(incident_bp, url_prefix='/incident')
    app.register_blueprint(change_bp, url_prefix='/change')
    app.register_blueprint(security_bp, url_prefix='/security')
