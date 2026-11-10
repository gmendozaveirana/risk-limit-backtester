"""Convert Binance spot 1h klines (data.binance.vision) to the CSV read by the page.

Input : CSV with columns open_time, open, high, low, close, volume
        (open_time in ms; Binance switched spot files to microseconds from 2025).
Output: data/BTCUSDT_H1.csv, tab-separated, MT5-style header, times in UTC.
"""
import sys
import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT_1h_binance.csv"
df = pd.read_csv(src)
t = df["open_time"].astype("int64")
t = t.where(t < 10**14, t // 1000)          # microseconds -> milliseconds
ts = pd.to_datetime(t, unit="ms", utc=True)
out = pd.DataFrame({
    "<DATE>": ts.dt.strftime("%Y.%m.%d"),
    "<TIME>": ts.dt.strftime("%H:%M"),
    "<OPEN>": df["open"], "<HIGH>": df["high"], "<LOW>": df["low"], "<CLOSE>": df["close"],
    "<TICKVOL>": df["volume"].round(3),
}).drop_duplicates(subset=["<DATE>", "<TIME>"])
out.to_csv("data/BTCUSDT_H1.csv", sep="\t", index=False)
print(len(out), "bars", out["<DATE>"].iloc[0], "->", out["<DATE>"].iloc[-1])
