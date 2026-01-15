from flask import jsonify, render_template, request
from werkzeug.exceptions import NotFound
from config.config import connex_app, basedir
from models.models import Users, UserActivity, Location, Activity
from connexion.options import SwaggerUIOptions
import os
import pathlib

# Add the API here - only once at startup
# connex_app.add_api(basedir.parent / "swagger" / "swagger.yml", name="MyUniqueNameKB123 ProfileService API")

# import endpoints for connexion so it can resolve operationId references
import python_endpoints.user
import python_endpoints.administrator

# Add API after all imports are complete
from connexion.options import SwaggerUIOptions
swagger_ui_options = SwaggerUIOptions(swagger_ui=True, swagger_ui_path="/ui")

# Patch Flask app's register_blueprint to handle duplicate registration gracefully
# This is needed because connexion middleware tries to register blueprints that may already be registered
_original_register = connex_app.app.register_blueprint

def _safe_register_blueprint(blueprint, **options):
    """Safely register blueprint, ignoring if already registered"""
    name = options.get('name', blueprint.name)
    # Check if already registered
    if name in connex_app.app.blueprints:
        return  # Already registered, skip
    try:
        return _original_register(blueprint, **options)
    except ValueError as e:
        if "already registered" in str(e):
            return  # Already registered, ignore
        raise

connex_app.app.register_blueprint = _safe_register_blueprint

# Add the API
connex_app.add_api(
    basedir.parent / "swagger" / "swagger.yml", 
    base_path="/profileservice-api",
    swagger_ui_options=swagger_ui_options
)

app = connex_app

# Note: Starlette exception handling is now done by connexion's middleware
# We don't need a custom handler here

@app.route("/")
def home():
    try:
        locations = Location.query.all() # retrieving all locations
        users = Users.query.all() # retrieving all users
        activities = Activity.query.all() # retrieving all activities
        user_activities = UserActivity.query.all() # retrieving all users' activities
        return render_template("home.html", locations=locations, users=users, activities=activities, user_activities=user_activities)
    except Exception as e:
        # show simple page and error if fails to connect to database
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
    # For development only - in production, use uvicorn directly via docker-entrypoint.sh
    # This avoids the development server warning
    import sys
    if os.getenv("FLASK_ENV") != "production" and "--production" not in sys.argv:
        # Development mode - use connexion's run (shows warning, but useful for dev)
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 8000))
        connex_app.run(host=host, port=port)
    else:
        # Production mode - should be run via uvicorn in docker-entrypoint.sh
        print("For production, run: uvicorn app:connex_app --host 0.0.0.0 --port 8000")
        sys.exit(1)