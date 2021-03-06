import pandas as pd
from pathlib import Path

DATA_PATH = Path("covid19za/data/")

HOSPITALISATION_DATA = Path("nicd_hospitalisation.csv")

DEATHS_PATH = DATA_PATH / "covid19za_provincial_cumulative_timeline_deaths.csv"

CASES_PATH = DATA_PATH / "covid19za_provincial_cumulative_timeline_confirmed.csv"

PROVINCE_MAPPING = {
    "Eastern Cape": "EC",
    "Free State": "FS",
    "Gauteng": "GP",
    "KwaZulu-Natal": "KZN",
    "Limpopo": "LP",
    "Mpumalanga": "MP",
    "Northern Cape": "NC",
    "North West": "NW",
    "Western Cape": "WC",
    "Total": "total",
}

PROVINCE_CODE_MAPPING = {
    "EC": "Eastern Cape",
    "FS": "Free State",
    "GP": "Gauteng",
    "KZN": "KwaZulu-Natal",
    "LP": "Limpopo",
    "MP": "Mpumalanga",
    "NC": "Northern Cape",
    "NW": "North West",
    "WC": "Western Cape",
    "total": "Total",
}

PROVINCE_CODES = list(PROVINCE_CODE_MAPPING.keys())


def extract_data(data_file_path, date_column_name="date", date_format="%d-%m-%Y"):
    """Read csv file and return dataframe"""
    df = pd.read_csv(data_file_path)
    df[date_column_name] = pd.to_datetime(df[date_column_name], format=date_format)
    return df.sort_values(by=date_column_name)


def make_covid19za_data_long(data_path, type=None):
    """ " Convert data from wide to long form"""
    df_extract = extract_data(data_path)
    if "daily" in type:
        df = df_extract[PROVINCE_CODES].diff()
    elif "average" in type:
        df = df_extract[PROVINCE_CODES].diff()
        df = df.rolling(7).mean().round(0)
    else:
        df = df_extract[PROVINCE_CODES]
    df["date"] = df_extract["date"]
    df["type"] = type
    return df


def concat_long_covid19_za_data(data_frames: list[pd.DataFrame]):
    df = pd.concat(data_frames)
    df = df.melt(id_vars=["date", "type"], value_vars=PROVINCE_CODES)
    df["variable"] = df.variable.apply(lambda x: PROVINCE_CODE_MAPPING[x])
    return df


df_hosp = extract_data(HOSPITALISATION_DATA, date_format="%Y-%m-%d")
df_hosp_melt = df_hosp.melt(
    id_vars=["date", "province"], value_vars=["currently_admitted", "current_in_icu"]
)
df_hosp_melt.columns = ["date", "variable", "type", "value"]

df_daily_cases = make_covid19za_data_long(CASES_PATH, type="daily_cases")
df_cummulative_cases = make_covid19za_data_long(CASES_PATH, type="cummulative_cases")
df_average_cases = make_covid19za_data_long(CASES_PATH, type="average_cases")

df_daily_deaths = make_covid19za_data_long(DEATHS_PATH, type="daily_deaths")
df_cummulative_deaths = make_covid19za_data_long(DEATHS_PATH, type="cummulative_deaths")
df_average_deaths = make_covid19za_data_long(DEATHS_PATH, type="average_deaths")


df = concat_long_covid19_za_data(
    [
        df_daily_cases,
        df_daily_deaths,
        df_cummulative_cases,
        df_cummulative_deaths,
        df_average_cases,
        df_average_deaths,
    ]
)

data = pd.concat([df, df_hosp_melt])
