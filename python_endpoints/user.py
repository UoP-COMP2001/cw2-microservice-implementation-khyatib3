from config.config import db, ma, app
from flask import jsonify, request, make_response
from models.models import Users, UserActivity, Activity, UserSavedTrails, Roles, Location
from schemas.schemas import create_account_schema, display_user_schema, update_account_schema, update_location_schema
from marshmallow import ValidationError
from passlib.hash import argon2
import authenticator

def getUser():
    if not request.authorization:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    email = request.authorization.username
    password = request.authorization.password

    if not email or not password:
        return make_response(jsonify({"error_message": "Email and password not found"}), 401)

    u = Users.query.filter_by(email=email).first()  # find user with given email
    if not u:
        return make_response(jsonify({"error_message": "Error occurred locating user"}), 404)
    
    # verify password using argon 2
    if not argon2.verify(password, u.hashed_password):
        return make_response(jsonify({"error_message": "Access denied"}), 401)

    return make_response(jsonify(display_user_schema.dump(u)), 200)
    
def updateUser():
    if not request.authorization:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    email = request.authorization.username
    password = request.authorization.password

    new_data = request.get_json()
    if not email or not password:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    # find user, if not found return 404
    user = Users.query.filter_by(email=email).first()
    if not user:
        return make_response(jsonify({"error_message": "User not found"}), 404)
    
    # verify password
    if not argon2.verify(password, user.hashed_password):
        return make_response(jsonify({"error_message": "Access denied"}), 401)
    
    # get user role
    user_role = Roles.query.filter_by(roleID=user.roleID).first()
    is_admin = user_role and user_role.role_name == "Admin"
    is_regular_user = user_role and user_role.role_name == "User"
    
    # stop general users from updating admin users (safety measure)
    if user.roleID == 1 and is_regular_user:
        return make_response(jsonify({"error_message": "Users with 'User' role cannot update Admin users"}), 403)
    
    # validate and update user data
    try:
        validated_data = update_account_schema.load(new_data, partial=True)
    except ValidationError as err:
        return make_response(jsonify({"error_message": err.messages}), 400)
    
    # stop email updates - as email used in auth so cant be changed
    if 'email' in validated_data:
        # Check if user is trying to change their email
        if validated_data['email'] != user.email:
            return make_response(jsonify({"error_message": "Email cannot be changed. Email is used for authentication and must remain unchanged."}), 400)
        # Remove email from validated_data to prevent any update attempt
        validated_data.pop('email')
    
    # stop user from changing role via this endpoint (security measure)
    if 'roleID' in validated_data:
        return make_response(jsonify({"error_message": "Role cannot be changed through this endpoint"}), 400)
    
    # update user fields
    if 'username' in validated_data:
        # check if username is already taken by another user
        existing = Users.query.filter_by(username=validated_data['username']).first()
        if existing and existing.userID != user.userID:
            return make_response(jsonify({"error_message": "Username already taken"}), 409)
        user.username = validated_data['username']
    
    if 'password' in validated_data:
        user.hashed_password = argon2.hash(validated_data['password'])
    
    if 'first_name' in validated_data:
        user.first_name = validated_data['first_name']
    if 'last_name' in validated_data:
        user.last_name = validated_data['last_name']
    if 'dob' in validated_data:
        user.dob = validated_data['dob']
    if 'phone_no' in validated_data:
        user.phone_no = validated_data['phone_no']
    if 'height' in validated_data:
        user.height = validated_data['height']
    if 'weight' in validated_data:
        user.weight = validated_data['weight']
    if 'marketing_language' in validated_data:
        user.marketing_language = validated_data['marketing_language']
    if 'about_me' in validated_data:
        user.about_me = validated_data['about_me']
    if 'time_preference_speed' in validated_data:
        user.time_preference_speed = validated_data['time_preference_speed']
    if 'preferred_unit_metric' in validated_data:
        user.preferred_unit_metric = validated_data['preferred_unit_metric']
    
    db.session.commit()
    return make_response(jsonify({"message": "User account updated successfully"}), 200)

def addActivity(activity_name):
    if not request.authorization:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    email = request.authorization.username
    password = request.authorization.password
    
    # if neither credential found/provided
    if not email or not password:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    # find user
    user = Users.query.filter_by(email=email).first()
    if not user:
        return make_response(jsonify({"error_message": "User not found"}), 404)
    
    # verify password
    if not argon2.verify(password, user.hashed_password):
        return make_response(jsonify({"error_message": "Access denied"}), 401)
    
    # find activity via name
    activity = Activity.query.filter_by(activity_name=activity_name).first()
    if not activity:  # if activity wasn't found
        return make_response(jsonify({"error_message": "Activity not found"}), 404)
    
    # get activity id from activity
    activityID = activity.activityID
    
    # check that the user doesn't already have this activity
    existing_user_activity = UserActivity.query.filter_by(userID=user.userID, activityID=activityID).first()
    if existing_user_activity:
        return make_response(jsonify({"error_message": "User already has this activity"}), 409)
    
    # add the activity
    new_user_activity = UserActivity(userID=user.userID, activityID=activityID)
    db.session.add(new_user_activity)
    db.session.commit()
    
    return make_response(jsonify({"message": "Activity added successfully"}), 201)

def updateUserOwnLocation(location):
    if not request.authorization:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    # get credentials from authorization header
    email = request.authorization.username
    password = request.authorization.password

    if not email or not password:
        return make_response(jsonify({"error_message": "Email and password not found"}), 401)

    user = Users.query.filter_by(email=email).first()  # find user with given email
    
    if not user:
        return make_response(jsonify({"error_message": "Could not find this user to update location"}), 404)
    
    # verify password
    if not argon2.verify(password, user.hashed_password):
        return make_response(jsonify({"error_message": "Access denied"}), 401)
    
    # validate location format
    try:
        validated_data = update_location_schema.load({"location": location})
    except ValidationError as err:
        return make_response(jsonify({"error_message": err.messages}), 400)
    
    # find location in database
    location_obj = Location.query.filter_by(location=location).first()
    if not location_obj:
        return make_response(jsonify({"error_message": "Location does not exist"}), 404)
    
    # update user's locationID
    user.locationID = location_obj.locationId
    db.session.commit()
    return make_response(jsonify({"message": "User's location updated successfully"}), 200)

def createNewUser(): # no authentication required
    creds = request.get_json() or request.form  # getting entered login details
    
    # validate data using schema first
    try:
        validated_data = create_account_schema.load(creds)
    except ValidationError as err:
        return make_response(jsonify({"error_message": err.messages}), 400)
    
    username = validated_data.get("username")
    email = validated_data.get("email")
    password = validated_data.get("password")
    roleID = 2  # set roleID to belong to general user role by default

    # extra email validation (safety measure)
    if not email:
        return make_response(jsonify({"error_message": "Email is required"}), 400)
    
    # convert to lowercase adn remove whitespaces
    email = email.lower().strip()
    
    # check for existing email (case-insensitive check)
    existing_email = Users.query.filter_by(email=email).first()
    if existing_email:
        return make_response(jsonify({"error_message": "User with this email already exists"}), 409)
    
    # check for existing username
    existing_username = Users.query.filter_by(username=username).first()
    if existing_username:
        return make_response(jsonify({"error_message": "Username already taken"}), 409)
    
    # hash the password with argon 2
    hashed_password = argon2.hash(password)
    
    # create new user account
    new_user = Users(
        username=username,
        hashed_password=hashed_password,
        roleID=roleID,
        email=email
    )
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({
        "message": "Account created"
    }), 201)

def deleteUser():
    if not request.authorization:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    email = request.authorization.username
    password = request.authorization.password
    
    # if neither credential found/provided
    if not email or not password:
        return make_response(jsonify({"error_message": "Email and password not found"}), 401)
    
    user = Users.query.filter_by(email=email).first()  # find user with given email
    
    #if user not found
    if not user:
        return make_response(jsonify({"error_message": "Could not find this user to delete"}), 404)
    
    # verify password
    if not argon2.verify(password, user.hashed_password):
        return make_response(jsonify({"error_message": "Access denied"}), 401)
    
    # get current user role
    user_role = Roles.query.filter_by(roleID=user.roleID).first()
    is_admin = user_role and user_role.role_name == "Admin"
    is_regular_user = user_role and user_role.role_name == "User"
    
    # if admin stop admin from deleting themselves
    if is_admin:
        return make_response(jsonify({"error_message": "Admin users cannot delete themselves"}), 403)
    
    # stop user from deleting admin (if happens) -- safety measure
    if user.roleID == 1 and is_regular_user:
        
        return make_response(jsonify({"error_message": "Users with 'User' role cannot delete Admin users"}), 403)
    
    # proceed with deletion
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({
        "message": "User deleted successfully"
    }), 204)
    

    