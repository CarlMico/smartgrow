import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Fetch JSON data from the API
@st.cache_data
def fetch_data(results):
    url = f"https://api.thingspeak.com/channels/2492394/feeds.json?key=ZB0QBIOG587X9V41&results={results}"
    response = requests.get(url)
    return response.json()

# Extract relevant data from JSON
def extract_data(data):
    feeds = data['feeds']
    timestamps = [feed['created_at'] for feed in feeds]
    moistures = [float(feed['field1']) if feed['field1'] is not None else None for feed in feeds]
    temperatures = [float(feed['field2']) if feed['field2'] is not None else None for feed in feeds]
    humidities = [float(feed['field3']) if feed['field3'] is not None else None for feed in feeds]
    return pd.DataFrame({'Timestamp': timestamps, 'Moisture': moistures, 'Temperature': temperatures, 'Humidity': humidities})

# Line Chart
def plot_chart(df):
    st.write("### Sensor Data")
    chart = alt.Chart(df).transform_fold(
        ['Moisture', 'Temperature', 'Humidity'],
        as_=['Sensor', 'Value']
    ).mark_line(point=True).encode(
        x='Timestamp:T',
        y='Value:Q',
        color='Sensor:N',
        tooltip=['Timestamp:T', 'Value:Q', 'Sensor:N']
    ).properties(
        width=600,
        height=400
    ).interactive()

    # Move legend to the bottom
    chart = chart.configure_legend(
        orient='bottom'
    )

    st.altair_chart(chart)

# Main function
def main():
    # Dropdown for selecting number of data points
    number_of_data = st.selectbox("Select number of data points", [5, 10, 15, 20], index=0)

    # Fetch data
    data = fetch_data(number_of_data)

    # Extract and process data
    df = extract_data(data)

    # Plot the chart
    plot_chart(df)

if __name__ == "__main__":
    main()
