SELECT
    channel_id,
    channel_name,
    medium,
    is_paid
FROM {{ ref('stg_mc_channels') }}