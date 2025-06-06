DROP DATABASE IF EXISTS cc_database;
CREATE DATABASE cc_database;
USE cc_database;

-- create country table
DROP TABLE IF EXISTS Countries;
CREATE TABLE Countries
(
    code    VARCHAR(50) PRIMARY KEY
    region  VARCHAR(50),
    name    VARCHAR(50),
);


DROP TABLE IF EXISTS OverallScore
CREATE TABLE OverallScore(
   country                                                                                            VARCHAR(31) NOT NULL PRIMARY KEY
  ,year                                                                                               INTEGER  NOT NULL
  ,overall_score                                                                               NUMERIC(4,1) NOT NULL
  ,"1 PREVENTION OF THE EMERGENCE OR RELEASE OF PATHOGENS"                                        NUMERIC(4,1) NOT NULL
  ,"2 EARLY DETECTION REPORTING FOR EPIDEMICS OF POTENTIAL INTL CONCERN"                       NUMERIC(4,1) NOT NULL
  ,"3 RAPID RESPONSE TO AND MITIGATION OF THE SPREAD OF AN EPIDEMIC"                                NUMERIC(4,1) NOT NULL
  ,"4 SUFFICIENT ROBUST HEALTH SECTOR TO TREAT THE SICK PROTECT HEALTH WORKERS"                       NUMERIC(4,1) NOT NULL
  ,"5 COMMITMENTS TO IMPROVING NATIONAL CAPACITY FINANCING AND ADHERENCE TO NORMS"                    NUMERIC(4,1) NOT NULL
  ,"6 OVERALL RISK ENVIRONMENT AND COUNTRY VULNERABILITY TO BIOLOGICAL THREATS"                      NUMERIC(4,1) NOT NULL

  ,FOREIGN KEY (country) REFERENCES Countries(code)
  );



DROP TABLE IF EXISTS CountryInfo;
CREATE TABLE CountryInfo
(
    countryCode VARCHAR(50),
    strengths   VARCHAR(50),
    weaknesses  VARCHAR(50),
    score       FLOAT,
    info        VARCHAR(50),
    FOREIGN KEY (countryCode) REFERENCES Countries(code),
    FOREIGN KEY (score) REFERENCES OverallScore(overall_score)
)


DROP TABLE IF EXISTS UserRoles;
CREATE TABLE UserROles;
(
    roleID INT PRIMARY KEY,
    roleName VARCHAR(50),
)

-- create users table
DROP TABLE IF EXISTS Users;
CREATE TABLE Users
(
    id               INT PRIMARY KEY,
    name             VARCHAR(50),
    roleID      INT,
    country VARCHAR(50),
    FOREIGN KEY (country) REFERENCES Countries (code).
    FOREIGN KEY (roleID) REFERENCES UserRoles(roleID)
);


-- create factors table
DROP TABLE IF EXISTS Factors;
CREATE TABLE Factors
(
    factorID    INT PRIMARY KEY,
    name        VARCHAR(50),
    score       FLOAT,
    
    FOREIGN KEY (score) REFERENCES OverallScore(overall_score),
);

-- create score projection table
DROP TABLE IF EXISTS score_project;
CREATE TABLE score_project
(
    time    DATETIME,
    targetScore     FLOAT primary key
    factorID        INT,
    FOREIGN KEY (factorID) REFERENCES Factors(factorID)
);


-- create comparator table
DROP TABLE IF EXISTS comparator;
CREATE TABLE comparator
(
    id INT PRIMARY KEY,
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
    country INT,
    slope FLOAT,
    intercept FLOAT,
    mse FLOAT,
    r2 FLOAT,
    factorID INT,
    userID INT,

    FOREIGN KEY (userID) REFERENCES Users(id),
    FOREIGN KEY (country) REFERENCES Countries(code),
    FOREIGN KEY (feature) REFERENCES Factors(factorID)
)

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
    country INT,
    userID INT,

    FOREIGN KEY (userID) REFERENCES Users(id),
    FOREIGN KEY (country) REFERENCES Countries(code)
)

DROP TABLE IF EXISTS regression_model_params;
CREATE TABLE regression_model_params
(
    year INT,
    expenditure FLOAT,
    country VARCHAR(50),
    FOREIGN KEY (country) REFERENCES country(name)
)

DROP TABLE IF EXISTS train_test;
CREATE TABLE train_test
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    train_x INT,
    test_x INT,
    train_y INT,
    test_y INT,
    country INT,
    FOREIGN KEY (country) REFERENCES Countries(code)
)

DROP TABLE IF EXISTS births_table;
CREATE TABLE births_table
(
   COUNTRY     VARCHAR(3) NOT NULL PRIMARY KEY
  ,COUNTRY_GRP VARCHAR(17)
  ,SEX         VARCHAR(3) NOT NULL
  ,YEAR        INTEGER  NOT NULL
  ,VALUE       NUMERIC(5,2) NOT NULL
)





