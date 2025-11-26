CREATE OR ALTER PROCEDURE CW2.DeleteUser
    @username VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @user_ID INT;
    
    SELECT @user_ID = userID
    FROM CW2.Users
    WHERE username = @username;

    IF @user_ID IS NULL
    BEGIN
        THROW 50000, 'Could not find this user. Deletion process cancelled.', 1;
        RETURN;
    END

    BEGIN TRANSACTION;
    BEGIN TRY
        DELETE FROM CW2.UserActivity WHERE userID = @user_ID;
        DELETE FROM CW2.Users WHERE userID = @user_ID;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;



     