WITH ad_groups AS (

    SELECT *
    FROM {{ ref('stg_mc_ad_groups') }}

),

campaigns AS (

    SELECT *
    FROM {{ ref('int_mc_campaigns') }}

)

SELECT
    ag.ad_group_id,
    ag.ad_group_name,

    ag.campaign_id,
    ca.campaign_name,

    ca.channel_id,
    ca.channel_name,
    ca.medium,
    ca.is_paid,

    ca.objective,
    ca.budget,

    ag.target_audience,
    ag.status

FROM ad_groups ag

LEFT JOIN campaigns ca
    ON ag.campaign_id = ca.campaign_id