from marshmallow import fields, Schema, validate
from models.models import Users, UserActivity, Activity, UserSavedTrails

class DisplayAccountSchema(Schema):
    # all fields to show when showing user account info
    username = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    phone_no = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    dob = fields.Date(dump_only=True)
    height = fields.Decimal(dump_only=True)
    weight = fields.Decimal(dump_only=True)
    about_me = fields.Str(dump_only=True)
    marketing_language = fields.Str(dump_only=True)
    preferred_unit_metric = fields.Str(dump_only=True)
    time_preference_speed = fields.Str(dump_only=True)
    
    # use methods to get the actual name/list instead of ids
    location = fields.Method("retrieve_location", dump_only=True)
    activities_list = fields.Method("retrieve_activities", dump_only=True)
    saved_trails = fields.Method("retrieve_saved_trails", dump_only=True)
    role_type = fields.Method("retrieve_role", dump_only=True)

    def retrieve_location(self, obj):
        if obj.location:
            return obj.location.location
        return None

    def retrieve_activities(self, obj):
        activities = [] # activities list
        for activity in obj.activities_list:
            act = Activity.query.get(activity.activityID)
            if act:
                activities.append(act.activity_name)
        return activities

    def retrieve_saved_trails(self, obj):
        trails = []
        for trail in obj.trails_list:
            trails.append({
                'trailID': trail.trailID, # have to return trail id as no trail name
                'trail_saved_timestamp': trail.trail_saved_timestamp # show timestamp for each id too
            })
        return trails

    def retrieve_role(self, obj):
        if obj.role_type:
            return obj.role_type.role_name # for testing to see differentiation in roles
        return None

display_users_schema = DisplayAccountSchema(many=True) # for many users
display_user_schema = DisplayAccountSchema() # for a single user

class CreateAccountSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4, max=40))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
    email = fields.Email(required=True, validate=validate.Length(max=60))
create_account_schema = CreateAccountSchema()

class UpdateAccountSchema(Schema):
    username = fields.Str(validate=validate.Length(min=4, max=40))
    first_name = fields.Str(validate=validate.Length(max=40))
    last_name = fields.Str(validate=validate.Length(max=40))
    dob = fields.Date()
    phone_no = fields.Int()
    height = fields.Decimal()
    weight = fields.Decimal()
    about_me = fields.Str(validate=validate.Length(max=700))
    marketing_language = fields.Str(validate=validate.Length(max=50))
    preferred_unit_metric = fields.Str(validate=validate.Length(max=10))
    time_preference_speed = fields.Str(validate=validate.Length(max=10))
update_account_schema = UpdateAccountSchema()

class UpdateLocationSchema(Schema):
    location = fields.Str(
        required=True,
        validate=[
            validate.Length(max=255),
            validate.Regexp(
                r'^[a-zA-Z\s]+,[a-zA-Z\s]+,[a-zA-Z\s]+$',
                error='Location must be in format: City, County, Country'
            )
        ]
    )
update_location_schema = UpdateLocationSchema()

class DisplayLocationSchema(Schema):
    locationID = fields.Int(dump_only=True)
    location = fields.Str(dump_only=True)
    
display_location_schema = DisplayLocationSchema()
display_locations_schema = DisplayLocationSchema(many=True)