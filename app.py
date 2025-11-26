from flask import jsonify, render_template, request
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

@app.route("/users", methods=["GET"])
def getUser():
    username = request.args.get("username")
    u: Users = Users.query.filter_by(username == username).first()
    if u:
        return jsonify({
            'userID': u.userID,
            'username': u.username,
            'password': u.password,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'dob': u.dob,
            'email': u.email,
            'phone_no' : u.phone_no,
            'height': u.height,
            'weight': u.weight,
            'about_me': u.about_me,
            'marketing_language': u.marketing_language,
            'preferred_unit_metric': u.preferred_unit_metric,
            'time_preference_speed': u.time_preference_speed
        })
    else:
        return jsonify({"error_mesage": "Error occured locating user"})