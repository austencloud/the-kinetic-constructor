import json

# Load JSON data
with open("preprocessed.json", encoding='utf-8') as f:
    data = json.load(f)

# Function to check if a dictionary is a motion dictionary
def is_motion_dict(d):
    return all(key in d for key in ['color', 'motion_type', 'arrow_location', 'start_location', 'end_location', 'turns'])

# Function to generate motion name
def generate_motion_name(motion, start_orientation):
    end_orientation = 'in' if motion['motion_type'] == 'pro' else 'out'
    if start_orientation == 'out':
        end_orientation = 'out' if motion['motion_type'] == 'pro' else 'in'
    return f"{motion['color']}_{motion['motion_type']}_{motion['start_location']}_{motion['end_location']}_{motion['turns']}_{start_orientation}_{end_orientation}"

# Extract all motion dictionaries
all_motions = []
for key in data:
    for combo in data[key]:
        all_motions.extend([motion for motion in combo[1] if is_motion_dict(motion)])  # Filter out non-motion dictionaries

# Identify unique motions and assign variable names
unique_motions_in = {}
unique_motions_out = {}
for motion in all_motions:
    # Create a variable name based on the motion attributes for starting in orientation
    motion_name_in = generate_motion_name(motion, 'in')
    # Create a variable name based on the motion attributes for starting out orientation
    motion_name_out = generate_motion_name(motion, 'out')
    # Add to unique motions if not already present
    if motion_name_in not in unique_motions_in:
        unique_motions_in[motion_name_in] = motion
    if motion_name_out not in unique_motions_out:
        unique_motions_out[motion_name_out] = motion

# Save the unique motions to JSON files with UTF-8 encoding
with open("unique_motions_in.json", 'w', encoding='utf-8') as f:
    json.dump(unique_motions_in, f, indent=4, ensure_ascii=False)
with open("unique_motions_out.json", 'w', encoding='utf-8') as f:
    json.dump(unique_motions_out, f, indent=4, ensure_ascii=False)

# Now, let's create the new structure for the combinations with in orientation
new_combinations_in = {}
for key in data:
    new_combinations_in[key] = []
    for letter, combo in data[key]:
        new_combo = []
        for motion in combo:
            if is_motion_dict(motion):
                motion_name = generate_motion_name(motion, 'in')
                new_combo.append(motion_name)
        new_combinations_in[key].append((letter, tuple(new_combo)))

# Now, let's create the new structure for the combinations with out orientation
new_combinations_out = {}
for key in data:
    new_combinations_out[key] = []
    for letter, combo in data[key]:
        new_combo = []
        for motion in combo:
            if is_motion_dict(motion):
                motion_name = generate_motion_name(motion, 'out')
                new_combo.append(motion_name)
        new_combinations_out[key].append((letter, tuple(new_combo)))

# Simplify the structure of new_combinations
for key, combos in new_combinations_out.items():
    simplified_combos = {combo[0]: combo[1] for combo in combos}
    new_combinations_out[key] = simplified_combos

# Save the simplified combinations to JSON file with UTF-8 encoding
with open("0_shift_out.json", 'w', encoding='utf-8') as f:
    json.dump(new_combinations_out, f, indent=4, ensure_ascii=False)
    
# Simplify the structure of new_combinations
for key, combos in new_combinations_in.items():
    simplified_combos = {combo[0]: combo[1] for combo in combos}
    new_combinations_in[key] = simplified_combos

# Save the simplified combinations to JSON file with UTF-8 encoding
with open("0_shift_in.json", 'w', encoding='utf-8') as f:
    json.dump(new_combinations_in, f, indent=4, ensure_ascii=False)