-- createAll.sql
-- 
-- CMSC 447 Team 1 - Fall 2021
-- Professor Abhijit Dutt

CREATE DATABASE IF NOT EXISTS RI_DATA;
USE RI_DATA;

DROP TABLE IF EXISTS Municipality;

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