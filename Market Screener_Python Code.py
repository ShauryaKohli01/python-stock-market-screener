import pandas as pd
import numpy as np
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# This line is only valid in Jupyter Notebook. Remove or comment it out if running as a .py file.
# %matplotlib inline  

# Dow30 tickers
tickers = [
    "AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
    "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"
]

# Download historical stock data
start_date = '2025-02-01'
end_date = '2025-07-27'  # or use dt.datetime.today().strftime('%Y-%m-%d')

data = yf.download(
    tickers,
    start=start_date,
    end=end_date,
    group_by='ticker',
    auto_adjust=True,
    threads=True
)

# Scoring Functions
def ma50_score(df):
    ma50_series = ta.SMA(df['Close'], timeperiod=50)
    ma200_series = ta.SMA(df['Close'], timeperiod=200)

    if len(ma50_series.dropna()) < 6 or len(ma200_series.dropna()) == 0:
        return 0  # Not enough data

    ma50 = ma50_series.iloc[-1]
    ma50_5ago = ma50_series.iloc[-5]
    ma200 = ma200_series.iloc[-1]
    close = df['Close'].iloc[-1]

    dist = (close - ma50) / ma50
    dist_score = np.clip(dist, -1, 1)

    slope = (ma50 - ma50_5ago) / ma50
    slope_score = np.clip(slope * 5, -1, 1)

    regime = 1 if ma50 > ma200 else -1

    score = 0.5 * dist_score + 0.3 * slope_score + 0.2 * regime
    return np.clip(score, -1, 1)

def rsi_score_momentum(df, rsi_period=14, lookback=20):
    rsi_series = ta.RSI(df['Close'], timeperiod=rsi_period)
    rsi_change = rsi_series.diff()

    if len(rsi_change.dropna()) < lookback:
        return 0

    change = rsi_change.iloc[-1]
    stdev = rsi_change.rolling(lookback).std().iloc[-1]

    if pd.isna(stdev) or stdev == 0:
        return 0

    score = change / (2 * stdev)
    return np.clip(score, -1, 1)

def vol_score(df, lookback_vol=20):
    if len(df) < lookback_vol + 2:
        return 0

    avg_vol = df['Volume'].rolling(window=lookback_vol).mean().iloc[-1]
    curr_vol = df['Volume'].iloc[-1]
    ratio = curr_vol / avg_vol if avg_vol != 0 else 0
    ratio = min(ratio, 1.0)

    price_diff = df['Close'].iloc[-1] - df['Close'].iloc[-2]
    trend_sign = np.sign(price_diff)

    return ratio * trend_sign

# Main loop
results = []

for ticker in tickers:
    try:
        df_ticker = data[ticker][['Close', 'Volume']].dropna()

        result = {
            'Ticker': ticker,
            'ma50_score': ma50_score(df_ticker),
            'rsi_score': rsi_score_momentum(df_ticker),
            'vol_score': vol_score(df_ticker),
        }

        result['final_score'] = np.mean([result['ma50_score'], result['rsi_score'], result['vol_score']])
        results.append(result)

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        continue

scanner_df = pd.DataFrame(results)
scanner_df = scanner_df.sort_values('final_score', ascending=False).reset_index(drop=True)

# Display top results
print(scanner_df.head())
scanner_df

# Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x='Ticker', y='final_score', data=scanner_df, palette='coolwarm')
plt.title('Final Score per Ticker')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Heatmap
values = scanner_df['final_score'].values
n = len(values)
rows = int(np.ceil(np.sqrt(n)))
cols = int(np.ceil(n / rows))

grid = np.full((rows, cols), np.nan)
labels = np.full((rows, cols), "", dtype=object)

for i, val in enumerate(values):
    r = i // cols
    c = i % cols
    grid[r, c] = val
    labels[r, c] = scanner_df['Ticker'].iloc[i]

plt.figure(figsize=(10, 6))
sns.heatmap(grid,
            annot=labels,
            fmt='',
            center=0,
            cmap='RdYlGn',
            cbar_kws={'label': 'Final Score'},
            linewidths=0.5,
            linecolor='gray')
plt.title('Stock Scanner Heatmap')
plt.yticks([])
plt.xticks([])
plt.show()

# Example data preview
print(data['MSFT'].tail())
