-- stg_weather.sql
SELECT
    timestamp,
    temperature AS temp_celsius,
    ROUND((temperature * 9/5) + 32, 2) AS temp_fahrenheit,
    humidity,
    CASE 
        WHEN humidity >= 80 THEN 'High'
        WHEN humidity BETWEEN 40 AND 79 THEN 'Moderate'
        ELSE 'Low'
    END AS humidity_category
FROM MY_FIRST_PIPELINE.RAW.RAW_WEATHER
WHERE timestamp IS NOT NULL