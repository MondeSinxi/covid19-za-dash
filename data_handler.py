import pandas as pd
from pathlib import Path

DATA_PATH = Path("covid19za/data/")

HOSPITALISATION_DATA = Path('nicd_hospitalisation.csv')

DEATHS_PATH = DATA_PATH / "covid19za_provincial_cumulative_timeline_deaths.csv"

CASES_PATH = DATA_PATH / "covid19za_provincial_cumulative_timeline_confirmed.csv"

PROVINCE_MAPPING = {"Eastern Cape": "EC", "Free State": "FS", "Gauteng": "GP",
                    "KwaZulu-Natal": "KZN", "Limpopo": "LP",
                    "Mpumalanga": "MP", "Northern Cape": "NC", "North West": "NW",
                    "Western Cape": "WC", "Total": "total"}

PROVINCE_CODE_MAPPING = {"EC": "Eastern Cape", "FS": "Free State", "GP": "Gauteng",
                    "KZN": "KwaZulu-Natal", "LP": "Limpopo",
                    "MP": "Mpumalanga", "NC": "Northern Cape", "NW": "North West",
                    "WC": "Western Cape", "total": "Total"}

def extract_data(data_file_path, date_column_name="date", date_format="%d-%m-%Y"):
    """ Read csv file and return dataframe"""
    df = pd.read_csv(data_file_path)
    df[date_column_name] = pd.to_datetime(df[date_column_name], format=date_format)
    return df.sort_values(by=date_column_name)

def make_covid19za_data_long(data_path, type=None):
    df_1 = extract_data(data_path)
    df = df_1[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'total']].diff()
    df["date"] = df_1["date"]
    df['type'] = type
    return df

def concat_long_covid19_za_data(data_frames: list[pd.DataFrame]):
    df = pd.concat(data_frames)
    df = df.melt(id_vars=['date', 'type'], value_vars=['total', 'EC', 'FS',  'GP', 'KZN', 'LP',  'MP', 'NC', 'NW', 'WC'])
    df["variable"] = df.variable.apply(lambda x: PROVINCE_CODE_MAPPING[x])
    return df

df_hosp = extract_data(HOSPITALISATION_DATA, date_format="%Y-%m-%d")

df_cases = make_covid19za_data_long(CASES_PATH, type='cases')

df_deaths = make_covid19za_data_long(DEATHS_PATH, type='deaths')

df = concat_long_covid19_za_data([df_cases, df_deaths])

df_hosp_melt = df_hosp.melt(id_vars=['date', 'province'], value_vars=['currently_admitted', 'current_in_icu'])
df_hosp_melt.columns = ['date', 'variable', 'type', 'value']

data = pd.concat([df,df_hosp_melt])