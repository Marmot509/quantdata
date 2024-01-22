import akshare as ak
import pandas as pd

# # 上证指数
# index_sh = ak.stock_zh_index_daily(symbol="sh000001")
# index_sh.to_csv("sh000001_d.csv", index=False)

# # 深证成指
# index_sz = ak.stock_zh_index_daily(symbol="sz399001")
# index_sz.to_csv("sz399001_d.csv", index=False)

# # 上交所融资融券余额
# sh_margin1 = ak.stock_margin_sse(start_date="20160101", end_date="20240208")
# sh_margin2 = ak.stock_margin_sse(start_date="20100106", end_date="20160101")
# sh_margin = pd.concat([sh_margin1, sh_margin2])
# sh_margin.to_csv("sh_margin.csv", index=False)

# 深交所融资融券余额
# csv_data = pd.read_csv("akshare_data/sh_margin.csv")
# dates = csv_data['信用交易日期'].astype(str)

# all_data = []
# for date in dates:
#     try:
#         formatted_date = pd.to_datetime(date).strftime('%Y%m%d')
#         daily_data = ak.stock_margin_szse(date=formatted_date)
#         all_data.append(daily_data)
#         print(formatted_date, 'done')
#     except Exception as e:
#         print(f"Error getting data for date {formatted_date}: {e}")

# all_data_df = pd.concat(all_data)
# all_data_df.to_csv("akshare_data/sz_margin.csv", index=False)


