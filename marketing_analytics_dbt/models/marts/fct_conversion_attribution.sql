SELECT
    conversion_id,

    TO_NUMBER(
        TO_CHAR(converted_at::DATE, 'YYYYMMDD')
    ) AS date_key,

    ad_group_id,
    campaign_id,

    first_touch_channel_id,
    last_touch_channel_id,

    device,
    touch_count,
    revenue

FROM {{ ref('int_mc_conversion_attribution') }}