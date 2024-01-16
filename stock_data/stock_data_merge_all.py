import pandas as pd
import os
from tqdm import tqdm

def merge_csv_files(folder_path, output_file):
    merged_data = pd.DataFrame()
    files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    for file in tqdm(files, desc='Merging files'):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, parse_dates=['trade_time'])
        file_name = os.path.splitext(file)[0]
        df.rename(columns={'close': file_name}, inplace=True)
        
        if merged_data.empty:
            merged_data = df
        else:
            merged_data = pd.merge_ordered(merged_data, df, on='trade_time', fill_method='ffill')

    merged_data.to_csv(output_file, index=False)

# 使用方法
folder_path = 'data/'  # 替换为您的文件夹路径
output_file = 'merged_data.csv'  # 您希望保存的文件名
merge_csv_files(folder_path, output_file)
