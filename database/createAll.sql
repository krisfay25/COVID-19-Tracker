-- createAll.sql
-- 
-- CMSC 447 Team 1 - Fall 2021
-- Professor Abhijit Dutt

CREATE DATABASE IF NOT EXISTS RI_DATA;
USE RI_DATA;

DROP TABLE IF EXISTS Municipality;
DROP TABLE IF EXISTS Monthly_Cases;

CREATE TABLE IF NOT EXISTS Municipality
(
	county 						VARCHAR(20) NOT NULL,
    municipality 				VARCHAR(20) NOT NULL UNIQUE,
    total_cases					INT NOT NULL,
    case_rate_per_100k			INT NOT NULL,
    total_hospital				INT NOT NULL,
    hospital_rate_per_100k		INT NOT NULL,
    total_deaths				INT NOT NULL,
    death_rate_per_100k			INT NOT NULL,
    total_vaccinated			INT NOT NULL,
    vaccinated_rate_per_100k	INT NOT NULL,
    PRIMARY KEY(municipality)
);

CREATE TABLE IF NOT EXISTS Monthly_Cases
(
	county 			VARCHAR(20) NOT NULL,
    municipality 	VARCHAR(20) NOT NULL UNIQUE,
    mar_2020		INT NOT NULL,
    apr_2020		INT NOT NULL,
	may_2020		INT NOT NULL,
    jun_2020		INT NOT NULL,
    jul_2020		INT NOT NULL,
    aug_2020		INT NOT NULL,
    sep_2020		INT NOT NULL,
    oct_2020		INT NOT NULL,
    nov_2020		INT NOT NULL,
    dec_2020		INT NOT NULL,
    jan_2021		INT NOT NULL,
    feb_2021		INT NOT NULL,
    mar_2021		INT NOT NULL,
    apr_2021		INT NOT NULL,
    may_2021		INT NOT NULL,
    jun_2021		INT NOT NULL,
    jul_2021		INT NOT NULL,
    aug_2021		INT NOT NULL,
    sep_2021		INT NOT NULL,
    total			INT NOT NULL,
    PRIMARY KEY(municipality)
);

CREATE TABLE IF NOT EXISTS Monthly_Vax_Nums
(
	county 			VARCHAR(20) NOT NULL,
    municipality 	VARCHAR(20) NOT NULL UNIQUE,
    population		INT NOT NULL,
    dec_2020		INT NOT NULL,
    jan_2021		INT NOT NULL,
    feb_2021		INT NOT NULL,
    mar_2021		INT NOT NULL,
    apr_2021		INT NOT NULL,
    may_2021		INT NOT NULL,
    jun_2021		INT NOT NULL,
    jul_2021		INT NOT NULL,
    aug_2021		INT NOT NULL,
    sep_2021		INT NOT NULL,
    oct_2021		INT NOT NULL,
    PRIMARY KEY(municipality)			

);