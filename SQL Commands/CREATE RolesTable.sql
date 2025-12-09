CREATE TABLE CW2.Roles(
    roleID TINYINT identity(0,1) NOT NULL,
    role_name VARCHAR(10) UNIQUE NOT NULL,
    CONSTRAINT pk_roleID PRIMARY KEY (roleID),
    CONSTRAINT chk_role CHECK (role_name IN ('User', 'Admin'))
);