import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
from types import SimpleNamespace


HOSPITALISATION_DATA = Path('nicd_hospitalisation.csv')

DATA_PATH = Path("covid19za/data/")
DEATHS_PATH = DATA_PATH / "covid19za_provincial_cumulative_timeline_deaths.csv"
CASES_PATH = DATA_PATH / "covid19za_provincial_cumulative_timeline_confirmed.csv"
PROVINCE_MAPPING = {"Eastern Cape": "EC", "Free State": "FS", "Gauteng": "GP",
                    "KwaZulu-Natal": "KZN", "Limpopo": "LP",
                    "Mpumalanga": "MP", "Northern Cape": "NC", "North West": "NW",
                    "Western Cape": "WC", "Total": "total"}


def extract_data(data_file_path, date_column_name="date", date_format="%d-%m-%Y"):
    """ Read csv file and return dataframe"""
    df = pd.read_csv(data_file_path)
    df[date_column_name] = pd.to_datetime(df[date_column_name], format=date_format)
    return df.sort_values(by=date_column_name)

def plot_two_charts(data_1, data_2):
    """Plot to graphs on a single chart"""
    graph_1 = alt.Chart(data_1.data).mark_area(opacity=0.3, color='green').encode(
        alt.X(data_1.X), alt.Y(data_1.Y)).interactive()

    graph_2 = alt.Chart(data_2.data).mark_area(opacity=0.3, color='red').encode(
        alt.X(data_2.X), alt.Y(data_2.Y)).interactive()

    layered_chart = alt.layer(graph_1, graph_2)
    return st.altair_chart(layered_chart, use_container_width=True)

st.title('COVID-19 Dashboard')

########## Plot hospitalisation data ##################################
st.write('Confirmed Cases and Hospitalisation Data')

df_hosp = extract_data(HOSPITALISATION_DATA, date_format="%Y-%m-%d")
df_cases = extract_data(CASES_PATH)

# select a province
selection = st.selectbox("Select Province", df_hosp.province.unique(),
                         index=0, help="select national or provincial data")

province_code = PROVINCE_MAPPING[selection]

# filter for current selection
df_hosp_selection = df_hosp[df_hosp["province"] == selection]

df_cases_selection = df_cases[["date", province_code]]

# get daily cases
df_cases_selection["cases"] = df_cases_selection[[province_code]].diff()

data_1 = {'data': df_hosp_selection, 'X': 'date:T', 'Y':  'currently_admitted'}
data_2 = {'data': df_cases_selection, 'X': 'date:T', 'Y': 'cases'}

plot_two_charts(SimpleNamespace(**data_1), SimpleNamespace(**data_2))


#########################################################################
