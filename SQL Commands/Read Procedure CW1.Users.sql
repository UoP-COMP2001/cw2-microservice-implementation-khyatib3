CREATE OR ALTER PROCEDURE CW2.RetrieveUserProfile 
    @username VARCHAR(100)

AS
    SELECT * 
    FROM CW2.ViewUserProfile
    WHERE username = @username;
