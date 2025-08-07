SELECT
    currency_code,
    MAX(conversion_date) AS latest_date
FROM
    conversion_rates
GROUP BY
    currency_code;