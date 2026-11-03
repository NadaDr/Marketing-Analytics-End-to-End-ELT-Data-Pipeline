
WITH source_data AS (

    SELECT *
    FROM {{ source('marketing_campaigns', 'daily_performance') }}

),

cleaned AS (

    SELECT
        performance_id AS performance_id,

        ad_group_id AS ad_group_id,

        TRY_TO_DATE(activity_date) AS activity_date,

        impressions AS impressions,

        clicks AS clicks,

        TRY_TO_DECIMAL(spend, 12, 2) AS spend,

        conversions AS conversions,

        TRY_TO_DECIMAL(conversion_value, 12, 2) AS conversion_value

    FROM source_data

)

SELECT *
FROM cleaned
