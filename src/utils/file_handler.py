import pandas as pd

def load_numbers_from_file(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    # Assuming the phone numbers are in the first column
    numbers = df.iloc[:, 0].astype(str).tolist()
    return numbers