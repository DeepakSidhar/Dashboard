from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User # importing the user table
from .change_management import ChangeManagement # importing the Change_Management table
from .hardware import Hardware # importing the Hardware table
from .incidentmanagement import IncidentManagement # importing the User_Role table
from .permission import Permission # importing the User_Role table
from .problem_managment import ProblemManagement # importing the User_Role table
from .role import Role # importing the User_Role table
from .rolepermission import RolePermission # importing the role_permission table
from .software import Software # importing the software table
from .userrole  import UserRole # importing the User_Role table
from .vulnerability import Vulnerability # importing the vulnerability table

