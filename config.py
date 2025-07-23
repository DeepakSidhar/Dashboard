import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres1@localhost:5433/dashboard_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sdfsjdfkl;sfssfsdfsssdfsf'# secret key so only .py  can modify
    NVD_API_KEY = 'eb1fd457-a957-419d-a6ed-e8aab63bad85'
    DEBUG = True

#This is collecting the system environments setting from the server to ensure the data is not hardcodeed
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')# secret key so only .py  can modify
    NVD_API_KEY = os.environ.get('NVD_API_KEY')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'# Checking the string if its anything other than true  then will pass the string to boolean
