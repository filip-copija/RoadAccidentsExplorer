-- summary_overall: Provides a summary of accidents across Poland for all categories since 2014, grouped by region type and accident category.
CREATE OR REPLACE VIEW summary_overall AS
SELECT
    r.region_id,
    r.name AS region_name,
    r.type AS region_type,
    at.category AS accident_category,
    SUM(a.value) AS total_value
FROM accidents a
JOIN accident_types at ON a.accident_type_id = at.accident_type_id
JOIN regions r ON a.region_id = r.region_id
WHERE r.name = 'POLSKA' and a.year >= 2014

-- summary_by_region_and_category: Aggregates accident data by region, category, and year for all regions since 2014.
CREATE OR REPLACE VIEW summary_by_region_and_category AS
SELECT
    r.region_id,
    r.name AS region_name,
    r.type AS region_type,
    at.category AS accident_category,
    a.year,
    SUM(a.value) AS total_value
FROM accidents a
JOIN accident_types at ON a.accident_type_id = at.accident_type_id
JOIN regions r ON a.region_id = r.region_id
WHERE a.year >= 2014
GROUP BY r.region_id, r.name, r.type, at.category, a.year;

-- accidents_by_vehicle: Focuses on accidents involving specific vehicle categories, aggregated by region and year for the period 2014-2023.
CREATE OR REPLACE VIEW accidents_by_vehicle AS
SELECT
    r.region_id,
    r.name AS region_name,
    r.type AS region_type,
    at.category AS accident_category,
    SUM(a.value) AS total_accidents,
    a.year
FROM accidents a
JOIN accident_types at ON a.accident_type_id = at.accident_type_id
JOIN regions r ON a.region_id = r.region_id
WHERE at.category IN (
    'samochody osobowe',
    'motocykle',
    'motocykle o pojemności silnika do 125 cm3',
    'rowery',
    'motorowery',
    'samochody ciężarowe',
    'hulajnogi elektryczne			',
    'urządzenie transportu osobistego',
    'inne pojazdy - ogółem',
    'inne pojazdy - pojazd nieustalony'
) AND a.year BETWEEN 2014 AND 2023
GROUP BY r.region_id, r.name, r.type, at.category, a.year
ORDER BY r.region_id, a.year;

-- accidents_over_time: Displays the total number of accidents ("wypadki ogółem") over time (2014-2023), grouped by region and year.
CREATE OR REPLACE VIEW accidents_over_time AS
SELECT
    r.region_id,
    r.name AS region_name,
    r.type AS region_type,
    a.year,
    SUM(a.value) AS total_accidents
FROM accidents a
JOIN regions r ON a.region_id = r.region_id
JOIN accident_types at ON a.accident_type_id = at.accident_type_id
WHERE at.category = 'wypadki ogółem' AND a.year BETWEEN 2014 AND 2023
GROUP BY r.region_id, r.name, r.type, a.year
ORDER BY r.region_id, a.year;