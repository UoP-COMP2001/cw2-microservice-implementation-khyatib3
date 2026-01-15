from config.config import db, app
from datetime import datetime
import os

# Helper function to get table args
def get_table_args():
    return {"schema": "CW2", 'implicit_returning': False}

# Helper function to get foreign key reference
def fk_ref(table_name, column_name):
  return f"CW2.{table_name}.{column_name}"

# Helper function to get default timestamp function
def get_timestamp_default():
    return db.func.sysdatetime()

class Location(db.Model):
    __tablename__ = "Location"
    __table_args__ = get_table_args()
    locationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(255), nullable=False)        


class Activity(db.Model):
    __tablename__ = "Activity"
    __table_args__ = get_table_args()
    activityID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_name = db.Column(db.String(50), nullable=False)

class UserActivity(db.Model):
    __tablename__ = "UserActivity"
    __table_args__ = get_table_args()
    userID = db.Column(db.Integer, db.ForeignKey(fk_ref('Users', 'userID')), primary_key=True, nullable=False)
    activityID = db.Column(db.Integer, db.ForeignKey(fk_ref('Activity', 'activityID')), primary_key=True, nullable=False)    

class Roles(db.Model):
    __tablename__ = "Roles"
    __table_args__ = get_table_args()
    roleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(10), nullable=False, unique=True)

class UserSavedTrails(db.Model):
    __tablename__ = "UserSavedTrails"
    __table_args__ = get_table_args()
    userID = db.Column(db.Integer, db.ForeignKey(fk_ref('Users', 'userID')), primary_key=True, nullable=False)
    trailID = db.Column(db.Integer, primary_key=True, nullable=False)
    trail_saved_timestamp = db.Column(db.DateTime, nullable=False, server_default=get_timestamp_default())
 

class Users(db.Model):
    __tablename__ = "Users"
    __table_args__ = get_table_args()
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roleID = db.Column(db.Integer, db.ForeignKey(fk_ref('Roles', 'roleID')), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    locationID = db.Column(db.Integer, db.ForeignKey(fk_ref('Location', 'locationId')))
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=True)
    phone_no = db.Column(db.Integer, nullable=True)
    first_name = db.Column(db.String(40), nullable=True)
    last_name = db.Column(db.String(40), nullable=True)
    dob = db.Column(db.Date(), nullable=True)
    height = db.Column(db.Numeric(5,2), nullable=True)
    weight = db.Column(db.Numeric(5,2), nullable=True)
    marketing_language = db.Column(db.String(50), nullable=True)
    about_me = db.Column(db.String(700), nullable=True)
    preferred_unit_metric = db.Column(db.String(10), nullable=True)
    time_preference_speed = db.Column(db.String(10), nullable=True)
    
    # set up associations between the link tables
    location = db.relationship('Location', backref='users')
    activities_list = db.relationship('UserActivity', backref='users', cascade="all, delete-orphan")
    trails_list = db.relationship('UserSavedTrails', backref='users', cascade="all, delete-orphan")
    role_type = db.relationship('Roles', backref='users')
