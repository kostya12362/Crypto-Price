CREATE EXTENSION IF NOT EXISTS intarray;

CREATE UNIQUE INDEX IF NOT EXISTS idx_cryptocurrency ON cryptocurrency  (name, symbol, slug, market_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_contract ON contract (contract_address, network_name, market_id);

-- GOOD INDEX
CREATE INDEX IF NOT EXISTS idx_contracts_id ON contract USING btree (cryptocurrency_id, cryptocurrency_id DESC);
-- GOOD INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_marge_id ON merge_cryptocurrency (from_cryptocurrency_id, to_cryptocurrency_id);
-- GOOD INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_merge_cryptocurrency_sort_unique ON merge_cryptocurrency (sort(array[from_cryptocurrency_id, to_cryptocurrency_id]));
-- GOOD INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_price_unique ON history_price(date_time, cryptocurrency_id, price, market_id);
-- GOOD INDEX
CREATE INDEX IF NOT EXISTS idx_price_order ON history_price(cryptocurrency_id, date_time DESC);
