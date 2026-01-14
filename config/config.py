import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()

# Enable Swagger UI explicitly
from connexion.options import SwaggerUIOptions
swagger_ui_options = SwaggerUIOptions(swagger_ui=True, swagger_ui_path="/ui")
connex_app = connexion.App(__name__, specification_dir=basedir.parent, swagger_ui_options=swagger_ui_options)

app = connex_app.app

# Configure template folder to point to project root templates directory
template_path = basedir.parent / "templates"
app.template_folder = str(template_path.absolute())

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
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