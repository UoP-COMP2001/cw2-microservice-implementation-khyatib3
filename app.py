from flask import render_template
import config
from models import Users, UserActivity, Location, Activity

app = config.connex_app
# app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    locations = Location.query.all()
    users = Users.query.all()
    activities = Activity.query.all()
    user_activities = UserActivity.query.all()
    return render_template("home.html", locations=locations, users=users, activities=activities, user_activities=user_activities)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
