### 从分钟数据的文件名中提取股票列表

import os
import json

def get_stock_id(path):
    stock_id = [''.join(filter(str.isdigit, f)) for f in os.listdir(path) if f.endswith('.csv')]
    stock_id_sorted = sorted(stock_id)
    return stock_id_sorted

# 分钟数据的文件夹路径
path_to_folder = 'data/2024/'

stock_ids_sorted = get_stock_id(path_to_folder)

# 目标JSON文件路径
path_to_json_file = 'stock_id.json'

with open(path_to_json_file, 'w') as json_file:
    json.dump(stock_ids_sorted, json_file, indent=4)