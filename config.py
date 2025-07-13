class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres1@localhost:5433/dashboard_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sdfsjdfkl;sfssfsdfsssdfsf'# secret key so only .py  can modify
    NVD_API_KEY = 'eb1fd457-a957-419d-a6ed-e8aab63bad85'
    DEBUG = True
