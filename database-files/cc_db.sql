DROP DATABASE IF EXISTS cc_database;
CREATE DATABASE cc_database;
USE cc_database;

-- create country table
DROP TABLE IF EXISTS Country;
CREATE TABLE Country
(
    Continent VARCHAR(50),
    name        VARCHAR(50) PRIMARY KEY,
);

DROP TABLE IF EXISTS CountryInfo;
CREATE TABLE CountryInfo
(
    country VARCHAR(50),
    strengths   VARCHAR(50),
    weaknesses  VARCHAR(50),
    score       FLOAT,
    info        VARCHAR(50),
    FOREIGN KEY (country) REFERENCES Country(name),
    FOREIGN KEY (score) REFERENCES Overall_Score("OVERALL SCORE")
)


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
    country       VARCHAR(50),
    FOREIGN KEY (country) REFERENCES Country (name)
);

-- create score projection table
DROP TABLE IF EXISTS score_project;
CREATE TABLE score_project
(
    time    DATETIME,
    targetScore     FLOAT primary key
);

DROP TABLE IF EXISTS Overall_Score
CREATE TABLE Overall_Score(
   Country                                                                                            VARCHAR(31) NOT NULL PRIMARY KEY
  ,Year                                                                                               INTEGER  NOT NULL
  ,"OVERALL SCORE"                                                                                    NUMERIC(4,1) NOT NULL
  ,"1 PREVENTION OF THE EMERGENCE OR RELEASE OF PATHOGENS"                                            NUMERIC(4,1) NOT NULL
  ,"2 EARLY DETECTION REPORTING FOR EPIDEMICS OF POTENTIAL INTL CONCERN"                              NUMERIC(4,1) NOT NULL
  ,"3 RAPID RESPONSE TO AND MITIGATION OF THE SPREAD OF AN EPIDEMIC"                                  NUMERIC(4,1) NOT NULL
  ,"4 SUFFICIENT ROBUST HEALTH SECTOR TO TREAT THE SICK PROTECT HEALTH WORKERS"                       NUMERIC(4,1) NOT NULL
  ,"5 COMMITMENTS TO IMPROVING NATIONAL CAPACITY FINANCING AND ADHERENCE TO NORMS"                    NUMERIC(4,1) NOT NULL
  ,"6 OVERALL RISK ENVIRONMENT AND COUNTRY VULNERABILITY TO BIOLOGICAL THREATS"                       NUMERIC(4,1) NOT NULL

  ,FOREIGN KEY (Country) REFERENCES Country(name)
  );


-- create factors table
DROP TABLE IF EXISTS factors;
CREATE TABLE factors
(
    factorID    INT PRIMARY KEY,
    name        VARCHAR(50),
    score       FLOAT,
    weight      FLOAT,
    country   VARCHAR(50),
    overallScore   FLOAT,
    targetScore     FLOAT,
    FOREIGN KEY (country) REFERENCES Country(name),
    FOREIGN KEY (overallScore) REFERENCES Overall_Score("OVERALL SCORE"),
    FOREIGN KEY (targetScore) REFERENCES score_project(targetScore)
);




-- create comparator table
DROP TABLE IF EXISTS comparator;
CREATE TABLE comparator
(
    country1  VARCHAR(50),
    country2  VARCHAR(50),
    country3 VARCHAR(50),
    FOREIGN KEY (country1) REFERENCES Country(name),
    FOREIGN KEY (country2) REFERENCES Country(name),
    FOREIGN KEY (country3) REFERENCES Country(name)
);

-- create country_compare table
DROP TABLE IF EXISTS country_compare;
CREATE TABLE country_compare
(
    country   VARCHAR(50),
    Country1   VARCHAR(50),
    Country2   VARCHAR(50),
    Country3   VARCHAR(50),
    FOREIGN KEY (country) REFERENCES Country(name)

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

DROP TABLE IF EXISTS regression_model_params;
CREATE TABLE regression_model_params
(
    year INT,
    expenditure FLOAT,
    country VARCHAR(50),
    FOREIGN KEY (country) REFERENCES country(name)
)

DROP TABLE IF EXISTS regression_weights;
CREATE TABLE regression_weights
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(50),
    feature VARCHAR(50),
    slope FLOAT,
    intercept FLOAT,
    mse FLOAT,
    r2 FLOAT
)



