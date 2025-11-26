CREATE OR ALTER PROCEDURE CW2.UpdateUser
    @username VARCHAR(100),
    @password VARCHAR(100) = NULL,
    @email VARCHAR(150) = NULL,
    @locationID INT = NULL,
    @phone_no VARCHAR(20) = NULL,
    @height DECIMAL(5,2) = NULL,
    @weight DECIMAL(5,2) = NULL,
    @marketing_language VARCHAR(50) = NULL,
    @about_me VARCHAR(700) = NULL,
    @preferred_unit_metric VARCHAR(10) = NULL,
    @time_preference_speed VARCHAR(10) = NULL
AS
        UPDATE CW2.Users
        SET
            username = COALESCE(@username, username),
            password = COALESCE(@password, password),
            email = COALESCE(@email, email),
            locationID = COALESCE(@locationID, locationID),
            height = COALESCE(@height, height),
            weight = COALESCE(@weight, weight),
            phone_no = COALESCE(@phone_no, phone_no),
            marketing_language = COALESCE(@marketing_language, marketing_language),
            about_me = COALESCE(@about_me, about_me),
            time_preference_speed = 0,
            preferred_unit_metric = COALESCE(@preferred_unit_metric, preferred_unit_metric)
        WHERE username = @username;

    

