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
        code = str(code).zfill(7)  
        if code == "0000000":  # Województwo 
            return "kraj"
        if code[2:] == "00000":  # Województwo
            return "województwo"
        elif code.isdigit() and len(code) == 7:  # Miasto
            return "miasto"
        else:
            return "nieznane"

    data["Type"] = data["Code"].apply(determine_region_type)

    countries = data[data["Type"] == "kraj"].drop_duplicates(subset=["Region"])
    provinces = data[data["Type"] == "województwo"].drop_duplicates(subset=["Region"])
    counties = data[data["Type"] == "powiat"].drop_duplicates(subset=["Region"])
    cities = data[data["Type"] == "miasto"].drop_duplicates(subset=["Region"])

    regions_data = pd.concat([countries, provinces, counties, cities])[["Region", "Type"]].drop_duplicates()

    accidents_data = data[["Region", "Year", "Accident_Type", "Value", "Unit"]]

    return regions_data, accidents_data
