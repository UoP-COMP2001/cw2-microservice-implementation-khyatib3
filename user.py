from config import db, ma
from sqlalchemy.dialects import mssql
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, render_template, request
from models import db, Users, UserActivity, Activity, UserSavedTrails
import config

app = config.connex_app

@app.route("/api/users", methods=["GET"])
def getUser():
    email = request.args.get("email") # get passed in email
    password = request.args.get("password") # get password 
    u: Users = Users.query.filter_by(email == email, password == password).first() # find user with given email and password
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
    
@app.route("/api/users", methods=["PUT"])
def updateUser():
    email = request.args.get("email")
    password = request.args.get("password")
    
    user = Users.query.filter_by(email=email, password=password).one_or_none
    if user:
        # getting all attributes from the form
        new_username = request.form['username']
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_dob = request.form['dob']
        new_phone_no = request.form['phone_no']
        new_height = request.form['height']
        new_weight = request.form['weight']
        new_marketing_language = request.form['marketing_language']
        new_about_me = request.form['about_me']
        new_time_preference_speed = request.form['time_preference_speed']
        new_preferred_unit_metric = request.form['preferred_unit_metric']

        user.username = new_username
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.dob = new_dob
        user.phone_no = new_phone_no
        user.height = new_height
        user.weight = new_weight
        user.marketing_language = new_marketing_language
        user.about_me = new_about_me
        user.time_preference_speed = new_time_preference_speed
        user.preferred_unit_metric = new_preferred_unit_metric


        config.db.session.commit()


@app.route("/api/users", methods=["POST"])
def createNewUser():
    creds = request.get_json(silent=True) or request.form # getting entered login details
    email = creds.get("email") # getting email
    password = creds.get("password") # getting password
    roleID = request.args.get("roleID") # get roleID to know what type of user account to create

    required = ["email", "password"] # these are required fields to create anaccount
    if not all (field in creds for field in required): # checking all required fields are given
        return jsonify({"error_message": "Email and password BOTH are required"}), 400
    
    existing = Users.query.filter_by(email=email).first() # checking for user with same email already existing
    if existing:
        return jsonify({"error_message": "User with this email already exists"}), 409 # returning appropriate message to user
    
    new_user = Users(email=email, password=password, roleID=roleID) # creating new user with email and password and roleID after passing checks
    config.db.session.add(new_user) # adding user
    config.db.session.commit()

    return jsonify({
        "message": "Account created" # returning message to user
    }), 201

@app.route("/api/users", methods=["DELETE"])
def deleteUser():
    email = request.args.get("email") # get passed in username
    user: Users = Users.query.filter_by(email == email).first() # find user with given username

    if user:
        userID = user.userID
        user_activities_list = UserActivity.query.filter_by(userID=userID).all() # getting all the user's activities
        user_saved_trails_list = UserSavedTrails.query.filter_by(userID=userID).all() # getting all the user's saved trails

        for user_activity in user_activities_list:
            config.db.session.delete(user_activity) # delete user activity associations
        
        for user_saved_trail in user_saved_trails_list:
            config.db.session.delete(user_saved_trail) # delete user saved trail associations


        config.db.session.delete(user) # deleting user
        config.db.session.commit()
        return jsonify({ # returning jsonified message
            "message": "User deleted successfully"
        }), 204
    else:
        return jsonify({"error_message": "Could not find this user to delete"}), 404
    

    