from .example import example_bp
from .authentication import authentication_bp
def register_routes(app):
    app.register_blueprint(example_bp)
    app.register_blueprint(authentication_bp)
