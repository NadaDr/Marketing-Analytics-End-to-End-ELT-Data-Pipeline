
WITH source_data AS (

    SELECT *
    FROM {{ source('marketing_campaigns', 'ad_groups') }}

),

cleaned AS (

    SELECT
        ad_group_id AS ad_group_id,

        campaign_id AS campaign_id,

        NULLIF(TRIM(ad_group_name), '') AS ad_group_name,

        LOWER(NULLIF(TRIM(target_audience), '')) AS target_audience,

        LOWER(NULLIF(TRIM(status), '')) AS status

    FROM source_data

)

SELECT *
FROM cleaned
