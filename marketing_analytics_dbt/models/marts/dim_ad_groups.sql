SELECT
    ad_group_id,
    ad_group_name,

    campaign_id,
    campaign_name,

    channel_id,
    channel_name,

    target_audience,
    status AS ad_group_status

FROM {{ ref('int_mc_ad_groups') }}