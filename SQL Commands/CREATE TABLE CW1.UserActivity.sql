CREATE TABLE CW2.UserActivity(
    activityID INT NOT NULL,
    userID INT NOT NULL,
    CONSTRAINT pk_userActivitiesID PRIMARY KEY (activityID, userID),
    CONSTRAINT fk_userID FOREIGN KEY (userID) REFERENCES CW2.Users (userID),
    CONSTRAINT fk_activityID FOREIGN KEY (activityID) REFERENCES CW2.Activity (activityID)
);