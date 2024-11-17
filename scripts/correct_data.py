import pandas as pd
from pathlib import Path

current_dir = Path(__file__).parent
file_path = current_dir.parent / "data" / "raw_accidents_2019_2024.csv"
output_path = current_dir.parent / "data" / "correct_accidents_2019_2024.csv"

data = pd.read_csv(file_path, encoding='utf-8')

replacements = {
    " (1)": "",
    " (2)": "",
    " (3)": "",
}

def replace_invalid_chars(text):
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    return text

data = data.applymap(lambda x: replace_invalid_chars(x) if isinstance(x, str) else x)
data.to_csv(output_path, index=False, encoding="utf-8")
