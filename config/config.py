import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()

db = SQLAlchemy()
ma = Marshmallow()

def create_connexion_app():
    connex_app = connexion.App(__name__, specification_dir=basedir)
    flask_app = connex_app.app

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mssql+pyodbc:///?odbc_connect="
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=dist-6-505.uopnet.plymouth.ac.uk;"
        "DATABASE=COMP2001_KBhatnagar;"
        "UID=KBhatnagar;"
        "PWD=ArlH525;"
        "TrustServerCertificate=yes;"
        "Encrypt=yes;"
    )
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(flask_app)
    ma.init_app(flask_app)

    return connex_app
