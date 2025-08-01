CREATE TABLE IF NOT EXISTS conversion_rates (
    conversion_date DATE,
    currency_code VARCHAR(3),
    conversion_rate DECIMAL(50, 4),
    PRIMARY KEY (conversion_date, currency_code)
);

CREATE INDEX IF NOT EXISTS idx_currency_timestamp ON conversion_rates(currency_code, conversion_date);