CREATE PROCEDURE CW2.CreateNewUser
@username VARCHAR(100),
@password VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO CW2.Users (username, password)
    VALUES (@username, @password);
END;

