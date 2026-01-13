from flask import jsonify, render_template, request
import config
from models import Users, UserActivity, Location, Activity

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    locations = Location.query.all() # retrieving all locations
    users = Users.query.all() # retrieving all users
    activities = Activity.query.all() # retrieving all activities
    user_activities = UserActivity.query.all() # retrieving all users' activities
    return render_template("home.html", locations=locations, users=users, activities=activities, user_activities=user_activities)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
    
