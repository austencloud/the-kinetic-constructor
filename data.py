
letter_positions = {
    "A": ("alpha", "alpha"),
    "B": ("alpha", "alpha"),
    "C": ("alpha", "alpha"),
    "D": ("beta", "alpha"),
    "E": ("beta", "alpha"),
    "F": ("beta", "alpha"),
    "G": ("beta", "beta"),
    "H": ("beta", "beta"),
    "I": ("beta", "beta"),
    "J": ("alpha", "beta"),
    "K": ("alpha", "beta"),
    "L": ("alpha", "beta"),
    "M": ("gamma", "gamma"),
    "N": ("gamma", "gamma"),
    "O": ("gamma", "gamma"),
    "P": ("gamma", "gamma"),
    "Q": ("gamma", "gamma"),
    "R": ("gamma", "gamma"),
    "S": ("gamma", "gamma"),
    "T": ("gamma", "gamma"),
    "U": ("gamma", "gamma"),
    "V": ("gamma", "gamma"),
    "W": ("gamma", "alpha"),
    "X": ("gamma", "alpha"),
    "Y": ("gamma", "beta"),
    "Z": ("gamma", "beta"),
    "Σ": ("alpha", "gamma"),
    "Δ": ("alpha", "gamma"),
    "θ": ("beta", "gamma"),
    "Ω": ("beta", "gamma"),
    "Φ": ("beta", "alpha"),
    "Ψ": ("alpha", "beta"),
    "Λ": ("gamma", "gamma"),
    "W-": ("gamma", "alpha"),
    "X-": ("gamma", "alpha"),
    "Y-": ("gamma", "beta"),
    "Z-": ("gamma", "beta"),
    "Σ-": ("beta", "gamma"),
    "Δ-": ("beta", "gamma"),
    "θ-": ("alpha", "gamma"),
    "Ω-": ("alpha", "gamma"),
    "Φ-": ("alpha", "alpha"),
    "Ψ-": ("beta", "beta"),
    "Λ-": ("gamma", "gamma"),
    "α": ("alpha", "alpha"),
    "β": ("beta", "beta"),
    "Γ": ("gamma", "gamma"),
}

compass_mapping = {
    "alpha": ("n", "s"),
    "alpha": ("w", "e"),
    "beta": ("e", "e"),
    "beta": ("s", "s"),
    "beta": ("w", "w"),
    "beta": ("n", "n"),
    "gamma": ("n", "e"),
    "gamma": ("e", "s"),
    "gamma": ("s", "w"),
    "gamma": ("w", "n"),
}
positions_map = {
    ('n', 'red', 's', 'blue'): 'alpha1',
    ('e', 'red', 'w', 'blue'): 'alpha2',
    ('s', 'red', 'n', 'blue'): 'alpha3',
    ('w', 'red', 'e', 'blue'): 'alpha4',
    ('n', 'red', 'n', 'blue'): 'beta1',
    ('e', 'red', 'e', 'blue'): 'beta2',
    ('s', 'red', 's', 'blue'): 'beta3',
    ('w', 'red', 'w', 'blue'): 'beta4',
    ('n', 'red', 'w', 'blue'): 'gamma1',
    ('e', 'red', 'n', 'blue'): 'gamma2',
    ('s', 'red', 'e', 'blue'): 'gamma3',
    ('w', 'red', 's', 'blue'): 'gamma4',
    ('n', 'red', 'e', 'blue'): 'gamma5',
    ('e', 'red', 's', 'blue'): 'gamma6',
    ('s', 'red', 'w', 'blue'): 'gamma7',
    ('w', 'red', 'n', 'blue'): 'gamma8',
}

letter_types = {
    'Type 1': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V'],
    'Type 2': ['W', 'X', 'Y', 'Z', 'Σ', 'Δ', 'θ', 'Ω'],
    'Type 3': ['W-', "X-", 'Y-', 'Z-', 'Σ-', 'Δ-', 'θ-', 'Ω-'],
    'Type 4': ['Φ', 'Ψ', 'Λ'],
    'Type 5': ['Φ-', 'Ψ-', 'Λ-'],
    'Type 6': ['α', 'β', 'Γ'],
}



ARROW_START_END_LOCATIONS = {
    "anti_l_ne_0.svg": ("n", "e"),
    "anti_l_se_0.svg": ("e", "s"),
    "anti_l_sw_0.svg": ("s", "w"),
    "anti_l_nw_0.svg": ("w", "n"),
    
    "anti_r_ne_0.svg": ("e", "n"),
    "anti_r_se_0.svg": ("s", "e"),
    "anti_r_sw_0.svg": ("w", "s"),
    "anti_r_nw_0.svg": ("n", "w"),
    
    "pro_l_ne_0.svg": ("e", "n"),
    "pro_l_se_0.svg": ("s", "e"),
    "pro_l_sw_0.svg": ("w", "s"),
    "pro_l_nw_0.svg": ("n", "w"),
    
    "pro_r_ne_0.svg": ("n", "e"),
    "pro_r_se_0.svg": ("e", "s"),
    "pro_r_sw_0.svg": ("s", "w"),
    "pro_r_nw_0.svg": ("w", "n"),
}

def calculate_quadrant(start_position, end_position):
    if start_position == "n" and end_position == "e" or start_position == "e" and end_position == "n":
        return "ne"
    elif start_position == "n" and end_position == "w" or start_position == "w" and end_position == "n":
        return "nw"
    elif start_position == "s" and end_position == "e" or start_position == "e" and end_position == "s":
        return "se"
    elif start_position == "s" and end_position == "w" or start_position == "w" and end_position == "s":
        return "sw"
    # Add more conditions here if necessary

def generate_variations(arrow_combination):
    # Define the mappings for rotations and reflections
    rotation_mapping = {"n": "e", "e": "s", "s": "w", "w": "n"}
    vertical_reflection_mapping = {"n": "s", "s": "n", "e": "e", "w": "w"}
    horizontal_reflection_mapping = {"n": "n", "s": "s", "e": "w", "w": "e"}
    rotation_reflection_mapping = {"l": "r", "r": "l"}

    # Generate the rotated versions
    rotated_versions = [arrow_combination]
    for _ in range(3):
        arrow_combination = [{**arrow, 
                              "start_position": rotation_mapping[arrow["start_position"]],
                              "end_position": rotation_mapping[arrow["end_position"]],
                              "quadrant": calculate_quadrant(rotation_mapping[arrow["start_position"]], rotation_mapping[arrow["end_position"]])} 
                             for arrow in arrow_combination]
        rotated_versions.append(arrow_combination)

    # Generate the reflected versions
    reflected_versions = []
    for version in rotated_versions:
        vertical_reflected_version = [{**arrow, 
                                       "start_position": vertical_reflection_mapping[arrow["start_position"]],
                                       "end_position": vertical_reflection_mapping[arrow["end_position"]],
                                       "rotation": rotation_reflection_mapping[arrow["rotation"]],
                                       "quadrant": calculate_quadrant(vertical_reflection_mapping[arrow["start_position"]], vertical_reflection_mapping[arrow["end_position"]])} 
                                      for arrow in version]
        horizontal_reflected_version = [{**arrow, 
                                         "start_position": horizontal_reflection_mapping[arrow["start_position"]],
                                         "end_position": horizontal_reflection_mapping[arrow["end_position"]],
                                         "rotation": rotation_reflection_mapping[arrow["rotation"]],
                                         "quadrant": calculate_quadrant(horizontal_reflection_mapping[arrow["start_position"]], horizontal_reflection_mapping[arrow["end_position"]])} 
                                        for arrow in version]
        reflected_versions.extend([vertical_reflected_version, horizontal_reflected_version])

    return rotated_versions + reflected_versions

