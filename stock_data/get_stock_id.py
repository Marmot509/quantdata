import os
import json

# Define the updated function to modify the filenames as required
def get_stock_id_with_prefix(path):
    stock_ids = []
    for f in os.listdir(path):
        if f.endswith('.csv'):
            # Extract numeric part
            numeric_part = ''.join(filter(str.isdigit, f))
            # Extract the letter part (.SZ or .SH), convert to lowercase and prepend to the numeric part
            letter_part = f.split('.')[1].lower()
            stock_id = letter_part + numeric_part
            stock_ids.append(stock_id)
    # Sort the list of IDs
    return sorted(stock_ids)

# Replace 'path_to_folder' with the actual path to your folder containing the CSV files
path_to_folder = 'data/2024'

# Get the modified stock ids
stock_ids_with_prefix = get_stock_id_with_prefix(path_to_folder)

# Convert the list of modified stock ids to JSON format
json_content = json.dumps(stock_ids_with_prefix, indent=4)

# Replace 'path_to_json_file' with the actual path where you want to save the JSON file
path_to_json_file = 'ticker.json'

# Write the JSON content to a file
with open(path_to_json_file, 'w') as json_file:
    json_file.write(json_content)