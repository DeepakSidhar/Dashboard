class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres1@localhost:5433/dashboard_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sdfsjdfkl;sfssfsdfsssdfsf'# secret key so only admin  can modify
