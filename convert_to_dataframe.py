import pandas as pd
import json

# Path to your JSON file
file_path = "preprocessed.json"

with open(file_path, "r") as file:
    json_data = json.load(file)

parsed_data = []
for key, value in json_data.items():
    for item in value:
        letter = item[0]
        details = item[1]
        for detail in details:
            detail["letter"] = letter
            detail["sequence"] = key
            parsed_data.append(detail)

df = pd.DataFrame(parsed_data)

# Filtering sequences with a specific motion type 'pro'
filtered_pro = df[df['motion_type'] == 'pro']

# Sorting sequences based on the number of turns
sorted_by_turns = df.sort_values(by='turns')

# Counting the frequency of each letter in sequences
letter_frequency = df['letter'].value_counts()

# You can then print these DataFrames or save them to a file
print(filtered_pro.head())
print(sorted_by_turns.head())
print(letter_frequency.head())
