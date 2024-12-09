CREATE DATABASE road_accidents;

\c road_accidents;

CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    UNIQUE(name, type)
);

CREATE TABLE accident_types (
    accident_type_id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    UNIQUE(category)
);

CREATE TABLE units (
    unit_id SERIAL PRIMARY KEY,
    unit_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE accidents (
    accident_id SERIAL PRIMARY KEY,
    region_id INT NOT NULL,
    accident_type_id INT NOT NULL,
    year INT NOT NULL,
    value INT NULL,
    unit_id INT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE CASCADE,
    FOREIGN KEY (accident_type_id) REFERENCES accident_types(accident_type_id) ON DELETE CASCADE,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id) ON DELETE CASCADE
);

CREATE INDEX idx_regions_name_type ON regions (name, type);
CREATE INDEX idx_accidents_region_year ON accidents (region_id, year);
CREATE INDEX idx_accidents_type_year ON accidents (accident_type_id, year);
