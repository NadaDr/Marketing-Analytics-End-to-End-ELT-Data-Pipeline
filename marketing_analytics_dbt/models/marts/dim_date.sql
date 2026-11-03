
WITH date_bounds AS (

    -- Dates from daily performance
    SELECT
        MIN(activity_date) AS min_date,
        MAX(activity_date) AS max_date
    FROM {{ ref('int_mc_daily_performance') }}

    UNION ALL

    -- Dates from conversion events
    SELECT
        MIN(converted_at::DATE) AS min_date,
        MAX(converted_at::DATE) AS max_date
    FROM {{ ref('int_mc_conversion_attribution') }}

),

date_range AS (

    SELECT
        MIN(min_date) AS min_date,
        MAX(max_date) AS max_date
    FROM date_bounds

),

dates AS (

    SELECT
        DATEADD(
            DAY,
            ROW_NUMBER() OVER (ORDER BY SEQ4()) - 1,
            min_date
        )::DATE AS date_day

    FROM date_range,
         TABLE(GENERATOR(ROWCOUNT => 10000))

    QUALIFY date_day <= max_date

)

SELECT
    TO_NUMBER(TO_CHAR(date_day, 'YYYYMMDD')) AS date_key,
    date_day,
    YEAR(date_day) AS year,
    QUARTER(date_day) AS quarter,
    MONTH(date_day) AS month,
    MONTHNAME(date_day) AS month_name,
    DAY(date_day) AS day_of_month,
    DAYOFWEEKISO(date_day) AS day_of_week,
    DAYNAME(date_day) AS day_name,
    WEEKISO(date_day) AS week_of_year

FROM dates
