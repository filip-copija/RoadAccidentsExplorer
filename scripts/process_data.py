import pandas as pd
from pathlib import Path

def process_csv(file_path):
    data = pd.read_csv(file_path, delimiter=";")

    data.columns = ["Code", "Region", "Accident_Type", "Year", "Value", "Unit", "Attribute"]

    data = data.drop(columns=["Attribute"])
    data["Value"] = pd.to_numeric(data["Value"], errors="coerce").fillna(0).astype(int)

    data["Region"] = data["Region"].str.strip()
    data["Accident_Type"] = data["Accident_Type"].str.strip()
    data["Unit"] = data["Unit"].str.strip()

    def determine_region_type(code):
        code_str = str(code).zfill(6)
        if code_str[2:] == "0000":
            return "województwo"
        elif code_str[4:] == "00":
            return "powiat"
        else:
            return "miasto"

    data["Type"] = data["Code"].apply(determine_region_type)

    provinces = data[data["Type"] == "województwo"].drop_duplicates(subset=["Region"])
    counties = data[data["Type"] == "powiat"].drop_duplicates(subset=["Region"])
    cities = data[data["Type"] == "miasto"].drop_duplicates(subset=["Region"])

    regions_data = pd.concat([provinces, counties, cities])[["Region", "Type"]].drop_duplicates()

    accidents_data = data[["Region", "Year", "Accident_Type", "Value", "Unit"]]

    return regions_data, accidents_data
