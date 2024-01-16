import akshare as ak
import json
import os

# 读取股票代码
path_to_json_file = 'ticker.json'
with open(path_to_json_file, 'r') as json_file:
    tickers = json.load(json_file)

# 检查并获取后复权因子
for ticker in tickers:
    filename = f"{ticker}.csv"

    # 检查文件是否存在
    if not os.path.exists("backward_adjust_factor/" + filename):
        try:
            # 尝试调用 API 获取数据
            df = ak.stock_zh_a_daily(symbol=ticker, adjust="hfq-factor")
            # 保存数据到 CSV 文件
            df.to_csv("backward_adjust_factor/" + filename, index=False)
            print(f"{ticker} data saved to {filename}")
        except Exception as e:
            # 打印错误信息，并继续处理下一个 ticker
            print(f"Error retrieving data for {ticker}: {e}")
    else:
        print(f"File {filename} already exists. Skipping.")