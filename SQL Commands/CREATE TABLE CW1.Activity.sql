CREATE TABLE CW2.Activity(
    activityID INT identity (1,1) NOT NULL,
    activity_name VARCHAR(50) UNIQUE NOT NULL,
    CONSTRAINT pk_activityID PRIMARY KEY (activityID)
);