from flask import jsonify, request, make_response
from config.config import app, db
from models.models import Users, Roles
from schemas.schemas import display_users_schema
from passlib.hash import argon2


def getAllUsers():
    if not request.authorization:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    # get admin credentials
    admin_email = request.authorization.username
    admin_password = request.authorization.password

    if not admin_email or not admin_password:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401)
    
    # find user with given email to get roleID
    user = Users.query.filter_by(email=admin_email).first()  
    if not user:
        return make_response(jsonify({"error_message": "User not found"}), 404)

    # verify password against user's hashed password
    if not argon2.verify(admin_password, user.hashed_password):
        return make_response(jsonify({"error_message": "Access denied"}), 401)

    roleID = user.roleID  # get user role id
    user_role = Roles.query.filter_by(roleID=roleID).first()  # find user role from roleID
    if not user_role or user_role.role_name != "Admin":
        return make_response(jsonify({"error_message": "Unauthorised access"}), 401)
    
    all_users = Users.query.all()  # get all users
    return make_response(jsonify(display_users_schema.dump(all_users)), 200)  
