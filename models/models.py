from sqlalchemy.dialects import mssql
from config.config import db

class Location(db.Model):
    __tablename__ = "Location"
    __table_args__ = {"schema": "CW2", 'implicit_returning':False}
    locationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(255), nullable=False)        


class Activity(db.Model):
    __tablename__ = "Activity"
    __table_args__ = {"schema": "CW2", 'implicit_returning':False}
    activityID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_name = db.Column(db.String(50), nullable=False)

class UserActivity(db.Model):
    __tablename__ = "UserActivity"
    __table_args__ = {"schema": "CW2", 'implicit_returning':False}
    userID = db.Column(db.Integer, db.ForeignKey('CW2.Users.userID'), primary_key=True, nullable=False)
    activityID = db.Column(db.Integer, db.ForeignKey('CW2.Activity.activityID'), primary_key=True, nullable=False)    

class Roles(db.Model):
    __tablename__ = "Roles"
    __table_args__ = {"schema": "CW2", 'implicit_returning': False}
    roleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(10), nullable=False, unique=True)

class UserSavedTrails(db.Model):
    __tablename__ = "UserSavedTrails"
    __table_args__ = {"schema": "CW2", 'implicit_returning': False}
    userID = db.Column(db.Integer, db.ForeignKey('CW2.Users.userID'), primary_key=True,  nullable=False)
    trailID = db.Column(db.Integer, primary_key=True, nullable=False)
    trail_saved_timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.sysdatetime())
 

class Users(db.Model):
    __tablename__ = "Users"
    __table_args__ = {"schema": "CW2", 'implicit_returning':False}
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roleID = db.Column(db.Integer, db.ForeignKey('CW2.Roles.roleID'), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    locationID = db.Column(db.Integer, db.ForeignKey('CW2.Location.locationID'))
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
