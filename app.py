from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from filters import register_filters
from models import db
from routes import register_routes


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db) #Migration script to implement sql  tables

register_routes(app)
register_filters(app)

if __name__ == '__main__' :
    app.run()