# Import Packages
import streamlit as st
import pandas as pd
import datetime
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
import numpy as np



# Function that reads in data
def read_file():
    return pd.read_csv('Final Project/shootings.csv')


# Functions that filters data by year.
def filter_data(df, min_date, max_date):
    df['OLD_DATE'] = df['DATE']
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df[df['DATE'] >= min_date]
    df = df[df['DATE'] <= max_date]
    return df.sort_values('DATE', ascending=True)


# Function that makes the line chart
def make_line_chart(df, min_date, max_date, legal_list):
    p = figure(sizing_mode="stretch_width", )
    if len(legal_list) == 2:
        if legal_list[0] == "Yes":
            color_one = 'blue'
            label_one = 'Legal Weapon'
            color_two = 'red'
            label_two = 'Illegal Weapon'

        elif legal_list[1] == "Yes":
            color_one = 'red'
            label_one = 'Illegal Weapon'
            color_two = 'blue'
            label_two = 'Legal Weapon'

        df_one = df[df['WEAPONSOBTAINEDLEGALLY'] == legal_list[0]]
        df_two = df[df['WEAPONSOBTAINEDLEGALLY'] == legal_list[1]]
        source_one = ColumnDataSource(df_one)
        source_two = ColumnDataSource(df_two)
        p.line(x='YEAR', y='TOTALVICTIMS', source=source_one, color=color_one, legend_label=label_one, line_width=2)
        p.line(x='YEAR', y='TOTALVICTIMS', source=source_two, color=color_two, legend_label=label_two,
               line_width=2)
        p.circle(x='YEAR', y='TOTALVICTIMS', size='TOTALVICTIMS', fill_color=color_one, source=source_one, fill_alpha=
        0.5, line_color=color_one)
        p.circle(x='YEAR', y='TOTALVICTIMS', size='TOTALVICTIMS', fill_color=color_two, source=source_two, fill_alpha=
        0.5, line_color=color_two)


    else:
        df = df[df['WEAPONSOBTAINEDLEGALLY'].isin(legal_list)]
        source_one = ColumnDataSource(df)
        if legal_list == ["Yes"]:
            color_one = 'blue'
            label_one = 'Legal Weapon'

        else:
            color_one = 'red'
            label_one = 'Illegal Weapon'

        p.line(x='YEAR', y='TOTALVICTIMS', source=source_one, color=color_one, legend_label=label_one, line_width=2)
        p.circle(x='YEAR', y='TOTALVICTIMS', size='TOTALVICTIMS', fill_color=color_one, source=source_one, fill_alpha=
        0.5, line_color=color_one)

    p.title.text = f"Number of Total Victims between {min_date} and {max_date}"
    p.title.text_font_size = "20px"
    p.title.align = "center"
    p.xaxis.axis_label = 'Years'
    p.yaxis.axis_label = 'Number of Total Victims'
    p.legend.location = "top_left"
    p.legend.title = "Weapons Obtained"
    p.legend.border_line_width = 2
    p.legend.border_line_color = "grey"

    hover = HoverTool()
    hover.tooltips = [
        ('Case', '@CASE'),
        ('Date of Shooting', '@OLD_DATE'),
        ('Total Victims', '@TOTALVICTIMS')
    ]

    p.add_tools(hover)
    return p

# Pivot table with max total victims and corresponding values to display as metric
def max_pivot(df):
    table = pd.pivot_table(df, index=['YEAR'],
                           aggfunc={'TOTALVICTIMS': np.sum, 'WOUNDED': np.sum, 'FATALITIES': np.sum})
    table = table.reset_index()
    total_victims = max(table['TOTALVICTIMS'])
    table = table.loc[table['TOTALVICTIMS'] == total_victims]
    return table['YEAR'].iloc[0], table['TOTALVICTIMS'], table['WOUNDED'], table['FATALITIES']


# Streamlit
def main():
    df = read_file()
    time, victims, wounded, fatalities = max_pivot(df)
    st.title('Data by Time')
    st.write("This web app application showcases mass shootings over time based on the number of weapons and whether"
             "the assailant obtained their weapon legally or not.")
    st.divider()
    st.header('Line Chart')
    st.subheader(f"Most Repeated Year: :red[{time}]")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Victims", victims)
    col2.metric("Fatalities", fatalities)
    col3.metric("Wounded", wounded)
    with st.sidebar:
        st.header("Filters")
        st.subheader('Choose a Timeframe')
        start_date = st.date_input("Enter the starting date you'd like to search for data",
                                   value=datetime.datetime(1982, 8, 20),
                                   min_value=datetime.datetime(1982, 8, 20), max_value=
                                   datetime.datetime(2015, 7, 16))
        end_date = st.date_input("Enter the ending date you'd like to search for data",
                                 value=datetime.datetime(2015, 7, 16),
                                 min_value=datetime.datetime(1982, 8, 20), max_value=
                                 datetime.datetime(2015, 7, 16))
        st.subheader("Choose Weapon Legality")
        answer = st.multiselect("Did the Assailant obtain their weapon legally:", ["Yes", "No"])

    filter_df = filter_data(df, pd.to_datetime(start_date), pd.to_datetime(end_date))
    st.bokeh_chart(make_line_chart(filter_df, start_date, end_date, answer), use_container_width=True)
    st.write()
main()
