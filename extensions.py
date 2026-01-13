from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from config import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)