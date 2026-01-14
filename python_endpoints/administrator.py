import pyodbc
from flask import Flask, jsonify, request, make_response, abort
from config.config import db
from models.models import Users, UserActivity, UserSavedTrails, Location, Activity, Roles
from schemas.schemas import display_users_schema, display_user_schema, update_account_schema, create_account_schema
from connexion import context
from passlib.hash import argon2

# set the session
session = db.session

# GET -- get all users'
def getAllUsers():
    if not request.authorization:
        return make_response(jsonify({"error_message": "Credentials not found"}), 401) # returning appropriate message to user
    
    admin_email = request.authorization.username

    user = Users.query.filter_by(email=admin_email).first() # find user with email
    if not user:
        return make_response(jsonify({"error_message": "User not found"}), 404) # if user not found, return 404

    roleID = user.roleID # get user role id
    user_role = Roles.query.filter_by(roleID=roleID).first() # find user role
    if user_role.role_name != "Admin":
        return make_response(jsonify({"error_message": "Unauthorised access"}), 401) # if role is not admin, return unauthorised access message
    else:
        all_users = Users.query.all() # get all users
        return make_response(jsonify(display_users_schema.dump(all_users)), 200) # return all users data  
