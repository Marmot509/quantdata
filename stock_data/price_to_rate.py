import pandas as pd

stock_prices_path = 'data/merged_data.csv'
output_path = 'data/stock_returns.csv'

# 设置每个块的列数
columns_per_chunk = 50

# 读取列名
all_columns = pd.read_csv(stock_prices_path, nrows=0).columns.tolist()
date_column = ['trade_time']
feature_columns = [col for col in all_columns if col != 'trade_time']

# 存储每个块处理后的结果
chunk_results = []

# 按列分块处理
for i in range(0, len(feature_columns), columns_per_chunk):
    chunk_columns = date_column + feature_columns[i:i + columns_per_chunk]
    stock_data_chunk = pd.read_csv(stock_prices_path, usecols=chunk_columns)
    stock_data_chunk.set_index('trade_time', inplace=True)

    # 计算收益率
    stock_returns = stock_data_chunk.pct_change()
    stock_returns = stock_returns.iloc[1:]  # 去掉第一行

    # 将结果存储在列表中
    chunk_results.append(stock_returns.reset_index())

# 合并所有处理后的块
final_result = pd.concat(chunk_results, axis=1)

# 移除重复的trade_time列
final_result = final_result.loc[:,~final_result.columns.duplicated()]

# 将最终结果写入文件
final_result.to_csv(output_path, index=True)

print("处理完成，结果已保存到:", output_path)
