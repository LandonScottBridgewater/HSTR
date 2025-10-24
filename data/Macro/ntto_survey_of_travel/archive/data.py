import json
import re
import pandas as pd

def excel_to_json(path):

    sheets = {
        "14 & 15": {
            "Section": "Purpose",
            "Columns": [1, 13],
            "Rows": [5, 15]
        },
        "38": {
            "Section": "Household Income",
            "Columns": [1, 11],
            "Rows": [5, 23]
        }
    }

    d1 = {}

    def merge_business_categories(data):
        section = "Purpose"
        target_key = "Business"
        merge_keys = ["Business**", "Business (Other)**", "Business (Other)*"]

        if section not in data:
            return

        if target_key not in data[section]:
            data[section][target_key] = {}

        for merge_key in merge_keys:
            if merge_key in data[section]:
                for row_key, year_data in data[section][merge_key].items():
                    if row_key not in data[section][target_key]:
                        data[section][target_key][row_key] = {}

                    for year, quarter_data in year_data.items():
                        if year not in data[section][target_key][row_key]:
                            data[section][target_key][row_key][year] = {}

                        for quarter, val in quarter_data.items():
                            if quarter in data[section][target_key][row_key][year]:
                                existing_val = data[section][target_key][row_key][year][quarter]
                                try:
                                    data[section][target_key][row_key][year][quarter] = existing_val + val
                                except TypeError:
                                    data[section][target_key][row_key][year][quarter] = val
                            else:
                                data[section][target_key][row_key][year][quarter] = val

                del data[section][merge_key]

    def per_sheet(sheet: pd.DataFrame, sheet_name, year, quarter):
        cfg = sheets[sheet_name]

        rows = slice(cfg["Rows"][0]-1, cfg["Rows"][1])
        cols = slice(cfg["Columns"][0]-1, cfg["Columns"][1])
        df = sheet.iloc[rows, cols].copy()

        header_rows = df.iloc[0:2].fillna("").astype(str)
        new_cols = (
            header_rows.apply(lambda x: " ".join([c.strip() for c in x if c.strip()]), axis=0)
            .str.replace("\n", " ", regex=False)
            .str.replace("Hotel/ Motel Lodging", "Hotel / Motel Lodging")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
        df.columns = new_cols
        df = df.drop(df.index[0:2])
        df = df.set_index(df.columns[0])

        result = {}
        for row_idx, row in df.iterrows():
            row_key = str(row_idx).replace("\n", " ").strip()
            if row_key == "":
                row_key = "All U.S."
            result.setdefault(row_key, {})

            for col_idx, val in row.items():
                col_name = str(col_idx).replace("\n", " ").strip()
                if col_name == "":
                    col_name = "All U.S."

                result[row_key].setdefault(col_name, {})
                result[row_key][col_name].setdefault(f"20{year}", {})

                if quarter != "Annual":
                    result[row_key][col_name][f"20{year}"][f"Q{quarter}"] = val
                else:
                    result[row_key][col_name][f"20{year}"]["Aggregate"] = val

        return result

    def iter_sheets(file_path, sheets, year, quarter):
        for sheet in sheets.keys():
            df = pd.read_excel(file_path, f"Table {sheet}")
            section = sheets[sheet]["Section"]
            new_data = per_sheet(df, sheet, year, quarter)

            if section not in d1:
                d1[section] = {}

            for row_key, row_val in new_data.items():
                if row_key not in d1[section]:
                    d1[section][row_key] = {}
                for col_key, col_val in row_val.items():
                    if col_key not in d1[section][row_key]:
                        d1[section][row_key][col_key] = {}
                    for year_key, year_val in col_val.items():
                        if year_key not in d1[section][row_key][col_key]:
                            d1[section][row_key][col_key][year_key] = {}

                        d1[section][row_key][col_key][year_key].update(year_val)

    for year in range(22, 25):
        yearly_file = f"{path}{year}A.xlsx"
        iter_sheets(yearly_file, sheets, year, "Annual")

        for quarter in range(1, 5):
            quarterly_file = f"{path}{year}Q{quarter}.xlsx"
            iter_sheets(quarterly_file, sheets, year, quarter)

    merge_business_categories(d1)

    return d1

def data_refit(income, purpose):

    def purpose_refit(purpose):
        d1 = purpose

        def nested(d1):
            for k in d1.keys():
                if isinstance(d1[k],float):
                    d1[k] = round(d1[k]*100,2)
                    print(d1[k])
                elif isinstance(d1[k],dict):
                    nested(d1[k])
            return d1

        nested(d1)

        return d1

    def income_refit(income):
        d1 = {}

        def range_mean(range_str):
            numbers = re.findall(r'\$?[\d,]+', range_str)
            clean_numbers = [int(n.replace('$', '').replace(',', '')) for n in numbers]
            if len(clean_numbers) == 2:
                return int(round(sum(clean_numbers) / 2, -3))
            else:
                raise ValueError(f"Could not find exactly two numbers in input: {range_str}")

        def is_valid_number(val):
            if isinstance(val, (int, float)):
                return True
            if isinstance(val, str):
                val_clean = val.strip().replace(',', '')
                return val_clean.replace('.', '', 1).isdigit()
            return False

        def to_number(val):
            if isinstance(val, (int, float)):
                return val
            val_clean = val.strip().replace(',', '')
            if '.' in val_clean:
                return float(val_clean)
            return int(val_clean)

        def calc(k, label):
            for kk in income[k]:
                for year in income[k][kk]:
                    for quarter in income[k][kk][year]:
                        value_raw = income[k][kk][year][quarter]
                        respondents_raw = income["Number of Respondents"][kk][year][quarter]

                        if not is_valid_number(value_raw) or not is_valid_number(respondents_raw):
                            continue

                        value = to_number(value_raw)
                        respondents = to_number(respondents_raw)

                        # Initialize Point Oriented dictionaries
                        if "Point Oriented" not in d1:
                            d1["Point Oriented"] = {}

                        # Inter-class
                        if "Inter-class" not in d1["Point Oriented"]:
                            d1["Point Oriented"]["Inter-class"] = {}
                        if kk not in d1["Point Oriented"]["Inter-class"]:
                            d1["Point Oriented"]["Inter-class"][kk] = {}
                        if year not in d1["Point Oriented"]["Inter-class"][kk]:
                            d1["Point Oriented"]["Inter-class"][kk][year] = {}
                        if quarter not in d1["Point Oriented"]["Inter-class"][kk][year]:
                            d1["Point Oriented"]["Inter-class"][kk][year][quarter] = {}

                        prev_point_inter = d1["Point Oriented"]["Inter-class"][kk][year][quarter].get(label, 0)
                        d1["Point Oriented"]["Inter-class"][kk][year][quarter][label] = round(100 * (prev_point_inter + value), 2)

                        # Intra-class
                        if "Intra-class" not in d1["Point Oriented"]:
                            d1["Point Oriented"]["Intra-class"] = {}
                        if year not in d1["Point Oriented"]["Intra-class"]:
                            d1["Point Oriented"]["Intra-class"][year] = {}
                        if quarter not in d1["Point Oriented"]["Intra-class"][year]:
                            d1["Point Oriented"]["Intra-class"][year][quarter] = {}
                        if label not in d1["Point Oriented"]["Intra-class"][year][quarter]:
                            d1["Point Oriented"]["Intra-class"][year][quarter][label] = {}

                        prev_point_intra = d1["Point Oriented"]["Intra-class"][year][quarter][label].get(kk, 0)
                        d1["Point Oriented"]["Intra-class"][year][quarter][label][kk] = round(100 * (prev_point_intra + value), 2)

                        # Initialize Change Oriented dictionaries
                        if "Change Oriented" not in d1:
                            d1["Change Oriented"] = {}

                        # Inter-class
                        if "Inter-class" not in d1["Change Oriented"]:
                            d1["Change Oriented"]["Inter-class"] = {}
                        if kk not in d1["Change Oriented"]["Inter-class"]:
                            d1["Change Oriented"]["Inter-class"][kk] = {}
                        if label not in d1["Change Oriented"]["Inter-class"][kk]:
                            d1["Change Oriented"]["Inter-class"][kk][label] = {}
                        if year not in d1["Change Oriented"]["Inter-class"][kk][label]:
                            d1["Change Oriented"]["Inter-class"][kk][label][year] = {}
                        if quarter not in d1["Change Oriented"]["Inter-class"][kk][label][year]:
                            d1["Change Oriented"]["Inter-class"][kk][label][year][quarter] = {}

                        prev_change_inter = d1["Change Oriented"]["Inter-class"][kk][label][year][quarter].get(label, 0)
                        d1["Change Oriented"]["Inter-class"][kk][label][year][quarter] = round(100 * (prev_change_inter + value), 2)

                        # Intra-class
                        if "Intra-class" not in d1["Change Oriented"]:
                            d1["Change Oriented"]["Intra-class"] = {}
                        if label not in d1["Change Oriented"]["Intra-class"]:
                            d1["Change Oriented"]["Intra-class"][label] = {}
                        if kk not in d1["Change Oriented"]["Intra-class"][label]:
                            d1["Change Oriented"]["Intra-class"][label][kk] = {}
                        if year not in d1["Change Oriented"]["Intra-class"][label][kk]:
                            d1["Change Oriented"]["Intra-class"][label][kk][year] = {}
                        if quarter not in d1["Change Oriented"]["Intra-class"][label][kk][year]:
                            d1["Change Oriented"]["Intra-class"][label][kk][year][quarter] = {}

                        prev_change_intra = d1["Change Oriented"]["Intra-class"][label][kk][year][quarter].get(label, 0)
                        d1["Change Oriented"]["Intra-class"][label][kk][year][quarter] = round(100 * (prev_change_intra + value), 2)

        for k in income.keys():
            if k == "Under $20,000":
                calc(k, "20000")
            elif k == "$300,000 or More":
                calc(k, "300000")
            elif k == "Number of Respondents":
                continue
            else:
                label = range_mean(k)
                calc(k, label)

        return d1
    
    return {
        "Household Income": income_refit(income),
        "Purpose": purpose_refit(purpose)
    }

data = excel_to_json("/home/amnesia/Documents/Projects/Active/HSTR/data/Working Data/ntto_survey_of_travel/archive/")

with open("/home/amnesia/Documents/Projects/Active/HSTR/data/Working Data/ntto_survey_of_travel/data.json","w") as f:
    json.dump(data_refit(data["Household Income"],data["Purpose"]),f,indent=4)
