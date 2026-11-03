WITH source_data AS (

    SELECT *
    FROM {{ source('marketing_campaigns', 'conversions') }}

),

cleaned AS (

    SELECT
        conversion_id,
        ad_group_id,
        first_touch_channel_id,
        last_touch_channel_id,
        converted_at,
        revenue,
        touch_count,
        LOWER(NULLIF(TRIM(device), '')) AS device

    FROM source_data

)

SELECT *
FROM cleaned