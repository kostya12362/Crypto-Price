-- ==================================================================================================
-- ////////////////////////////////////
-- ==================================================================================================
-- marge table filter and concat

DROP FUNCTION IF EXISTS  marge_clean();
create or replace function marge_clean()
    returns TABLE
            (
                f integer,
                t integer
            )
    language sql
as
$$
with mrcr as (select (CASE
                          WHEN
                              c1.market_id < c2.market_id and mc.from_cryptocurrency_id is not null THEN c1.id
                          ELSE
                              c2.id
    END)::int4                      AS f,
                     (CASE
                          WHEN
                              c1.market_id > c2.market_id THEN c1.id
                          ELSE
                              c2.id
                         END)::int4 AS t
              from merge_cryptocurrency as mc
                       inner join cryptocurrency c1 on c1.id = mc.from_cryptocurrency_id
                       inner join cryptocurrency c2 on c2.id = mc.to_cryptocurrency_id

              union all
              select cr3.id::int4 as f, NULL::int4 as t
              from cryptocurrency as cr3
              where cr3.id not in
                    (select unnest(array_remove(array_agg(to_cryptocurrency_id) || array_agg(from_cryptocurrency_id),
                                                null))
                     from merge_cryptocurrency)
)
select *
from mrcr
$$;

-- ==================================================================================================
-- ////////////////////////////////////
-- ==================================================================================================
-- filter contracts by name contract_address, symbol, ignore_market_ids

DROP FUNCTION IF EXISTS get_contracts();
create or replace function get_contracts(
    _name citext default null,
    _contract_address citext default null,
    _symbol citext default null,
    _ignore_market_ids int[] default null
    )
    returns TABLE
            (
                id int,
                name               varchar,
                symbol             varchar,
                "contractAddress"  citext,
                "decimals"         int,
                "blockExplorerURL" text,
                "rpcNodeURL"       text,
                "networkName"      citext,
                "networkLogoURL"   varchar,
                "chainId"          int,
                "logoURL"          text,
                "bridge"           bool,
                "cryptocurrencyId" int,
                "markets" jsonb
            )
    language sql
as
$$
SELECT
       (array_agg(c.id))[1]                 as "id",
       (array_agg(c.name))[1]               as "name",
       (array_agg(c.symbol))[1]             as "symbol",
       regexp_replace(c.contract_address, '( )', '')::citext           as "contractAddress",
       (array_agg(c.decimals))[1]           as "decimals",
       (array_agg(c.block_explorer_url))[1] as "blockExplorerURL",
       (array_agg(distinct c.rpc_node_url)
            filter (where c.rpc_node_url is not null and c.rpc_node_url !=array[]::text[]))[1]   as "rpcNodeURL",
       c.network_name::citext               as "networkName",
       (array_agg(c.network_logo_url))[1]   as "networkLogoURL",
       (array_agg(c.chain_id))[1]           as "chainId",
       (array_agg(c.logo_url))[1]           as "logoURL",
       (array_agg(c.is_bridge))[1]          as "bridge",
       (array_agg(distinct c.cryptocurrency_id))[1]  as "cryptocurrencyId",
       jsonb_agg(distinct jsonb_build_object(
               'marketId', m1.id, 'marketName', m1.name, 'marketLogoURL', m1.logo, 'marketSiteURL', m1.site
           )
        )                                as "markets"
FROM contract as c
         LEFT JOIN market as m1 on m1.id = c.market_id
WHERE (c.name::citext like coalesce(_name, '%') AND
      regexp_replace(c.contract_address, '( )', '')::citext like coalesce(_contract_address, '%')) AND
      (c.symbol::citext like coalesce(_symbol, '%')) and c.network_name IS NOT NULL and
      not (c.market_id = any(coalesce(_ignore_market_ids, '{}'::int[])))
GROUP BY "contractAddress", "networkName"
ORDER BY "cryptocurrencyId"
$$;


-- ==================================================================================================
-- ////////////////////////////////////
-- ==================================================================================================
-- filter contracts by name contract_address, symbol, ignore_market_ids

select mr.f                                                       as "id",
       (array_agg(cr1.name))[1]                                   as "name",
       (array_agg(cr1.market_id))[1]                              as "marketId",
       (array_agg(cr1.cm_id))[1]                                  as "cmId",
       (array_agg(cr1.symbol))[1]                                 as "symbol",
       (array_agg(cr1.slug))[1]                                   as "slug",
       (array_agg(cr1.date_added))[1]                             as "dateAdded",
       (array_agg(cr1.logo_url))[1]                               as "logoURL",
       (array_agg(cr1.rank))[1]                                   as "rank",
       jsonb_build_object(
               'audit', jsonb_agg(distinct cr1.audit_infos) -> 0,
               'rank', jsonb_agg(distinct cr1.rank) -> 0,
               'tags', jsonb_agg(distinct cr1.tags) -> 0,
               'website', jsonb_agg(distinct cr1.website) -> 0,
               'community', jsonb_agg(distinct cr1.community) -> 0,
               'explorers', jsonb_agg(distinct cr1.explorers) -> 0,
               'source_code', jsonb_agg(distinct cr1.source_code) -> 0
           )                                                      as meta,
       nullif(array_remove(array_agg(distinct mr.t), null), '{}') as groups,
       (CASE
            WHEN (array_agg(con."contractAddress"))[1] is not null THEN
                jsonb_agg(
                        distinct jsonb_build_object(
                        'id', con.id,
                        'name', con.name,
                        'symbol', con.symbol,
                        'contractAddress', con."contractAddress",
                        'networkName', con."networkName",
                        'networkLogoURL', con."networkLogoURL",
                        'chainId', con."chainId",
                        'decimals', con.decimals,
                        'rpcNodeURL', nullif(con."rpcNodeURL", '{}'),
                        'blockExplorerURL', con."blockExplorerURL",
                        'markets', con.markets
                    )
                    )
            ELSE
                '[]'::jsonb
           END
           )                                                      as "contracts"
from marge_clean() mr
         left join (select * from get_contracts() where name is not null and "contractAddress" is not null) con
                   on mr.f = con."cryptocurrencyId" or
                      mr.t = con."cryptocurrencyId"
         left join cryptocurrency as cr1 on mr.f = cr1.id or mr.f = cr1.id and cr1.id != mr.f
where cr1.symbol::citext = 'SOY'
group by mr.f
order by (array_agg(cr1.market_id))[1], (array_agg(cr1.rank))[1] nulls last,
         array_length(nullif(array_remove(array_agg(distinct mr.t), null), '{}'), 1)
limit 5;