DROP DATABASE IF EXISTS cc_database;
CREATE DATABASE cc_database;
USE cc_database;


DROP TABLE IF EXISTS Countries;
CREATE TABLE Countries
(
    region  VARCHAR(50),
    name    VARCHAR(50),
    code    VARCHAR(50) PRIMARY KEY

);

DROP TABLE IF EXISTS OverallScore;
CREATE TABLE OverallScore(
    scoreID INT AUTO_INCREMENT PRIMARY KEY,
    country          VARCHAR(31) NOT NULL,
    year             INTEGER  NOT NULL,
    overall_score    FLOAT NOT NULL,
    prevention       FLOAT NOT NULL,
    detectReport     FLOAT NOT NULL,
    rapidResp        FLOAT NOT NULL,
    healthSys        FLOAT NOT NULL,
    intlNorms        FLOAT NOT NULL,
    riskEnv          FLOAT NOT NULL,

    FOREIGN KEY (country) REFERENCES Countries(code)
  );


DROP TABLE IF EXISTS CountryInfo;
CREATE TABLE CountryInfo
(
    countryCode VARCHAR(50),
    strengths   VARCHAR(50),
    weaknesses  VARCHAR(50),
    score       INT,
    info        VARCHAR(50),
    FOREIGN KEY (countryCode) REFERENCES Countries(code),
    FOREIGN KEY (score) REFERENCES OverallScore(scoreID)
);


DROP TABLE IF EXISTS UserRoles;
CREATE TABLE UserRoles
(
    roleID INT PRIMARY KEY,
    roleName VARCHAR(50)
);

DROP TABLE IF EXISTS Users;
CREATE TABLE Users
(
    id               INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(50),
    roleID           INT,
    country          VARCHAR(50),
    FOREIGN KEY (country) REFERENCES Countries (code),
    FOREIGN KEY (roleID) REFERENCES UserRoles(roleID)
);


DROP TABLE IF EXISTS Factors;
CREATE TABLE Factors
(
    factorID    INT PRIMARY KEY,
    name        VARCHAR(50),
    score       INT,
    
    FOREIGN KEY (score) REFERENCES OverallScore(scoreID)
);

DROP TABLE IF EXISTS score_project;
CREATE TABLE score_project
(
    time    DATETIME,
    targetScore     FLOAT primary key,
    factorID        INT,
    FOREIGN KEY (factorID) REFERENCES Factors(factorID)
);


DROP TABLE IF EXISTS comparator;
CREATE TABLE comparator
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    country1  VARCHAR(50),
    country2  VARCHAR(50),
    country3 VARCHAR(50),
    FOREIGN KEY (country1) REFERENCES Countries(code),
    FOREIGN KEY (country2) REFERENCES Countries(code),
    FOREIGN KEY (country3) REFERENCES Countries(code)
);

DROP TABLE IF EXISTS regression_weights;
CREATE TABLE regression_weights
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(50),
    slope FLOAT,
    intercept FLOAT,
    mse FLOAT,
    r2 FLOAT,
    factorID INT,
    userID INT,

    FOREIGN KEY (userID) REFERENCES Users(id),
    FOREIGN KEY (country) REFERENCES Countries(code),
    FOREIGN KEY (factorID) REFERENCES Factors(factorID)
);

DROP TABLE IF EXISTS cosine_weights;
CREATE TABLE cosine_weights
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    preventionWeight FLOAT,
    healthSysWeight FLOAT,
    rapidRespWeight FLOAT,
    intlNormsWeight FLOAT,
    riskEnvWeight FLOAT,
    detectReportWeight FLOAT,
    country VARCHAR(50),
    userID INT,

    FOREIGN KEY (userID) REFERENCES Users(id),
    FOREIGN KEY (country) REFERENCES Countries(code)
);

DROP TABLE IF EXISTS regression_model_params;
CREATE TABLE regression_model_params
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    expenditure FLOAT,
    country VARCHAR(50),
    FOREIGN KEY (country) REFERENCES Countries(code)
);

DROP TABLE IF EXISTS train_test;
CREATE TABLE train_test
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    train_x INT,
    test_x INT,
    train_y INT,
    test_y INT,
    country VARCHAR(50),
    FOREIGN KEY (country) REFERENCES Countries(code)
);

DROP TABLE IF EXISTS births_table;
CREATE TABLE births_table
(
   COUNTRY     VARCHAR(50) NOT NULL 
  ,COUNTRY_GRP VARCHAR(50)
  ,SEX         VARCHAR(50) NOT NULL
  ,YEAR        INTEGER  NOT NULL
  ,VALUE       NUMERIC(5,2) NOT NULL
  ,FOREIGN KEY (COUNTRY) REFERENCES Countries(code)
);





