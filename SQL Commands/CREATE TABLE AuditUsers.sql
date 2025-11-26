CREATE TABLE CW2.AuditUsers(
    userID INT identity(1,1) NOT NULL,
    admin_role bit,
    date_of_log DATETIME DEFAULT GETDATE() NOT NULL,
    username VARCHAR(100),
    password VARCHAR(100),
    locationID INT,
    email VARCHAR(150),
    phone_no INT,
    first_name VARCHAR(60),
    last_name VARCHAR(70),
    dob DATE,
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    marketing_language VARCHAR(50),
    about_me VARCHAR(700),
    preferred_unit_metric VARCHAR(10),
    time_preference_speed VARCHAR(10) 
);