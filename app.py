from flask import jsonify, render_template, request
import config
from models import Users, UserActivity, Location, Activity

app = config.connex_app
# app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    locations = Location.query.all() # retrieving all locations
    users = Users.query.all() # retrieving all users
    activities = Activity.query.all() # retrieving all activities
    user_activities = UserActivity.query.all() # retrieving all users' activities
    return render_template("home.html", locations=locations, users=users, activities=activities, user_activities=user_activities)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)

@app.route("/users", methods=["GET"])
def getUser():
    email = request.args.get("email") # get passed in username
    u: Users = Users.query.filter_by(email == email).first() # find user with given username
    if u:
        return jsonify({ # returned jsonified data belonging to that user
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
        return jsonify({"error_mesage": "Error occured locating user"}) # or return error message if that user was not found
    

@app.route("/users", methods=["POST"])
def addNewUser():
    creds = request.get_json(silent=True) or request.form # getting entered login details
    email = creds.get("email") # getting email
    password = creds.get("password") # getting password

    if not email or not password: # checking both email and password are given
        return jsonify({"error_message": "Email and password BOTH are required"}), 400

    existing = Users.query.filter_by(email=email).first() # checking for user with same email already existing
    if existing:
        return jsonify({"error_message": "User with this email already exists"}), 409 # returning appropriate message to user

    new_user = Users(email=email, password=password) # creating new user with email and password after passing checks
    config.db.session.add(new_user) # adding user
    config.db.session.commit()

    return jsonify({
        "message": "New user added" # returning message to user
    }), 201

@app.route("/users", methods=["POST", "GET"])
def updateUser():
    email = request.args.get("email")
    password = request.args.get("password")
    
    u = Users.query.filter_by(email=email, password=password).one_or_none
    if request.method == 'POST':
        # getting all attributes from the form
        new_username = request.form['username']
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_email = request.form['email']
        new_password = request.form['password']
        new_dob = request.form['dob']
        new_phone_no = request.form['phone_no']
        new_height = request.form['height']
        new_weight = request.form['weight']
        new_marketing_language = request.form['marketing_language']
        new_about_me = request.form['about_me']
        new_time_preference_speed = request.form['time_preference_speed']
        new_preferred_unit_metric = request.form['preferred_unit_metric']

        u.username = new_username
        u.email = new_email
        u.password = new_password
        u.first_name = new_first_name
        u.last_name = new_last_name
        u.dob = new_dob
        u.phone_no = new_phone_no
        u.height = new_height
        u.weight = new_weight
        u.marketing_language = new_marketing_language
        u.about_me = new_about_me
        u.time_preference_speed = new_time_preference_speed
        u.preferred_unit_metric = new_preferred_unit_metric

        config.db.session.add(u)
        config.db.commit()

@app.route("/users", methods=["POST"]) 
def deleteUser():
      
        
        



