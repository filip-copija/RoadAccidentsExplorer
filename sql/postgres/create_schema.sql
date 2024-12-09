-- Create the database
CREATE DATABASE road_accidents;

-- Connect to the new database
\c road_accidents;

-- Create the regions table
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY, -- Unique region ID
    name VARCHAR(255) NOT NULL,  -- Region name
    type VARCHAR(50) NOT NULL    -- Region type (e.g., country, province, city)
);

-- Create the accidents table
CREATE TABLE accidents (
    accident_id SERIAL PRIMARY KEY, -- Unique accident ID
    region_id INT NOT NULL,         -- Region ID (foreign key)
    year INT NOT NULL,              -- Year
    accident_type VARCHAR(100) NOT NULL, -- Type of accident (e.g., fatalities, injuries)
    value INT NOT NULL,             -- Number of accidents or victims
    unit VARCHAR(20) NOT NULL,      -- Unit of measurement (e.g., count, person)
    FOREIGN KEY (region_id) REFERENCES regions(region_id) -- Relation to regions table
);

-- Add indexes for faster queries
CREATE INDEX idx_regions_name_type ON regions (name, type);
CREATE INDEX idx_accidents_region_year ON accidents (region_id, year);
