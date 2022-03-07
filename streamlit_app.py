import streamlit as st
import pandas as pd
import altair as alt

from data_handler import data

def extract_data(data_file_path, date_column_name="date", date_format="%d-%m-%Y"):
    """ Read csv file and return dataframe"""
    df = pd.read_csv(data_file_path)
    df[date_column_name] = pd.to_datetime(df[date_column_name], format=date_format)
    return df.sort_values(by=date_column_name)

def format_name(s):
    return s.replace('_', " ").capitalize()

st.title('COVID-19 Dashboard')

# select a province
province_selection = st.selectbox("Select Province", data.variable.unique(),
                         index=0, help="select national or provincial data")


type_selection = st.multiselect("Select data type", data.type.unique(), default=None,
                           format_func = format_name,
                           help="select type of data to display")

# filter
filtered_data = data[(data["type"].isin(type_selection)) & (data["variable"] == province_selection)]

chart = alt.Chart(filtered_data).mark_area(opacity=0.3).encode(
    x="date:T",
    y=alt.Y("value:Q", stack=None),
    color="type:N"
).interactive()

st.altair_chart(chart, use_container_width=True)