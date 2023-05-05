# Import Packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Function that reads in data
def read_file():
    return pd.read_csv('Final Project/shootings.csv')


# Function that filters data based on the states you'd like to show
def filter_data(df, state_list):
    df = df[df['STATE'].isin(state_list)]
    return df


def shooting_frequency(df, state_list):
    freq = [len(df[df['STATE'] == state]) for state in state_list]
    return freq


def make_pie_chart(freq, state_list):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Create a list to separate state with most shootings dynamically
    explode = [0 for i in range(len(freq))]
    if len(freq) > 0:
        max_num = max(freq)
        max_index = freq.index(max_num)
        explode[max_index] = 0.25

    wedges, texts, autotexts = ax.pie(freq, labels=state_list, autopct='%1.1f%%', explode=explode,
                                      wedgeprops=dict(edgecolor='k', linewidth=1, linestyle='solid', alpha=0.7,
                                                      width=0.5))
    ax.legend(wedges, state_list,
              title="States",
              loc="lower left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title(f"Donut Chart Showing Frequency of Mass Shootings in {', '.join(state_list)}", y=1.05)
    ax.set_facecolor('#F5F5F5')
    return plt


def max_pivot(df):
    table = pd.pivot_table(df, index=['STATE'],
                           aggfunc={'TOTALVICTIMS': np.sum, 'WOUNDED': np.sum, 'FATALITIES': np.sum})
    table = table.reset_index()
    total_victims = max(table['TOTALVICTIMS'])
    table = table.loc[table['TOTALVICTIMS'] == total_victims]
    return table['STATE'].iloc[0], table['TOTALVICTIMS'], table['WOUNDED'], table['FATALITIES'], table


# Main function has all the streamlit code needed
def main():
    df = read_file()
    state, victims, wounded, fatalities, table = max_pivot(df)
    with st.sidebar:
        states = st.multiselect("Pick the states you'd like to display", df['STATE'])
    st.title("US Gun Violence Database")
    st.header("Data by Geographics")
    st.write("This data web application showcases the amount of mass murders in chosen states as well as location type"
             " within those same states")
    st.subheader(f"Most Repeated State: :red[{state}]")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Victims", victims)
    col2.metric("Fatalities", fatalities)
    col3.metric("Wounded", wounded)
    filter_df = filter_data(df, states)
    frequency = shooting_frequency(filter_df, states)
    pie = make_pie_chart(frequency, states)
    st.pyplot(pie)


main()
