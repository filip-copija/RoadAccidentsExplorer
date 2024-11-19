-- Sum of accidents by region_name and type
CREATE OR REPLACE VIEW accidents_by_region AS
SELECT
    r.name AS region_name,
    r.type AS region_type,
    a.accident_type,
    SUM(a.value) AS total_accidents
FROM
    regions r
JOIN
    accidents a ON r.region_id = a.region_id
GROUP BY
    r.name, r.type, a.accident_type;

-- Sum of accidents by year
CREATE OR REPLACE VIEW accidents_by_year AS
SELECT
    a.year,
    a.accident_type,
    SUM(a.value) AS total_accidents
FROM
    accidents a
GROUP BY
    a.year, a.accident_type
ORDER BY
    a.year;

-- TOP 10 regions base on sum of accidents
CREATE OR REPLACE VIEW top_accidents_regions AS
SELECT
    r.name AS region_name,
    SUM(a.value) AS total_accidents
FROM
    regions r
JOIN
    accidents a ON r.region_id = a.region_id
WHERE
    a.accident_type = 'wypadki ogółem' and r.name <> N'POLSKA'
GROUP BY
    r.name
ORDER BY
    total_accidents DESC
LIMIT 10;

-- DASHBOARD: accidents_summary
CREATE OR REPLACE VIEW accidents_summary AS
SELECT
    COUNT(DISTINCT r.region_id) AS total_regions,
    COUNT(DISTINCT a.accident_id) AS total_accidents_records,
    SUM(a.value) AS total_accidents
FROM
    regions r
JOIN
    accidents a ON r.region_id = a.region_id;

-- Sum of accidents per year
CREATE OR REPLACE VIEW accidents_over_time AS
SELECT year, SUM(value) AS total_accidents
    FROM accidents
    WHERE accident_type = 'wypadki ogółem'
    GROUP BY year
    ORDER BY year;
    