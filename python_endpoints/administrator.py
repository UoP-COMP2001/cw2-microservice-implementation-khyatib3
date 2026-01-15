from flask import jsonify, request, make_response
from config.config import app, db
from models.models import Users, Roles
from schemas.schemas import display_users_schema, display_user_schema, update_account_schema
from marshmallow import ValidationError
from utility.utilities import authoriseAdmin
from passlib.hash import argon2


def getAllUsers():
    admin_user, error_response = authoriseAdmin()
    if error_response:
        status = error_response.get("status", 401)
        return make_response(jsonify({"error_message": error_response.get("error_message", "Unauthorized")}), status)
    
    all_users = Users.query.filter_by(roleID=2).all()  # get all general users
    return make_response(jsonify(display_users_schema.dump(all_users)), 200)

def getSpecificUser(user_email):
    admin_user, error_response = authoriseAdmin()
    if error_response:
        status = error_response.get("status", 401)
        return make_response(jsonify({"error_message": error_response.get("error_message", "Unauthorized")}), status)
    
    specific_user = Users.query.filter_by(email=user_email).first()  # find user by email
    if not specific_user:
        return make_response(jsonify({"error_message": "User not found"}), 404)
    
    return make_response(jsonify(display_user_schema.dump(specific_user)), 200)

def deleteGeneralUser(user_email):
    admin_user, error_response = authoriseAdmin()
    if error_response:
        status = error_response.get("status", 401)
        return make_response(jsonify({"error_message": error_response.get("error_message", "Unauthorized")}), status)
    
    user_to_delete = Users.query.filter_by(email=user_email).first()  # find user by email
    if not user_to_delete:
        return make_response(jsonify({"error_message": "User not found"}), 404)
    
    if user_to_delete.roleID != 2:  # ensure only general users can be deleted
        return make_response(jsonify({"error_message": "Cannot delete non-general user"}), 401)
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted successfully"}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error_message": f"Error deleting user: {user_email}"}), 500)

def performProfileUpdate(user_email):
    admin_user, error_response = authoriseAdmin()
    if error_response:
        status = error_response.get("status", 401)
        return make_response(jsonify({"error_message": error_response.get("error_message", "Unauthorized")}), status)
    
    data = request.get_json() # get data from request body
    
    user_to_update = Users.query.filter_by(email=user_email).first()
    if not user_to_update:
        return make_response(jsonify({"error_message": "User not found"}), 404)
    
    # validate and update user data
    try:
        validated_data = update_account_schema.load(data, partial=True)
    except ValidationError as err:
        return make_response(jsonify({"error_message": err.messages}), 400)
    
    # stop email updates - as email used in auth so cant be changed
    if 'email' in validated_data:
        # Check if user is trying to change their email
        if validated_data['email'] != user_to_update.email:
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
        if existing and existing.userID != user_to_update.userID:
            return make_response(jsonify({"error_message": "Username already taken"}), 409)
        user_to_update.username = validated_data['username']
    
    if 'first_name' in validated_data:
        user_to_update.first_name = validated_data['first_name']
    if 'last_name' in validated_data:
        user_to_update.last_name = validated_data['last_name']
    if 'dob' in validated_data:
        user_to_update.dob = validated_data['dob']
    if 'phone_no' in validated_data:
        user_to_update.phone_no = validated_data['phone_no']
    if 'height' in validated_data:
        user_to_update.height = validated_data['height']
    if 'weight' in validated_data:
        user_to_update.weight = validated_data['weight']
    if 'marketing_language' in validated_data:
        user_to_update.marketing_language = validated_data['marketing_language']
    if 'about_me' in validated_data:
        user_to_update.about_me = validated_data['about_me']
    if 'time_preference_speed' in validated_data:
        user_to_update.time_preference_speed = validated_data['time_preference_speed']
    if 'preferred_unit_metric' in validated_data:
        user_to_update.preferred_unit_metric = validated_data['preferred_unit_metric']
    
    db.session.commit()
    return make_response(jsonify({"message": "User account updated successfully"}), 200)