
WITH source_data AS (

    SELECT *
    FROM {{ source('marketing_campaigns', 'channels') }}

),

cleaned AS (

    SELECT
        channel_id AS channel_id,

        NULLIF(TRIM(channel_name), '') AS channel_name,

        LOWER(NULLIF(TRIM(medium), '')) AS medium,

        is_paid

    FROM source_data

)

SELECT *
FROM cleaned
