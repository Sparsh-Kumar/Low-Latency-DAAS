-- migrate:up

CREATE TABLE exchanges (
  exchange_id TEXT PRIMARY KEY,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- migrate:down

DROP TABLE exchanges;
