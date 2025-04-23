CREATE KEYSPACE IF NOT EXISTS financial_data WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE financial_data;
CREATE TABLE IF NOT EXISTS trades (
    symbol text,
    price double,
    volume double,  -- Changed to double for fractional volumes
    timestamp timestamp,
    PRIMARY KEY (symbol, timestamp)
);
CREATE TABLE IF NOT EXISTS trade_aggregates (
    symbol text,
    window_start timestamp,
    window_end timestamp,
    avg_price double,
    total_volume double,
    PRIMARY KEY (symbol, window_end)
);
