from flask import Blueprint, render_template
from models.models import Users, UserActivity, Location, Activity
from create_app import create_app
import os

app = create_app()

# Set template folder
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app.template_folder = template_dir

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    locations = Location.query.all()
    users = Users.query.all()
    activities = Activity.query.all()
    user_activities = UserActivity.query.all()
    return render_template(
        "home.html",
        locations=locations,
        users=users,
        activities=activities,
        user_activities=user_activities
    )

app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)