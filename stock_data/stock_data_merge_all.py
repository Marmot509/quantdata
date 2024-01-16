import pandas as pd
import os
from tqdm import tqdm

def merge_csv_files(folder_path, output_file):
    # 创建一个空的 DataFrame 用于存放合并后的数据
    merged_data = pd.DataFrame()

    # 保存文件名和相应的 DataFrame
    data_frames = {}

    # 获取文件夹中所有 CSV 文件的列表
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    # 使用 tqdm 显示进度条
    for file in tqdm(csv_files, desc="Merging CSV files"):
        file_path = os.path.join(folder_path, file)
        # 读取 CSV 文件
        df = pd.read_csv(file_path, parse_dates=['trade_time'])
        # 使用文件名（不包括 .csv）作为列名
        file_name = os.path.splitext(file)[0]
        df.rename(columns={'close': file_name}, inplace=True)
        # 保存 DataFrame
        data_frames[file_name] = df

    # 对文件名进行排序
    sorted_file_names = sorted(data_frames.keys())

    # 根据排序结果合并数据
    for file_name in sorted_file_names:
        df = data_frames[file_name]
        if merged_data.empty:
            merged_data = df
        else:
            merged_data = pd.merge(merged_data, df, on='trade_time', how='outer')

    # 对结果按照 trade_time 排序
    merged_data.sort_values(by='trade_time', inplace=True)

    # 保存到新的 CSV 文件
    merged_data.to_csv(output_file, index=False)

# 使用方法
folder_path = 'data/'  # 替换为您的文件夹路径
output_file = 'merged_data.csv'  # 您希望保存的文件名
merge_csv_files(folder_path, output_file)
