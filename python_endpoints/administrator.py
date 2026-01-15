from flask import jsonify, request, make_response
from config.config import app, db
from models.models import Users, Roles
from schemas.schemas import display_users_schema, display_user_schema
from utility.utilities import authoriseAdmin
from passlib.hash import argon2


def getAllUsers():
    admin_user, error_response = authoriseAdmin()
    if error_response:
        return jsonify(error_response)
    
    all_users = Users.query.filter_by(roleID=2).all()  # get all general users
    return make_response(jsonify(display_users_schema.dump(all_users)), 200)

def getSpecificUser(user_email):
    admin_user, error_response = authoriseAdmin()
    if error_response:
        return jsonify(error_response)
    
    specific_user = Users.query.filter_by(email=user_email).first()  # find user by email
    if not specific_user:
        return make_response(jsonify({"error_message": "User not found"}), 404)
    
    return make_response(jsonify(display_user_schema.dump(specific_user)), 200)

def deleteGeneralUser(user_email):
    admin_user, error_response = authoriseAdmin()
    if error_response:
        return jsonify(error_response)
    
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
     