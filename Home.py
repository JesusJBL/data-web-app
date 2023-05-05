"""
Name: Jesus Bautista Lopez
CS230: Section 1
Data: United States Mass Shooting
URL: TBD

Description: Final Project for CS 230, created a multipage web app based on a US Mass Shooting Data Set of 50. The
project uses bokeh, seaborne and matplotlib to create a line chart, relative plot and pie chart based on different ch-
aracteristics of the data.
"""

# Import packages
import streamlit as st
import pandas as pd
import numpy as np
import folium
import requests
from streamlit_folium import st_folium, folium_static
from streamlit_lottie import st_lottie


# Function to read in data and turn into a dataframe
def read_file():
    return pd.read_csv('Final Project/shootings.csv')


# Map detailing killings. This acts as my "summary".
def summary_map(df):
    m = folium.Map(location=[df.LATITUDE.mean(), df.LONGITUDE.mean()],
                   zoom_start=3, control_scale=True, tiles='Stamen Toner')
    for i, row in df.iterrows():
        NEW_LINE = '<br>'
        iframe = folium.IFrame(f'<b>Year</b>: {(row["YEAR"])}{NEW_LINE}<b>Location</b>: {(row["LOCATION"])}{NEW_LINE} '
                               f'<b>Summary</b>: {(row["SUMMARY"])}{NEW_LINE}'
                               f'<b>Weapon Bought In</b>: {(row["WHEREWEAPONOBTAINED"])}{NEW_LINE}<b>Type of Weapon</b>: '
                               f'{(row["TYPEOFWEAPONS"])}{NEW_LINE} '
                               f'<b>More Info</b>: {(row["SOURCES"])}')
        popup = folium.Popup(iframe, min_width=300, max_width=600)
        tooltip = row['CASE']
        if row['SHOOTINGTYPE'] == 'Mass':
            color = 'red'
        else:
            color = 'orange'

        folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']],
                      popup=popup, c=row['CASE'], tooltip=tooltip,
                      icon=folium.Icon(color=color, icon="screenshot")).add_to(
            m)

    folium_static(m, 1300)


# Map summarizing the killings by state
def state_map(df):
    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
    )
    state_geo = f"{url}/us-states.json"
    m = folium.Map(location=[df.LATITUDE.mean(), df.LONGITUDE.mean()],
                   zoom_start=3)

    choices = ['Total Victims', "Fatalities", 'Wounded']
    choice_made = st.selectbox("What statistics would you like to display?", choices)

    if choice_made == 'Total Victims':
        column = 'TOTALVICTIMS'
    elif choice_made == 'Fatalities':
        column = 'FATALITIES'
    elif choice_made == 'Wounded':
        column = 'WOUNDED'

    df = df.groupby("STATE").agg({"TOTALVICTIMS": np.sum, "FATALITIES": np.sum, "WOUNDED": np.sum})
    df = df.reset_index()
    cp = folium.Choropleth(
        geo_data=state_geo,
        name="choropleth",
        data=df,
        columns=["STATE", column],
        key_on="feature.properties.name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'{choice_made}',
        highlight=True
    ).add_to(m)

    folium.GeoJsonTooltip(['name']).add_to(cp.geojson)

    folium.LayerControl().add_to(m)

    folium_static(m, width=1300)


# Makes an animation, uses a default parameter and the lottie package.
def load_animation(url="https://assets1.lottiefiles.com/packages/lf20_uzkz8cdb.json"):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Streamlit
def main():
    dataframe = read_file()
    st.set_page_config(page_title="US Gun Violence Database", initial_sidebar_state="collapsed", layout="wide")
    with st.container():
        st.title("US Gun Violence Database")
        st.subheader("About")
        left_column, right_column = st.columns(2)
        with left_column:
            st.write(
                "Welcome to the US Gun Violence Database. This website showcases statistics for US Mass Shootings up "
                "until 2015 in order to raise awareness. If you'd like to donate click on the link below.")
            st.write("[Click Here to Donate](https://marchforourlives.com)")
        with right_column:
            st_lottie(load_animation(), height=250, key="No guns")
        st.divider()

    with st.container():
        st.header("Summary")

        pivot_map, pivot_info = st.tabs(['Map 1', 'Map 2'])
        with pivot_map:
            summary_map(dataframe)
            st.caption('This is a map that summarizes the key insights for every shooting in the dataset. Red '
                       'icons represent mass shootings while orange represents spree shootings.')

        with pivot_info:
            state_map(dataframe)
            st.write('This map summarizes key information of the dataset that the map does not cover'
                     ' focusing on total victims, total number of wounded and fatalities by state.')


main()
