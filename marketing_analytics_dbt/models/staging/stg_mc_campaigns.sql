
WITH source_data AS (

    SELECT *
    FROM {{ source('marketing_campaigns', 'campaigns') }}

),

cleaned AS (

    SELECT
        campaign_id AS campaign_id,

        NULLIF(TRIM(campaign_name), '') AS campaign_name,

        channel_id AS channel_id,

        LOWER(NULLIF(TRIM(objective), '')) AS objective,

        TRY_TO_DATE(started_on) AS started_on,

        TRY_TO_DATE(ended_on) AS ended_on,

        TRY_TO_DECIMAL(budget, 12, 2) AS budget

    FROM source_data

)

SELECT *
FROM cleaned