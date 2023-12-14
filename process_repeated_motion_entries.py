import json
import pandas as pd

# Load JSON data
with open("preprocessed.json") as f:
    data = json.load(f)

# Helper function to flatten the nested JSON structure
def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            for i, a in enumerate(x):
                flatten(a, name + str(i) + "_")
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Flatten each entry in the JSON file
flat_list = [flatten_json(entry) for key in data for entry in data[key]]

# Convert to DataFrame
df = pd.DataFrame(flat_list)

# Print the first few rows to see the dataframe structure
print(df.head())

# Assuming that all the relevant attributes are prefixed by a common index (like '0_' or '1_'),
# we can filter the columns to include only those that contain motion attributes.
# This will dynamically create the subset list for drop_duplicates.
motion_attribute_columns = [col for col in df.columns if 'color' in col or 'motion_type' in col or 'rotation_direction' in col or 'arrow_location' in col or 'start_location' in col or 'end_location' in col or 'turns' in col]

# Now drop duplicates based on the motion attributes
df_unique = df.drop_duplicates(subset=motion_attribute_columns).reset_index(drop=True)

# Save the unique motions to a new JSON file
df_unique.to_json("unique_motions.json", orient="records", indent=4)

# Print the unique motions DataFrame
print(df_unique)
