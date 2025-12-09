CREATE TABLE CW2.Location(
    locationID INT identity(1,1) NOT NULL UNIQUE,
    location VARCHAR(255),
    CONSTRAINT pk_locationID PRIMARY KEY (locationID)
)