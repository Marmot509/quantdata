import json
import re

# 假设你的json文件名为'top_market_cap_stocks.json'
with open('stock_data/top_market_cap_stocks.json', 'r') as f:
    data = json.load(f)

# 遍历json文件中的所有字符串
for i in range(len(data)):
    # 使用正则表达式去掉数字后面的.和字母
    data[i] = re.sub(r'(\d)\.[a-zA-Z]*', r'\1', data[i])

data = sorted(data)

# 将修改后的数据写回json文件
with open('stock_data/top_market_cap_stocks.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)