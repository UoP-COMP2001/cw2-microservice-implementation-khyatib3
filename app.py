from flask import jsonify, render_template, request
from werkzeug.exceptions import NotFound
from config.config import connex_app, basedir
from models.models import Users, UserActivity, Location, Activity
from connexion.options import SwaggerUIOptions
import os
import pathlib
import sys

# import endpoints for connexion
import python_endpoints.user
import python_endpoints.administrator

#enable swagger ui so endpoints can be tested
from connexion.options import SwaggerUIOptions
swagger_ui_options = SwaggerUIOptions(swagger_ui=True, swagger_ui_path="/ui")


_original_register = connex_app.app.register_blueprint

def _safe_register_blueprint(blueprint, **options):
    # added as was getting many 'non-unique blueprint' errors durng runime
    name = options.get('name', blueprint.name)
    # check if blueprint already exists
    if name in connex_app.app.blueprints:
        return 
    try:
        return _original_register(blueprint, **options)
    except ValueError as e:
        if "already registered" in str(e):
            return 
        raise

connex_app.app.register_blueprint = _safe_register_blueprint

# add swagger
connex_app.add_api(
    basedir.parent / "swagger" / "swagger.yml", 
    base_path="/profileservice-api",
    swagger_ui_options=swagger_ui_options
)

app = connex_app

@app.route("/")
def home():
    try:
        locations = Location.query.all() # retrieving all locations
        users = Users.query.all() # retrieving all users
        activities = Activity.query.all() # retrieving all activities
        user_activities = UserActivity.query.all() # retrieving all users' activities
        return render_template("home.html", locations=locations, users=users, activities=activities, user_activities=user_activities)
    except Exception as e:
        # show simple page and any error if fails to connect to database
        return f"""
        <html>
        <head><title>COMP2001</title></head>
        <body>
            <h1>ProfileService Microservice</h1>
            <p>Database connection error: {str(e)}</p>
            <p>API Documentation: <a href="/profileservice-api/ui/" target="_blank">Swagger UI</a></p>
            <p>API Base: <a href="/profileservice-api/">/profileservice-api/</a></p>
            <p>OpenAPI Spec: <a href="/profileservice-api/openapi.json" target="_blank">/profileservice-api/openapi.json</a></p>
        </body>
        </html>
        """, 200

if __name__ == "__main__":
    
    if os.getenv("FLASK_ENV") != "production" and "--production" not in sys.argv:
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 8000))
        connex_app.run(host=host, port=port)
    else:
        print("Run: uvicorn app:connex_app --host 0.0.0.0 --port 8000")
        sys.exit(1)