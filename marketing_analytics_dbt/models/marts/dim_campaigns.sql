SELECT
    campaign_id,
    campaign_name,

    channel_id,
    channel_name,

    objective,
    started_on,
    ended_on,
    budget

FROM {{ ref('int_mc_campaigns') }}
