from .example import example_bp
from .authentication import authentication_bp
from .home import home_bp
from .user import user_bp
def register_routes(app):
    app.register_blueprint(example_bp)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp, url_prefix='/admin/user')

