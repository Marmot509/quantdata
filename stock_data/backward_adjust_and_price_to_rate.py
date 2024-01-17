import pandas as pd
from tqdm import tqdm

# 假设股票价格数据的文件路径
stock_prices_path = 'data/merged_data.csv'
# 假设后复权因子文件夹的路径
adjust_factor_path = 'data/backward_adjust_factor/'

# 分块大小
chunksize = 10**5  # 根据您的内存调整

# 读取股票价格数据的行数来计算总块数
total_rows = sum(1 for row in open(stock_prices_path, 'r'))
total_chunks = total_rows // chunksize + (total_rows % chunksize > 0)

# 初始化存储后复权价格的DataFrame
adjusted_prices = None

# 使用tqdm显示进度条
with tqdm(total=total_chunks, desc="Processing chunks") as pbar:
    for chunk in pd.read_csv(stock_prices_path, chunksize=chunksize):
        chunk['trade_time'] = pd.to_datetime(chunk['trade_time'])
        if adjusted_prices is None:
            adjusted_prices = pd.DataFrame()
            adjusted_prices['trade_time'] = chunk['trade_time']

        # 对于每个股票代码
        for stock_code in chunk.columns[1:]:
            try:
                # 尝试加载后复权因子文件
                hfq_factor_file = f'{adjust_factor_path}sh{stock_code}.csv'
                hfq_factors = pd.read_csv(hfq_factor_file)
            except FileNotFoundError:
                try:
                    hfq_factor_file = f'{adjust_factor_path}sz{stock_code}.csv'
                    hfq_factors = pd.read_csv(hfq_factor_file)
                except FileNotFoundError:
                    # 如果都找不到，打印信息并跳过该股票
                    print(f"未找到股票 {stock_code} 的后复权因子文件")
                    continue

            hfq_factors['date'] = pd.to_datetime(hfq_factors['date'])
            hfq_factors.sort_values('date', inplace=True)
            hfq_factors.set_index('date', inplace=True)

            # 计算后复权价格
            adjusted_chunk = chunk.apply(
                lambda row: row[stock_code] * hfq_factors.loc[:row['trade_time']].iloc[-1]['hfq_factor'],
                axis=1
            )
            adjusted_prices[stock_code] = adjusted_chunk

        pbar.update(1)  # 更新进度条

# 设置交易时间为索引
adjusted_prices.set_index('trade_time', inplace=True)

# 保存结果
adjusted_prices.to_csv('data/stock_prices_hfq.csv', index=True)
print('data/stock_prices_hfq.csv saved')

# 计算收益率
returns = adjusted_prices.pct_change()
print('returns calculated')

# 移除收益率DataFrame中的第一行，因为它将会是NaN（第一个点没有前一个点来计算收益率）
returns = returns.iloc[1:]

# 将收益率DataFrame保存为CSV文件
returns.to_csv('data/stock_returns.csv', index=True)
print('data/stock_returns.csv saved')

# 将收益率DataFrame保存为序列化的二进制文件（Pickle格式）
returns.to_pickle('data/stock_returns.pkl')
print('data/stock_returns.pkl saved')
