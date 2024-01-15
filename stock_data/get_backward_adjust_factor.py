import akshare as ak
import json
import os

# 读取股票代码
path_to_json_file = 'stock_id.json'
with open(path_to_json_file, 'r') as json_file:
    stock_ids = json.load(json_file)

# 检查并获取后复权因子
for stock_id in stock_ids:
    filename = f"{stock_id}.csv"

    # 检查文件是否存在
    if not os.path.exists("backward_adjust_factor/"+filename):
        # 调用 API 获取数据
        df = ak.stock_zh_a_daily(symbol=stock_id, adjust="hfq-factor")

        # 保存数据到 CSV 文件
        df.to_csv("backward_adjust_factor/"+filename, index=False)
        print(f"{stock_id} data saved to {filename}")
    else:
        print(f"File {filename} already exists. Skipping.")
