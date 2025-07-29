import os

from flask import  Flask
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig
from filters import register_filters
from logger import setup_logging
from models import db
from routes import register_routes
from audit import run_pip_audit # checking if any vulnerabilitues in the system




app = Flask(__name__)
#Get which enviroment the application is running in
environment = os.environ.get('FLASK_ENV', 'developement').lower()
app.config.from_object(DevelopmentConfig if environment == 'developement' else ProductionConfig)
#DataBase
db.init_app(app)
migrate = Migrate(app, db) #Migration script to implement sql  tables
#Routes
register_routes(app)
#Filters  jinja filters for serverity for error codes
register_filters(app)
#Create a logging
setup_logging(app)


if __name__ == '__main__' :
    run_pip_audit()
    app.run()