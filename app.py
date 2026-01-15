from flask import jsonify, render_template, request
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
    # Use environment variables for host/port, defaulting to values suitable for Docker
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    connex_app.run(host=host, port=port)