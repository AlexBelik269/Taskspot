USE master;
GO

DROP DATABASE IF EXISTS TaskSpotDB;
GO

CREATE DATABASE TaskSpotDB;
GO

USE TaskSpotDB;
GO


CREATE TABLE users (
    userID INT IDENTITY,
    user_username VARCHAR(255) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL,
	user_email VARCHAR(255),
	user_city VARCHAR(255)
	primary key(userID)
);

CREATE TABLE tasks(
	taskID INT IDENTITY,
	task_description VARCHAR(500),
	city VARCHAR(255)
	primary key(taskID)
)



