import akshare as ak
import json

# 读取股票代码
path_to_json_file = 'stock_id.json'
with open(path_to_json_file, 'r') as json_file:
    stock_ids = json.load(json_file)

# 获取后复权因子
results = []
for stock_id in stock_ids:  # 为了演示，这里只处理前5个股票代码
    df = ak.stock_zh_a_daily(symbol=stock_id, adjust="hfq-factor")
    results.append({
        "stock_id": stock_id,
        "backward_factor": df.to_json(orient="records", date_format="iso")
    })
    print(stock_id, 'done')

# 将结果保存到 JSON 文件
with open('backward_factors.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
