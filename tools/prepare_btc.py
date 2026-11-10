"""Convert Binance 1h OHLCV bars to the CSV read by the page.

Input : CSV with a time column (open_time or timestamp, in ms or microseconds)
        and open, high, low, close, volume.
Output: data/BTCUSD_H1.csv, tab-separated, MT5-style header, times in UTC.
"""
import sys
import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "btc_hourly.csv"
df = pd.read_csv(src)
t = df["open_time" if "open_time" in df.columns else "timestamp"].astype("int64")
t = t.where(t < 10**14, t // 1000)          # microseconds -> milliseconds
ts = pd.to_datetime(t, unit="ms", utc=True)
out = pd.DataFrame({
    "<DATE>": ts.dt.strftime("%Y.%m.%d"),
    "<TIME>": ts.dt.strftime("%H:%M"),
    "<OPEN>": df["open"], "<HIGH>": df["high"], "<LOW>": df["low"], "<CLOSE>": df["close"],
    "<TICKVOL>": df["volume"].round(3),
}).drop_duplicates(subset=["<DATE>", "<TIME>"])
out.to_csv("data/BTCUSD_H1.csv", sep="\t", index=False)
print(len(out), "bars", out["<DATE>"].iloc[0], "->", out["<DATE>"].iloc[-1])
