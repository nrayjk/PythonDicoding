import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
def load_data():
    return pd.read_csv("Air Quality.csv")

# Load and cache the data
all_data = load_data()

# User inputs
station = st.selectbox('Select Station', all_data['station'].unique())
start_year, end_year = st.slider('Select Year Range', min_value=int(all_data['year'].min()), max_value=int(all_data['year'].max()), value=(2013, 2017))
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Filter the data based on selected station and year range
pollutant_data = all_data.groupby(['station', 'year'])[pollutants].mean()
station_data = pollutant_data.loc[station].loc[start_year:end_year].reset_index()

# Display the filtered data
st.dataframe(station_data)

# Plot pollutant levels
st.write(f"### Average Pollutant Levels at Station {station} ({start_year}-{end_year})")
plot_data = station_data.set_index('year')[pollutants]
st.line_chart(plot_data)

excluded_columns = st.multiselect('Exclude Columns for Correlation', ['DEWP', 'year', 'month', 'day', 'hour', 'RAIN', 'WSPM', 'wd_degrees', 'PRES'])
excluded_columns.append('station')

if 'TEMP' in all_data.columns:
    corr_temp = all_data.drop(columns=excluded_columns).corr()
    corr_temp_only = corr_temp['TEMP'].sort_values(ascending=False)

    st.write("### Histogram of Environmental Data Correlation with Temperature")
    st.bar_chart(corr_temp_only)
