import pandas as pd
from pathlib import Path

DATA_PATH = Path("covid19za/data")

CATEGORIES = ["confirmed", "recoveries", "deaths", "testing", "vaccination"]

def get_covid19_data(categories) -> dict:
    DATA = {}
    for data_type in categories:
        file_path = DATA_PATH / f"covid19za_provincial_cumulative_timeline_{data_type}.csv"
        df = pd.read_csv(file_path)
        df.date = pd.to_datetime(df.date)
        DATA[data_type] = {"path": file_path, "data": df}
    return DATA

if __name__ == "__main__":
    print(get_covid19_data(CATEGORIES))