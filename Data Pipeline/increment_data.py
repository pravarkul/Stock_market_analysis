import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine, text
from datetime import timedelta
import sys
engine = create_engine(
    "mysql+pymysql://root:root@localhost/Stock_market_analysis"
)
latest_date = pd.read_sql(
    """
    SELECT MAX(date) AS latest_date
    FROM stock_prices
    """,
    engine
)

latest_date = latest_date.iloc[0]["latest_date"]

print("Latest SQL date:", latest_date)

download_start = latest_date - timedelta(days=60)

print(download_start)

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "^NSEI",
    "ICICIBANK.NS",
    "SBIN.NS",
    "ITC.NS",
    "HINDUNILVR.NS",
    "BHARTIARTL.NS",
    "LT.NS",
    "MARUTI.NS",
    "ASIANPAINT.NS",
    "CIPLA.NS",
    "AXISBANK.NS",
    "KOTAKBANK.NS",
    "BAJFINANCE.NS",
    "BAJAJFINSV.NS",
    "ONGC.NS",
    "POWERGRID.NS",
    "NTPC.NS",
    "M&M.NS",
    "SUNPHARMA.NS",
    "DRREDDY.NS",
    "NESTLEIND.NS",
    "TATACONSUM.NS",
    "TATASTEEL.NS",
    "HINDALCO.NS",
    "JSWSTEEL.NS",
    "ULTRACEMCO.NS",
    "SBILIFE.NS",
    "HDFCLIFE.NS",
    "ADANIPORTS.NS"
]

all_data = []

for stock in stocks:

    df = yf.download(
        stock,
        start=download_start,
        auto_adjust=True
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns.name = None

    df = df.reset_index()

    df["Ticker"] = stock

    all_data.append(df)

master_df = pd.concat(
    all_data,
    ignore_index=True
)
df = master_df.copy()
df = df.sort_values(
    ["Ticker", "Date"]
).reset_index(drop=True)
df["Date"] = pd.to_datetime(df["Date"])

df["Price Change"] = (
    df.groupby("Ticker")["Close"]
      .diff()
      .round(2)
)

df["Daily Return"] = (
    df.groupby("Ticker")["Close"]
      .pct_change() * 100
).round(2)

df["MA20"] = (
    df.groupby("Ticker")["Close"]
      .transform(lambda x: x.rolling(20).mean())
)

df["MA50"] = (
    df.groupby("Ticker")["Close"]
      .transform(lambda x: x.rolling(50).mean())
)

df["Volatility"] = (
    df.groupby("Ticker")["Daily Return"]
      .transform(lambda x: x.rolling(20).std())
)

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

delta = df.groupby("Ticker")["Close"].diff()

gain = delta.where(delta > 0, 0)

loss = -delta.where(delta < 0, 0)

avg_gain = (
    gain.groupby(df["Ticker"])
    .rolling(14)
    .mean()
    .reset_index(level=0, drop=True)
)

avg_loss = (
    loss.groupby(df["Ticker"])
    .rolling(14)
    .mean()
    .reset_index(level=0, drop=True)
)

rs = avg_gain / avg_loss

df["RSI"] = 100 - (100 / (1 + rs))

df.columns = [
    "date",
    "close_price",
    "high_price",
    "low_price",
    "open_price",
    "volume",
    "ticker",
    "price_change",
    "daily_return",
    "ma20",
    "ma50",
    "volatility",
    "year",
    "month",
    "rsi"
]
latest_date = pd.to_datetime(latest_date).normalize()
df["date"] = pd.to_datetime(df["date"]).dt.normalize()
df_new = df[df["date"] > latest_date]
df_new = df_new.drop_duplicates(
    subset=["ticker", "date"]
)
print("Rows to append:", len(df_new))
print(df_new[["ticker", "date"]].head())
if df_new.empty:
    print("No new records found")
    sys.exit()
try:
    df_new.to_sql(
        "stock_prices",
        engine,
        if_exists="append",
        index=False
    )

    print(f"{len(df_new)} rows inserted successfully")

except Exception as e:
    print("Insert failed")
    print(e)
print("Pipeline completed successfully")