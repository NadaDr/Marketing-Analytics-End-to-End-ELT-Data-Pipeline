SELECT
    performance_id,

    TO_NUMBER(TO_CHAR(activity_date, 'YYYYMMDD')) AS date_key,

    campaign_id,
    ad_group_id,
    channel_id,

    impressions,
    clicks,
    spend,
    conversions,
    conversion_value,

    daily_ctr

FROM {{ ref('int_mc_daily_performance') }}