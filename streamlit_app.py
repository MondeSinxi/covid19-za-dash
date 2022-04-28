import streamlit as st
import pandas as pd
import altair as alt

from data_handler import data


def extract_data(data_file_path, date_column_name="date", date_format="%d-%m-%Y"):
    """Read csv file and return dataframe"""
    df = pd.read_csv(data_file_path)
    df[date_column_name] = pd.to_datetime(df[date_column_name], format=date_format)
    return df.sort_values(by=date_column_name)


def format_name(s):
    return s.replace("_", " ").capitalize()


st.title("COVID-19 Dashboard")

# select a province
province_selection = st.selectbox(
    "Select Province",
    data.variable.unique(),
    index=0,
    help="select national or provincial data",
)


type_selection = st.multiselect(
    "Select data type",
    data.type.unique(),
    default=None,
    format_func=format_name,
    help="select type of data to display",
)

# Filter
filtered_data = data[
    (data["type"].isin(type_selection)) & (data["variable"] == province_selection)
]

# Plot
area_chart = (
    alt.Chart(filtered_data)
    .mark_area(opacity=0.3)
    .encode(x="date:T", y=alt.Y("value:Q", stack=None), color="type:N")
)

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(
    type="single", nearest=True, on="mouseover", fields=["date"], empty="none"
)


# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = (
    alt.Chart(filtered_data)
    .mark_point()
    .encode(
        x="date:T",
        opacity=alt.value(0),
    )
    .add_selection(nearest)
)


# Draw a rule at the location of the selection
rules = (
    alt.Chart(filtered_data)
    .mark_rule(color="gray")
    .encode(
        x="date:T",
    )
    .transform_filter(nearest)
)

# Draw points on the line, and highlight based on selection
points = area_chart.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = area_chart.mark_text(align="left", dx=5, dy=-5).encode(
    text=alt.condition(nearest, "value:Q", alt.value(" "))
)

# Put the five layers into a chart and bind the data
layered_chart = (
    alt.layer(area_chart, selectors, points, rules, text)
    .encode(tooltip=["date"])
    .interactive()
)

# Plot the chart
st.altair_chart(layered_chart, use_container_width=True)
