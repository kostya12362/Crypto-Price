-- ==================================================================================================
-- Trigger check other cryptocurrency from different market and add to table 'merge_cryptocurrency'

CREATE EXTENSION IF NOT EXISTS citext;

DROP FUNCTION IF EXISTS merge_cryptocurrency_trigger_function() cascade;
CREATE OR REPLACE FUNCTION merge_cryptocurrency_trigger_function() RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$func$
DECLARE
    rows_processed integer;
    item           record;
BEGIN
    FOR item IN (select cr.id,
                        cr.name,
                        cr.symbol,
                        cr.market_id,
                        cr.website::citext[],
                        cr.community::citext[],
                        cr.explorers::citext[]
                 from cryptocurrency as cr
                 where cr.market_id != new.market_id
                   and ((new.website::citext[] && cr.website::citext[] and
                         new.community::citext[] && cr.community::citext[]) or
                        (new.explorers::citext[] && cr.explorers::citext[]) or
                        (cr.symbol = new.symbol and cr.name = new.name)
                     )
    )
        LOOP
            raise notice '%', item.name;
            PERFORM unnest(new.community::citext[] || item.community::citext[] || new.website::citext[] ||
                        item.website::citext[] || new.explorers::citext[] || item.explorers::citext[]) as cc
            group by cc
            having count(*) > 1;
            get diagnostics rows_processed = row_count;
            raise notice 'count % DETECT item %, %, %, % || BASE %, %, %, % ', rows_processed, item.id, item.symbol,
                                            item.name, item.market_id, new.id, new.symbol, new.name, new.market_id;
            if item.symbol = new.symbol then
                if item.market_id < new.market_id THEN
                    INSERT INTO merge_cryptocurrency (from_cryptocurrency_id, to_cryptocurrency_id)
                    VALUES (item.id, new.id)
                    on conflict do nothing;
                ELSE
                    INSERT INTO merge_cryptocurrency (from_cryptocurrency_id, to_cryptocurrency_id)
                    VALUES (new.id, item.id)
                    on conflict do nothing;
                END if;
            END IF;
        END LOOP;
    RETURN new;
END;
$func$;

DROP TRIGGER IF EXISTS merge_cryptocurrency_trigger
    ON "cryptocurrency";
CREATE TRIGGER merge_cryptocurrency_trigger
    AFTER INSERT OR UPDATE
    ON "cryptocurrency"
    FOR EACH ROW
EXECUTE FUNCTION merge_cryptocurrency_trigger_function();


-- ==================================================================================================
-- ////////////////////////////////////
-- ==================================================================================================


DROP FUNCTION IF EXISTS merge_cryptocurrency_by_contract_trigger_function() cascade;
CREATE OR REPLACE FUNCTION merge_cryptocurrency_by_contract_trigger_function() RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$func$
DECLARE
    item record;
    _rec record;
BEGIN
    FOR item IN (select *
                 from contract as c
                 where c.contract_address::citext = new.contract_address::citext
                   and c.market_id != new.market_id)
        LOOP
            if new.network_name is null and item.network_name is not null and
               new.chain_id::int = item.chain_id::int THEN
                new.network_name := item.network_name;
            end if;
            if new.decimals is null and item.decimals is not null and new.network_name = item.network_name THEN
                new.decimals := item.decimals;
            end if;
            if new.chain_id is null and item.chain_id is not null and new.network_name = item.network_name THEN
                new.chain_id := item.chain_id;
            end if;
            if new.cryptocurrency_id is null and item.cryptocurrency_id is not null and
               ((item.chain_id = new.chain_id and new.chain_id is not null) or (item.network_name = new.network_name and item.network_name is not null)) THEN
                new.cryptocurrency_id := item.cryptocurrency_id;
            end if;
            if new.cryptocurrency_id is not null and item.cryptocurrency_id is not null THEN
                if item.market_id < new.market_id THEN
                    INSERT INTO merge_cryptocurrency (from_cryptocurrency_id, to_cryptocurrency_id)
                    VALUES (item.cryptocurrency_id, new.cryptocurrency_id)
                    on conflict do nothing;
                ELSE
                    INSERT INTO merge_cryptocurrency (from_cryptocurrency_id, to_cryptocurrency_id)
                    VALUES (new.cryptocurrency_id, item.cryptocurrency_id)
                    on conflict do nothing;
                end if;
            end if;
        END LOOP;
    raise notice '%, ===========', new.network_name;
    if new.network_name is null and new.network_logo_url is not null THEN
        if new.contract_address like '%-%' THEN
            select *
            INTO _rec
            from contract as c1
            where c1.network_name is not null
              and c1.network_logo_url = new.network_logo_url
              and c1.contract_address like '%-%';
            new.network_name := _rec.network_name;
        else
            select *
            INTO _rec
            from contract as c1
            where c1.network_name is not null
              and c1.network_logo_url = new.network_logo_url;
            new.network_name := _rec.network_name;
            raise notice '%, %, ===========', new.network_name, _rec.network_name;
        end if;
    end if;
    raise notice '%', new.network_name;
    RETURN new;
END
$func$;

-- ==================================================================================================
-- ////////////////////////////////////
-- ==================================================================================================


DROP FUNCTION IF EXISTS price_function_trigger() cascade;
CREATE OR REPLACE FUNCTION price_function_trigger() RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$func$
DECLARE
    item           record;
BEGIN
    SELECT p.price, p.date_time, p.cryptocurrency_id INTO item FROM history_price as p WHERE p.cryptocurrency_id = new.cryptocurrency_id order by p.date_time desc limit 1;
    IF item.price != new.price or item.date_time is null THEN
        raise notice '%, %', item.price, new.price;
        RETURN new;
    ELSE
        new.date_time := item.date_time;
        RETURN new;
    END IF;
END;
$func$;

DROP TRIGGER IF EXISTS price_insert_trigger ON "history_price";
CREATE TRIGGER price_insert_trigger
    BEFORE INSERT ON "history_price"
    FOR EACH ROW
EXECUTE FUNCTION price_function_trigger();