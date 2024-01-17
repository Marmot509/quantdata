import pandas

# 假设股票价格数据的文件路径
stock_prices_path = 'merged_data.csv'
# 假设后复权因子文件夹的路径
adjust_factor_path = 'backward_adjust_factor/'

# 加载股票价格数据
stock_prices = pd.read_csv(stock_prices_path)

# 将交易时间转换为pandas的datetime格式
stock_prices['trade_time'] = pd.to_datetime(stock_prices['trade_time'])

# 创建一个空的DataFrame来存储后复权价格
adjusted_prices = pd.DataFrame()
adjusted_prices['trade_time'] = stock_prices['trade_time']

# 对于每个股票代码，执行以下操作
for stock_code in stock_prices.columns[1:]:  # 跳过交易时间列
    # 尝试加载后复权因子文件，如果以'sh'开头的没有找到，尝试以'sz'开头
    try:
        hfq_factor_file = f'{adjust_factor_path}sh{stock_code}.csv'
        hfq_factors = pd.read_csv(hfq_factor_file)
    except FileNotFoundError:
        hfq_factor_file = f'{adjust_factor_path}sz{stock_code}.csv'
        hfq_factors = pd.read_csv(hfq_factor_file)
    
    # 将日期转换为datetime格式，并按日期排序
    hfq_factors['date'] = pd.to_datetime(hfq_factors['date'])
    hfq_factors.sort_values('date', inplace=True)
    
    # 设置索引为日期，便于后续查找
    hfq_factors.set_index('date', inplace=True)
    
    # 计算后复权价格
    adjusted_prices[stock_code] = stock_prices.apply(
        lambda row: row[stock_code] * hfq_factors.loc[:row['trade_time']].iloc[-1]['hfq_factor'],
        axis=1
    )

    print(stock_code + ' done')

adjusted_prices.set_index('trade_time', inplace=True)

# 将后复权价格DataFrame保存为CSV文件
adjusted_prices.to_csv('stock_prices_hfq.csv', index=True)
print('stock_prices_hfq.csv saved')

# 计算收益率
returns = adjusted_prices.pct_change()
print('returns calculated')

# 移除收益率DataFrame中的第一行，因为它将会是NaN（第一个点没有前一个点来计算收益率）
returns = returns.iloc[1:]

# 将收益率DataFrame保存为CSV文件
returns.to_csv('stock_returns.csv', index=True)
print('stock_returns.csv saved')

# 将收益率DataFrame保存为序列化的二进制文件（Pickle格式）
returns.to_pickle('stock_returns.pkl')
print('stock_returns.pkl saved')
