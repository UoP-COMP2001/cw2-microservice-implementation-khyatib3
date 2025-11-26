CREATE OR ALTER VIEW CW2.ViewUserProfile AS
SELECT us.username, us.email, us.first_name, us.last_name, us.dob, us.about_me, us.height, us.weight, us.marketing_language, us.preferred_unit_metric, COUNT(act.activity_name) AS number_of_activities
FROM CW2.Users AS us
LEFT JOIN CW2.UserActivity as favAct ON us.userID = favAct.userID
LEFT JOIN CW2.Activity as act ON favAct.activityID = act.activityID
GROUP BY us.username, us.email, us.first_name, us.last_name, us.dob, us.about_me, us.height, us.weight, us.marketing_language,us.preferred_unit_metric;

