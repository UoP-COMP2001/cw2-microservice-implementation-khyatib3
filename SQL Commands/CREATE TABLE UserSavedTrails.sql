CREATE TABLE CW2.UserSavedTrails(
    userID INT NOT NULL,
    trailID INT NOT NULL,
    trail_saved_timestamp DATETIME DEFAULT GETDATE() NOT NULL,
    CONSTRAINT pk_savedTrailsID PRIMARY KEY (userID, trailID),
    CONSTRAINT fk_usersavedtrails_user FOREIGN KEY (userID) REFERENCES CW2.Users (userID) ON DELETE CASCADE
);