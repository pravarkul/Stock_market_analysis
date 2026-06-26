import pandas as pd

df=pd.read_csv(r"D:\working datasets\Realtime Stock Market Analysis\data\master_data.csv")
df["Date"] = pd.to_datetime(
    df["Date"])
df["Price Change"] = (df.groupby("Ticker")["Close"]).diff().round(2)
df["Daily Return"]=(df.groupby("Ticker")["Close"].pct_change() * 100).round(2)
df["MA20"]=(df.groupby("Ticker")["Close"].transform(lambda x:x.rolling(window=20).mean()))
df["MA50"]=(df.groupby("Ticker")["Close"].transform(lambda x:x.rolling(window=50).mean()))
df["Volatility"]=(df.groupby("Ticker")["Daily Return"].transform(lambda x:x.rolling(window=20).std()))
df["Year"]=df["Date"].dt.year
df["Month"]=df["Date"].dt.month


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
    "month"
]
delta = df.groupby("ticker")["close_price"].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.groupby(df["ticker"]).rolling(14).mean().reset_index(level=0, drop=True)
avg_loss = loss.groupby(df["ticker"]).rolling(14).mean().reset_index(level=0, drop=True)

rs = avg_gain / avg_loss

df["rsi"] = 100 - (100 / (1 + rs))
df.to_csv(
    r"D:\working datasets\Realtime Stock Market Analysis\data\master_data_transformed.csv",
    index=False
)
# print(df.head())
# print(df.columns)
# print(df.shape)
