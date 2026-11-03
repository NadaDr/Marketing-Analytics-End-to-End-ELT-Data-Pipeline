WITH conversions AS (

    SELECT *
    FROM {{ ref('stg_mc_conversions') }}

),

ad_groups AS (

    SELECT *
    FROM {{ ref('int_mc_ad_groups') }}

),

first_touch_channels AS (

    SELECT *
    FROM {{ ref('stg_mc_channels') }}

),

last_touch_channels AS (

    SELECT *
    FROM {{ ref('stg_mc_channels') }}

)

SELECT
    c.conversion_id,
    c.converted_at,

    c.ad_group_id,
    ag.ad_group_name,
    ag.campaign_id,
    ag.campaign_name,

    c.first_touch_channel_id,
    ft.channel_name AS first_touch_channel,

    c.last_touch_channel_id,
    lt.channel_name AS last_touch_channel,

    c.device,
    c.touch_count,
    c.revenue

FROM conversions c

LEFT JOIN ad_groups ag
    ON c.ad_group_id = ag.ad_group_id

LEFT JOIN first_touch_channels ft
    ON c.first_touch_channel_id = ft.channel_id

LEFT JOIN last_touch_channels lt
    ON c.last_touch_channel_id = lt.channel_id