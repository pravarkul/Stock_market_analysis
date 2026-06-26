-- INITIALIZATION --
show databases;
create database stock_market_analysis;
use stock_market_analysis;
CREATE TABLE stock_prices (
    date DATE,
    close_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    open_price FLOAT,
    volume BIGINT,
    ticker VARCHAR(20),
    price_change FLOAT,
    daily_return FLOAT,
    ma20 FLOAT,
    ma50 FLOAT,
    volatility FLOAT,
    year INT,
    month INT
);
CREATE TABLE sector_mapping (
    ticker VARCHAR(20) PRIMARY KEY,
    sector VARCHAR(50)
);
INSERT INTO sector_mapping VALUES
('^NSEI','Index'),
('RELIANCE.NS','Energy'),
('ONGC.NS','Energy'),
('TCS.NS','Information Technology'),
('INFY.NS','Information Technology'),
('HDFCBANK.NS','Banking'),
('ICICIBANK.NS','Banking'),
('SBIN.NS','Banking'),
('AXISBANK.NS','Banking'),
('KOTAKBANK.NS','Banking'),
('BAJFINANCE.NS','Financial Services'),
('BAJAJFINSV.NS','Financial Services'),
('SBILIFE.NS','Insurance'),
('HDFCLIFE.NS','Insurance'),
('ITC.NS','FMCG'),
('HINDUNILVR.NS','FMCG'),
('NESTLEIND.NS','FMCG'),
('TATACONSUM.NS','FMCG'),
('BHARTIARTL.NS','Telecom'),
('LT.NS','Capital Goods'),
('MARUTI.NS','Automobile'),
('M&M.NS','Automobile'),
('CIPLA.NS','Pharmaceuticals'),
('SUNPHARMA.NS','Pharmaceuticals'),
('DRREDDY.NS','Pharmaceuticals'),
('ASIANPAINT.NS','Consumer Durables'),
('POWERGRID.NS','Utilities'),
('NTPC.NS','Utilities'),
('TATASTEEL.NS','Metals'),
('HINDALCO.NS','Metals'),
('JSWSTEEL.NS','Metals'),
('ULTRACEMCO.NS','Cement'),
('ADANIPORTS.NS','Infrastructure');
SELECT * from sector_mapping;

desc stock_prices;
ALTER TABLE stock_prices
MODIFY COLUMN ticker VARCHAR(20);

ALTER TABLE stock_prices
ADD CONSTRAINT unique_stock_date
UNIQUE (ticker, date);
SHOW index from stock_prices;
select count(*) from stock_prices;
-- ANALYSIS --

WITH stock_bounds AS (
    SELECT
        ticker,
        MIN(date) AS start_date,
        MAX(date) AS end_date
    FROM stock_prices
    GROUP BY ticker
)

SELECT
    s.ticker,
    ROUND(
        (
            end_price.close_price
            -
            start_price.close_price
        )
        /
        start_price.close_price
        * 100,
        2
    ) AS total_return_pct
FROM stock_bounds s
JOIN stock_prices start_price
ON start_price.ticker = s.ticker
AND start_price.date = s.start_date
JOIN stock_prices end_price
ON end_price.ticker = s.ticker
AND end_price.date = s.end_date
ORDER BY total_return_pct DESC;

SELECT ticker, ROUND(AVG(volatility),2)
AS avg_volatility
FROM stock_prices
GROUP BY ticker
ORDER BY avg_volatility DESC;

SELECT ticker, ROUND(AVG(daily_return),4)
AS avg_daily_return
FROM stock_prices
GROUP BY ticker
ORDER BY avg_daily_return DESC;

SELECT ticker, ROUND(AVG(volume),0)
AS avg_volume
FROM stock_prices
GROUP BY ticker
ORDER BY avg_volume DESC;

SELECT ticker, year, month, ROUND(AVG(daily_return),2)
AS avg_monthly_return
FROM stock_prices
GROUP BY ticker, year, month
ORDER BY year, month;

SELECT ticker, year, ROUND(AVG(daily_return),2)
AS yearly_avg_return
FROM stock_prices
GROUP BY ticker, year
ORDER BY year;

SELECT ticker, COUNT(*)
AS bullish_days
FROM stock_prices
WHERE ma20 > ma50
GROUP BY ticker
ORDER BY bullish_days DESC;

SELECT ticker, MAX(daily_return)
AS best_day
FROM stock_prices
GROUP BY ticker
ORDER BY best_day DESC;

SELECT ticker, MIN(daily_return)
AS worst_day
FROM stock_prices
GROUP BY ticker
ORDER BY worst_day;

SELECT ticker, ROUND(AVG(daily_return),3) AS avg_return,
ROUND(AVG(volatility),3) AS avg_risk
FROM stock_prices
GROUP BY ticker;

SELECT ticker, ROUND(AVG(daily_return)/AVG(volatility),4)
AS risk_adjusted_return
FROM stock_prices
GROUP BY ticker
ORDER BY risk_adjusted_return DESC;

SELECT
    ticker,
    date,
    COUNT(*) AS cnt
FROM stock_prices
GROUP BY ticker, date
HAVING COUNT(*) > 1;