# Import Packages
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns


# Function that reads in data
def read_file():
    return pd.read_csv('Final Project/shootings.csv')


# Function to filter the data to group by race and find the mean per race of total victims
def filter_data(df, values, mental_health):
    df = df[df['PRIORSIGNSOFMENTALILLNESS'] == mental_health]
    df = df[df['TOTALVICTIMS'] >= values[0]]
    df = df[df['TOTALVICTIMS'] <= values[1]]
    return df


# Function to make a relative plot
def rel_plot(df, sizes):
    df = df.rename(columns={"WOUNDED": "Wounded", "RACE": "Race", "GENDER": "Gender", "FATALITIES": "Fatalities"})
    sns.set_style('darkgrid')
    g = sns.relplot(data=df, x="Wounded", y="Fatalities", hue="Race", style="Gender", s=300
                    , legend="brief", markers=(u'$\u2642$', u'$\u2640$')).set(title='Total Victims per Race')
    # https://stackoverflow.com/questions/25590609/men-mars-and-female-venus-symbols-in-python, explains usage of
    # symbols.
    return g


# Function for pivot table to display value with top total victims
def max_pivot(df):
    table = pd.pivot_table(df, index=['RACE', 'GENDER'],
                           aggfunc={'TOTALVICTIMS': np.sum, 'WOUNDED': np.sum, 'FATALITIES': np.sum})
    table = table.reset_index()
    race = max(table['RACE'])
    gender = max(table['GENDER'])
    demographic = str(race) + ' ' + str(gender)
    total_victims = max(table['TOTALVICTIMS'])
    wounded = max(table['WOUNDED'])
    fatalities = max(table['FATALITIES'])
    return demographic, int(total_victims), int(wounded), int(fatalities)

# Streamlit
def main():
    df = read_file()
    demographic, victims, wounded, fatalities = max_pivot(df)
    st.title("Data by Assailant")
    st.write("This web app application looks specifically at data that characterizes the assailants whether that be"
             " through gender, race, signs of mental illness, etc.")
    st.divider()
    st.header("Scatter-plot")
    st.subheader(f"Most Repeated Demographic: :red[{demographic}]")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Victims", victims)
    col2.metric("Fatalities", fatalities)
    col3.metric("Wounded", wounded)

    with st.sidebar:
        st.header("Filters")
        mental_health = st.radio("Display assailants with previous signs of mental illness", ('Yes', 'No'))
        values = st.slider('Select a range of victims', 5.0, 70.0, (10.0, 30.0))

    filter_df = filter_data(df, values, mental_health)
    st.pyplot(rel_plot(filter_df, values))


main()
