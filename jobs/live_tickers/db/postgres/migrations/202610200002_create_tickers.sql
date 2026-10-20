-- migrate:up

CREATE TABLE tickers (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  exchange_id TEXT NOT NULL,
  symbol TEXT NOT NULL,
  bid NUMERIC,
  ask NUMERIC,
  received_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- migrate:down

DROP TABLE tickers;

