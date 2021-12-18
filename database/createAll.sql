-- createAll.sql
-- 
-- CMSC 447 Team 1 - Fall 2021
-- Professor Abhijit Dutt

CREATE DATABASE IF NOT EXISTS RI_DATA;
USE RI_DATA;

DROP TABLE IF EXISTS Monthly_Hospital;
DROP TABLE IF EXISTS Monthly_Deaths;
DROP TABLE IF EXISTS Monthly_Cases;
DROP TABLE IF EXISTS Monthly_Vax_Nums;
DROP TABLE IF EXISTS Counties;
DROP TABLE IF EXISTS State;

CREATE TABLE IF NOT EXISTS State
(
	state_id	INT NOT NULL,
    state_name	VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY(state_id)

);

CREATE TABLE IF NOT EXISTS Counties
(
	fips						INT NOT NULL,
    state_id					INT NOT NULL,
    county_name 				VARCHAR(20) NOT NULL,
    geo_json_data				TEXT NOT NULL,
    total_cases					INT NOT NULL,
    case_rate_per_100k			INT NOT NULL,
    total_hospital				INT NOT NULL,
    hospital_rate_per_100k		INT NOT NULL,
    total_deaths				INT NOT NULL,
    death_rate_per_100k			INT NOT NULL,
    total_vaccinated			INT NOT NULL,
    vaccinated_rate_per_100k	INT NOT NULL,
    last_updated_timestamp		VARCHAR(30) NOT NULL,
    PRIMARY KEY(fips),
    FOREIGN KEY(state_id) REFERENCES State(state_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Monthly_Cases
(
	fips 			INT NOT NULL,
    infection_month	INT NOT NULL,
    infection_year	INT NOT NULL,
    num_cases		INT NOT NULL,
    rate_cases		INT NOT NULL,
    last_updated	VARCHAR(30) NOT NULL,
    PRIMARY KEY(fips, infection_month, infection_year),
    FOREIGN KEY(fips) REFERENCES Counties(fips) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Monthly_Vax_Nums
(
	fips 			INT NOT NULL,
    vaxxed_month	INT NOT NULL,
    vaxxed_year		INT NOT NULL,
    num_vaxxed		INT NOT NULL,
    rate_vaxxed		INT NOT NULL,
    last_updated	VARCHAR(30) NOT NULL,
    PRIMARY KEY(fips, vaxxed_month, vaxxed_year),
    FOREIGN KEY(fips) REFERENCES Counties(fips) ON DELETE CASCADE			
);

CREATE TABLE IF NOT EXISTS Monthly_Deaths
(
	fips 			INT NOT NULL,
    death_month		INT NOT NULL,
    death_year		INT NOT NULL,
    num_deaths		INT NOT NULL,
    rate_deaths		INT NOT NULL,
    last_updated	VARCHAR(30) NOT NULL,
    PRIMARY KEY(fips, death_month, death_year),
    FOREIGN KEY(fips) REFERENCES Counties(fips) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Monthly_Hospital
(
	fips 			INT NOT NULL,
    hospit_month	INT NOT NULL,
    hospit_year		INT NOT NULL,
    num_hospit		INT NOT NULL,
    rate_hospit		INT NOT NULL,
    last_updated	VARCHAR(30) NOT NULL,
    PRIMARY KEY(fips, hospit_month, hospit_year),
    FOREIGN KEY(fips) REFERENCES Counties(fips) ON DELETE CASCADE
);

CREATE INDEX fips_counties ON Counties(fips);
CREATE INDEX fips_case ON Monthly_Cases(fips);
CREATE INDEX fips_vaxx ON Monthly_Vax_Nums(fips);
CREATE INDEX fips_death ON Monthly_Deaths(fips);
CREATE INDEX fips_hospit ON Monthly_Hospital(fips);
