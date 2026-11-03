WITH campaigns AS (

    SELECT *
    FROM {{ ref('stg_mc_campaigns') }}

),

channels AS (

    SELECT *
    FROM {{ ref('stg_mc_channels') }}

)

SELECT
    ca.campaign_id,
    ca.campaign_name,

    ca.channel_id,
    ch.channel_name,
    ch.medium,
    ch.is_paid,

    ca.objective,
    ca.started_on,
    ca.ended_on,
    ca.budget

FROM campaigns ca

LEFT JOIN channels ch
    ON ca.channel_id = ch.channel_id