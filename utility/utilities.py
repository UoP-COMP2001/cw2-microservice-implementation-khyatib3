from config.config import app , db
from flask import request
from models.models import Users, Roles
from passlib.hash import argon2
import os

# helper function to authorise admin users
def authoriseAdmin():
    if not request.authorization:
        return None, {"error_message": "Credentials not found", "status": 401}
    
    email = request.authorization.username
    password = request.authorization.password
    
    if not email or not password:
        return None, {"error_message": "Email and password not found", "status": 401}
    
    #find user with given email
    user = Users.query.filter_by(email=email).first()
    if not user:
        return None, {"error_message": "User not found", "status": 404}
    
    # verify pasword with argon2
    if not argon2.verify(password, user.hashed_password):
        return None, {"error_message": "Access denied", "status": 401}
    
    # get user role to check if theyre admin
    user_role = Roles.query.filter_by(roleID=user.roleID).first()
    if not user_role or user_role.role_name != "Admin":
        return None, {"error_message": "Unauthorised access", "status": 401}
    
    #return user if authorised
    return user, None
