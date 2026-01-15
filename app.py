from flask import jsonify, render_template, request
from config.config import connex_app, basedir
from models.models import Users, UserActivity, Location, Activity
from connexion.options import SwaggerUIOptions

# import endpoints for connexion so it can resolve operationId references
import python_endpoints.user
import python_endpoints.administrator

app = connex_app

# enable Swagger UI for api
api_swagger_ui_options = SwaggerUIOptions(swagger_ui=True, swagger_ui_path="/ui")
app.add_api(basedir.parent / "swagger" / "swagger.yml", swagger_ui_options=api_swagger_ui_options,name="ProfileService API")

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
    app.run(host="127.0.0.1", port=8000)