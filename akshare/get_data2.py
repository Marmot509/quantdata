import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


# # 获取国债收益率
# start_date = datetime(1990, 1, 1)
# end_date = datetime(2024, 1, 12)

# all_data = pd.DataFrame()
# while start_date < end_date:
#     current_end_date = min(start_date + timedelta(days=365), end_date)
#     start_str = start_date.strftime('%Y%m%d')
#     end_str = current_end_date.strftime('%Y%m%d')

#     temp_data = ak.bond_china_yield(start_date=start_str, end_date=end_str)
#     filtered_data = temp_data[temp_data['曲线名称'] == '中债国债收益率曲线']
#     all_data = pd.concat([all_data, filtered_data])
#     start_date = current_end_date + timedelta(days=1)

# all_data.to_csv("cn_treasury_bond_yield.csv", index=False)

# # 获取汇率数据
# forex_rate = ak.currency_boc_safe()
# forex_rate.to_csv("forex_rate.csv", index=False)

# 获取Shibor利率
shibor_on = ak.rate_interbank(market="上海银行同业拆借市场", symbol="Shibor人民币", indicator="隔夜")
shibor_on.to_csv("shibor_on.csv", index=False)
shibor_3m = ak.rate_interbank(market="上海银行同业拆借市场", symbol="Shibor人民币", indicator="3月")
shibor_3m.to_csv("shibor_3m.csv", index=False)
shibor_1y = ak.rate_interbank(market="上海银行同业拆借市场", symbol="Shibor人民币", indicator="1年")
shibor_1y.to_csv("shibor_1y.csv", index=False)

