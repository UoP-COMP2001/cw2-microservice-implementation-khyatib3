from config.config import db, ma
from sqlalchemy.dialects import mssql
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, render_template, request
from models.models import Users, UserActivity, Activity, UserSavedTrails, Roles
from schemas.schemas import create_account_schema, display_user_schema, update_account_schema
from marshmallow import ValidationError
import authenticator
# GET -- show user's own details
def getUser():
    email = request.authorization.username
    password = request.authorization.password

    if not email or not password:
        return jsonify({"error_message": "Email and password not found"}), 401 # returning appropriate message to user

    u: Users = Users.query.filter_by(email = email, password = password).first() # find user with given email and password

    if u:
        if u.email != email or u.password != password:
            return jsonify({"error_message": "Access denied"}), 401 # returning appropriate message to user
        else:
            return jsonify(display_user_schema.dump(u)), 200 # returning user data if found
    else:
        return jsonify({"error_mesage": "Error occured locating user"}), 404 # or return error message if that user was not found
    
# PUT -- update user's own details
def updateUser():
    email = request.authorization.username
    password = request.authorization.password

    new_data = request.get_json()
    if not email or not password:
        return jsonify({"error_message": "Credentials not found"}), 401 # returning appropriate message to user
    
    user = Users.query.filter_by(email=email, password=password).one_or_none
    if user:
        # getting all attributes from the form
        user.username = new_data.username
        user.first_name = new_data.first_name
        user.last_name = new_data.last_name
        user.dob = new_data.dob
        user.email = new_data.email
        user.phone_no = new_data.phone_no
        user.height = new_data.height
        user.weight = new_data.weight
        user.marketing_language = new_data.marketing_language
        user.about_me = new_data.about_me
        user.time_preference_speed = new_data.time_preference_speed
        user.preferred_unit_metric = new_data.preferred_unit_metric

        new_user_data = update_account_schema.load(new_data, instance=user, partial=True)
        db.session.add(new_user_data)
        db.session.commit()
        return jsonify({"message": "User account updated successfully"}), 200
    else:
        return jsonify({"error_message": "User not found"}), 404

# POST -- add activity to user's own profile
def addActivity(activity_name):
    if not request.authorization:
        return jsonify({"error_message": "Credentials not found"}), 401
    
    email = request.authorization.username
    password = request.authorization.password
    
    # find the user
    user = Users.query.filter_by(email=email, password=password).one_or_none()
    if not user:
        return jsonify({"error_message": "User not found"}), 404
    
    # find activity via name
    activity = Activity.query.filter_by(activity_name=activity_name).first()
    if not activity: # if activity wasnt found
        return jsonify({"error_message": "Activity not found"}), 404
    
    # get activity id from activity
    activityID = activity.activityID
    
    # check that the user doesnt already have this activity
    existing_user_activity = UserActivity.query.filter_by(userID=user.userID, activityID=activityID).first()
    if existing_user_activity:
        return jsonify({"error_message": "User already has this activity"}), 409 # returning appropriate message to user
    
    # add the updated activity
    new_user_activity = UserActivity(userID=user.userID, activityID=activityID)
    db.session.add(new_user_activity)
    db.session.commit()
        

# POST -- create a new user account
def createNewUser():
    creds = request.get_json() or request.form # getting entered login details
    username = creds.get("username") # getting username since backlog says user wants to create account with username
    email = creds.get("email") # getting email
    password = creds.get("password") # getting password
    roleID = "2" # set roleID to belong to general user role by default

    existing_email = Users.query.filter_by(username=username).first() # checking for user with same email already existing
    if existing_email:
        return jsonify({"error_message": "User with this email already exists"}), 409 # returning appropriate message to user
    
    existing_username = Users.query.filter_by(username=username).first() # checking for user with same username already existing
    if existing_username:
        return jsonify({"error_message": "Username already taken"}), 409 # returning appropriate message to user

    # validate data using schema after ensuring no duplication
    try:
        validated_data = create_account_schema.load(creds)
    except ValidationError as err:
        return jsonify({"error_message": err.messages}), 400
    
    # create new user account
    new_user = Users(username=username, password=password, roleID=roleID, email=email) # creating new user with username email and password and roleID after passing checks
    db.session.add(new_user) # adding user
    db.session.commit()

    return jsonify({
        "message": "Account created" # returning message to user
    }), 201


# DELETE -- delete user's own account
def deleteUser():
    email = request.authorization.username
    password = request.authorization.password

    if not email or not password:
        return jsonify({"error_message": "Email and password not found"}), 401 # returning appropriate message to user

    user: Users = Users.query.filter_by(email == email).first() # find user with given username
    
    if user.email != email or user.password != password:
        return jsonify({"error_message": "Access denied"}), 401 # returning appropriate message to user

    if user:
        db.session.delete(user) # deleting user
        db.session.commit()
        return jsonify({ # returning jsonified message
            "message": "User deleted successfully"
        }), 204
    else:
        return jsonify({"error_message": "Could not find this user to delete"}), 404
    

    