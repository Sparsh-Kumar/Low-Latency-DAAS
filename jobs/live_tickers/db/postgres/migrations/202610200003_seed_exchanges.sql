-- migrate:up

INSERT INTO exchanges (exchange_id, enabled)
VALUES
  ('binance', TRUE),
  ('bybit', TRUE)
ON CONFLICT (exchange_id)
DO UPDATE SET enabled = EXCLUDED.enabled;

-- migrate:down

DELETE FROM exchanges
WHERE exchange_id IN ('binance', 'bybit');
