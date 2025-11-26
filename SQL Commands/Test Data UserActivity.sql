INSERT INTO CW2.UserActivity(userID, activityID)
    SELECT usr.userID, activity.activityID
    FROM CW2.Users AS usr
    CROSS JOIN
        CW2.Activity AS activity
    WHERE
        usr.username = 'Grace Hopper' AND activity.activity_name = 'Hiking';

INSERT INTO CW2.UserActivity
    SELECT usr.userID, activity.activityID
    FROM CW2.Users AS usr
    CROSS JOIN
        CW2.Activity AS activity
    WHERE
        usr.username = 'Tim Berners-Lee' AND activity.activity_name = 'Camping';

INSERT INTO CW2.UserActivity
    SELECT usr.userID, activity.activityID
    FROM CW2.Users AS usr
    CROSS JOIN
        CW2.Activity AS activity
    WHERE
        usr.username = 'Ada Lovelace' AND activity.activity_name = 'Horse-back Riding';

INSERT INTO CW2.UserActivity
    SELECT usr.userID, activity.activityID
    FROM CW2.Users AS usr
    CROSS JOIN
        CW2.Activity AS activity
    WHERE
        usr.username = 'spag_hetti3' AND activity.activity_name = 'Walking';

