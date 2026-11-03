WITH daily AS (

    SELECT *
    FROM {{ ref('stg_mc_daily_performance') }}

),

ad_groups AS (

    SELECT *
    FROM {{ ref('int_mc_ad_groups') }}

)

SELECT
    d.performance_id,
    d.activity_date,

    d.ad_group_id,
    ag.ad_group_name,

    ag.campaign_id,
    ag.campaign_name,

    ag.channel_id,
    ag.channel_name,
    ag.medium,
    ag.is_paid,

    ag.target_audience,
    ag.status AS ad_group_status,

    d.impressions,
    d.clicks,
    d.spend,
    d.conversions,
    d.conversion_value,

    d.clicks * 1.0 / NULLIF(d.impressions, 0) AS daily_ctr

FROM daily d

LEFT JOIN ad_groups ag
    ON d.ad_group_id = ag.ad_group_id