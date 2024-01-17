import pandas as pd

stock_prices_path = 'data/merged_data.csv'
stock_data = pd.read_csv(stock_prices_path)
stock_data.set_index('trade_time', inplace=True)

# 计算收益率
stock_returns = stock_data.pct_change()
stock_returns = stock_returns.iloc[1:]  # 去掉第一行
stock_returns.to_csv('data/stock_returns.csv', index=True)