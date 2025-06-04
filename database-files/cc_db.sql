DROP DATABASE IF EXISTS cc_database;
CREATE DATABASE cc_database;
USE cc_database;

-- create country table
DROP TABLE IF EXISTS Country;
CREATE TABLE Country
(
    id   INT PRIMARY KEY,
    name        VARCHAR(50),
    region      VARCHAR(50),
    strengths   VARCHAR(50),
    weaknesses  VARCHAR(50),
    score       FLOAT,
    info        VARCHAR(50),
    time        DATETIME
);

-- create users table
DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    id               INT PRIMARY KEY,
    name             VARCHAR(50),
    userType         VARCHAR(50),
    qualityWeight    FLOAT,
    accessibilityWeight FLOAT,
    affordabilityWeight FLOAT,
    outcomeWeight       FLOAT,
    countryID       INT,
    FOREIGN KEY (countryID) REFERENCES Country (id)
);

-- create score projection table
DROP TABLE IF EXISTS score_project;
CREATE TABLE score_project
(
    time    DATETIME,
    targetScore     FLOAT primary key
);


-- create overall score table
DROP TABLE IF EXISTS overall_score;
CREATE TABLE overall_score
(
    overallScore FLOAT PRIMARY KEY,
    qualityScore FLOAT,
    accessibilityScore FLOAT,
    affordabilityScore FLOAT,
    outcomeScore FLOAT
);

-- create factors table
DROP TABLE IF EXISTS factors;
CREATE TABLE factors
(
    factorID    INT PRIMARY KEY,
    name        VARCHAR(50),
    score       FLOAT,
    weight      FLOAT,
    countryID   INT,
    overallScore   FLOAT,
    targetScore     FLOAT,
    FOREIGN KEY (countryID) REFERENCES Country(id),
    FOREIGN KEY (overallScore) REFERENCES overall_score(overallScore),
    FOREIGN KEY (targetScore) REFERENCES score_project(targetScore)
);


-- create comparator table
DROP TABLE IF EXISTS comparator;
CREATE TABLE comparator
(
    country1ID  INT,
    country2ID  INT,
    country3ID INT,
    FOREIGN KEY (country1ID) REFERENCES Country(id),
    FOREIGN KEY (country2ID) REFERENCES Country(id),
    FOREIGN KEY (country3ID) REFERENCES Country(id)
);

-- create country_compare table
DROP TABLE IF EXISTS country_compare;
CREATE TABLE country_compare
(
    countryID   INT,
    Country1_ID   INT,
    Country2_ID    INT,
    Country3_ID   INT,
    FOREIGN KEY (countryID) REFERENCES Country(id)

);

-- create user_score table
DROP TABLE IF EXISTS user_score;
CREATE TABLE user_score
(
    userID   INT,
    overallScore    FLOAT,
    FOREIGN KEY (userID) REFERENCES users(id),
    FOREIGN KEY (overallScore) REFERENCES overall_score(overallScore)
);



