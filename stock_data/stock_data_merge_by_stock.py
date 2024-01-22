import os
import pandas as pd
import json

# 路径设置
json_file = 'data/top_market_cap_stocks.json'
data_dir = 'data/stocks'
merged_dir = os.path.join(data_dir, 'data/merged/')
if not os.path.exists(merged_dir):
    os.makedirs(merged_dir)

# 读取股票代码列表
with open(json_file, 'r') as f:
    tickers = json.load(f)

# 为每个股票代码合并数据
for ticker in tickers:
    all_data = []  # 存储单个股票的所有数据
    # 遍历每个年份的文件夹
    for year in os.listdir(data_dir):
        year_dir = os.path.join(data_dir, year)
        if os.path.isdir(year_dir):  # 确保是目录
            # 假设后缀可能是.SZ或.SH，尝试两种可能性
            for suffix in ['.SZ', '.SH']:
                file_path = os.path.join(year_dir, f"{ticker}{suffix}.csv")
                if os.path.isfile(file_path):  # 确保文件存在
                    # 读取CSV文件的指定列
                    data = pd.read_csv(file_path, usecols=['trade_time', 'close'])
                    all_data.append(data)
                    break  # 如果找到文件，则不需要尝试另一个后缀
    
    if all_data:
        # 合并数据
        merged_data = pd.concat(all_data)
        # 按交易时间排序



        
        merged_data.sort_values(by='trade_time', inplace=True)
        # 保存到merged文件夹
        merged_data.to_csv(os.path.join(merged_dir, f"{ticker}.csv"), index=False)