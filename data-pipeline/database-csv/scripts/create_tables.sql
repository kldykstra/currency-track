-- Create a table to store conversion rates with 3 columns
-- conversion_date, currency_code, conversion_rate
CREATE TABLE IF NOT EXISTS conversion_rates (
    conversion_date DATE,
    currency_code VARCHAR(3),
    conversion_rate DECIMAL(10, 4),
    PRIMARY KEY (conversion_date, currency_code)
);