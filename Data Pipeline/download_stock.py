import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

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
        start="2019-01-01",
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

engine = create_engine(
    "mysql+pymysql://root:root@localhost/Stock_market_analysis"
)

df.to_sql(
    "stock_prices",
    engine,
    if_exists="replace",
    index=False
)
print("Pipeline completed successfully")
