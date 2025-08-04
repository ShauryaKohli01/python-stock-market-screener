# Market Screener in Python

A powerful stock market screener built in Python using `yfinance` for real-time data, `TA-Lib` for technical analysis indicators, and pandas for data manipulation.  
Easily customizable to backtest strategies, filter stocks, and visualize trends.


A market scanner is used by traders, especially those traders that have universe of stocks in their portfolio. For example, let's say you are a Trader and is looking for an opportunities or 
entry in suppose 500 stocks. In general, it will require a lot of human labour to analyse each and every stock. That's why you need a MARKET SCANNER to tell of which stock to focus on and buying that stock.

# Important Libraries Used


1. yfinance: Downloads historical stock data (Open, High, Low, Close, Volume) for tickers using Yahoo Finance. It gives us the base dataset we’ll apply our indicators to.

2. TA-Lib (talib): A library to calculate technical indicators like RSI, Moving Averages, Bollinger Bands, etc., essential for analyzing price action and momentum.

3. matplotlib & seaborn: Visualization libraries used to build clear and attractive bar charts and heatmaps of stock performance based on the final score.

4. numpy & pandas: Core libraries for numerical operations and dataframe handling.

# What Are Scoring Functions?


Scoring functions quantify different technical aspects of a stock and return a score between -1 (weak) and +1 (strong). These scores are averaged into a final_score that tells us how attractive a stock is for buying, based on:

1. ma50_score → trend strength

2. rsi_score → momentum

3. vol_score → volume breakout

Each scoring function uses a different technical factor, giving a comprehensive picture.

# Key Technical Indicators Explained

1. TA-Lib
TA-Lib simplifies using technical indicators. For example:
<img width="341" height="51" alt="image" src="https://github.com/user-attachments/assets/becb8034-736e-43b4-bd38-b4d81be81154" />


Calculates the 50-day Simple Moving Average (SMA), which smooths out price to identify trend direction.

2. 50-day Moving Average (MA50)
A stock trading above its MA50 typically signals upward momentum. If MA50 is also above MA200, that suggests a strong long-term uptrend (this is used in the ma50_score function).

3. RSI (Relative Strength Index)
RSI measures price momentum — values above 70 suggest overbought conditions, while below 30 suggest oversold. Here, we're scoring stocks based on how rapidly RSI is changing — faster change = higher momentum.

4. Volume Score
Higher volume often confirms price moves. If today’s volume is much higher than the 20-day average and the price is rising, that’s bullish. This is captured in vol_score.

# Visual Outputs from Code

1. Bar Chart (sns.barplot)


<img width="1190" height="591" alt="image" src="https://github.com/user-attachments/assets/a6f0887e-3a51-4a61-a2d9-0e3381c049f7" />


This shows each stock's final_score, sorted from highest to lowest. It gives a clear visual comparison of which stocks are currently scoring best based on our 3 metrics. 
The bar's height and color intensity reflect relative strength.



2. Heatmap (sns.heatmap)


<img width="842" height="558" alt="image" src="https://github.com/user-attachments/assets/58500ba3-504a-467c-a2ad-8e265856d863" />



This is a grid-style visual where each cell represents a stock's final_score with its ticker name inside. Color gradients (green → 
strong, red → weak) make it easy to spot strong vs. weak performers at a glance. It’s more compact and intuitive when you're screening many stocks.


# Conclusion:
This stock screener uses Python to analyze and rank stocks from the Dow 30 index based on key technical indicators—namely the 50-day moving average (MA50), Relative Strength Index (RSI), and volume trends—using real-time data from Yahoo Finance via yfinance. By applying scoring functions on each stock and aggregating them, it helps identify momentum, trend strength, and volume surges, allowing traders to focus on high-potential stocks.


The screener is powered by TA-Lib, a powerful library for computing indicators like moving averages and RSI with ease. The final results are visualized through a bar chart, which shows the comparative final score of each stock, and a heatmap, which provides a quick visual snapshot of how each stock performs technically.


This tool ultimately simplifies decision-making by narrowing down the large stock universe into actionable insights—ideal for traders looking for technically strong candidates without spending hours on manual chart analysis.






