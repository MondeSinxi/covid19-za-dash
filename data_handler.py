import pandas as pd
from pathlib import Path

DATA_PATH = Path("covid19za/data")

CATEGORIES = ["confirmed", "recoveries", "deaths", "testing", "vaccination"]

def get_covid19_data(categories: list) -> dict:
    DATA = {}
    for data_type in categories:
        file_path = DATA_PATH / f"covid19za_provincial_cumulative_timeline_{data_type}.csv"
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        # df['daily_value'] = df.total.diff()
        DATA[data_type] = {"path": file_path, "data": df}
    return DATA

def to_long_form(df: pd.DataFrame, id_vars: list = ['date'], value_vars=['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'MP', 'WC', 'total']) -> pd.DataFrame:
    return pd.melt(df, id_vars=id_vars, value_vars=value_vars)

if __name__ == "__main__":
    print(get_covid19_data(CATEGORIES))