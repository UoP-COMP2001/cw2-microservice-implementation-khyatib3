CREATE TRIGGER CW2.trg_AddNewUser 
ON CW2.Users
AFTER INSERT
AS 
BEGIN
    INSERT INTO CW2.AuditUsers (
        admin_role, 
        username, 
        password, 
        locationID,
        email, 
        phone_no, 
        first_name, 
        last_name, 
        dob, 
        height, 
        weight, 
        marketing_language, 
        about_me, 
        preferred_unit_metric, 
        time_preference_speed
    )

    SELECT admin_role, username, password, locationID,
        email, phone_no, first_name, last_name, dob, height, weight, 
        marketing_language, about_me, preferred_unit_metric, time_preference_speed
    FROM inserted
END;