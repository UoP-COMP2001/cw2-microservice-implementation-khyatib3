import pathlib
import connexion
from connexion.apps.flask import FlaskApp
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()

# enable swagger ui
from connexion.options import SwaggerUIOptions
swagger_ui_options = SwaggerUIOptions(swagger_ui=True, swagger_ui_path="/ui")
# Use FlaskApp explicitly for Flask applications
connex_app = FlaskApp(__name__, specification_dir=basedir.parent, swagger_ui_options=swagger_ui_options)

app = connex_app.app

template_path = basedir.parent / "templates"
app.template_folder = str(template_path.absolute())

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=dist-6-505.uopnet.plymouth.ac.uk;"
    "DATABASE=COMP2001_KBhatnagar;"
    "UID=KBhatnagar;"
    "PWD=ArlH525;"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
    )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy()
ma = Marshmallow()

db.init_app(app)
ma.init_app(app)