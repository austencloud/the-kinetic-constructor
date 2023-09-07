import os

def replace_text_in_file(file_path, replacement):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    with open(file_path, 'w', encoding='utf-8') as file:
        for key, value in replacement.items():
            file_contents = file_contents.replace(key, value)
        file.write(file_contents)

def process_files(folder_path):
    # Define the mapping of text to Greek symbols
    greek_symbols = {
        'sigma': 'Σ',
        'delta': 'Δ',
        'theta': 'θ',
        'omega': 'Ω',
        'phi': 'Φ',
        'psi': 'Ψ',
        'lambda': 'Λ',
        'alpha': 'α',
        'beta': 'β',
        'gamma': 'Γ',
        'mu': 'μ',
        'nu': 'ν',
        'eta': 'η',
        'zeta': 'ζ',
        'tau': 'τ',
        'terra': '⊕'
    }

    # Iterate through the files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.svg'):
            file_path = os.path.join(folder_path, file_name)
            print(f'Processing file: {file_path}')
            replace_text_in_file(file_path, greek_symbols)
            print(f'Processed file: {file_path}')

folder_path = '/images/letters/greek'  # Replace with the path to the folder containing your files
process_files(folder_path)
