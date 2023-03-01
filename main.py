import streamlit as st
import pandas as pd
import plotly.express as px
import os


def concat_data(country):
    data = pd.DataFrame()
    if len(country) > 0:
        for i in range(len(country)):
            df1 = population[population['Entity'] == country[i]].dropna()
            df2 = co2_emissions[co2_emissions['Entity'] == country[i]].dropna()
            # df2['Population'] = df1['Population'].where(df1['Year'].equals(df2['Year']))
            df2 = pd.merge(df1, df2, left_on='Year_Pop', right_on='Year', how='right').drop('Year_Pop', axis=1)
            print(df2)
            # df2['Per Capita CO2 Emissions'] = df2['Annual CO2 emissions']/df1['Population'].where(df2['Year'].reset_index(drop=True) == df1['Year'].reset_index(drop=True))
            data = data.append(df2)
            print(data)
    return data


if __name__ == '__main__':
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    dir_of_interest = os.path.join(FILE_DIR, "Resources")
    emissions_path = os.path.join(dir_of_interest, "annual-co2-emissions-per-country.csv")
    population_path = os.path.join(dir_of_interest, "population.csv")
    st.set_page_config(layout="wide")
    st.title(":red[Carbon Dioxide] Emissions")
    st.subheader("*CO2 Data Explorer*")
    co2_emissions = pd.read_csv(emissions_path)
    population = pd.read_csv(population_path)
    st.dataframe(co2_emissions)
    del co2_emissions['Code']

    st.header("Per Capita CO2 Emissions")
    text = """<p style="font-family:sans-serif; font-size: 16px;">CO2 emissions per capita measure the average annual emissions per person for a country or region. It is calculated by dividing the total annual emissions of the
    country or region by its total population. The source for the annual CO2 emissions data is the Global Carbon Project.</p>"""
    st.markdown(text, unsafe_allow_html=True)
    st.subheader("Select multiple entities to compare the CO2 Emissions")

    country = st.multiselect("Select any Entity: ", co2_emissions['Entity'].unique())
    data = concat_data(country)
    col1, col2 = st.columns(2)
    # print(data)
    if len(data) > 0:
        data['CO2 emissions (in Mtonnes)'] = data['Annual CO2 emissions']/1000000
        fig = px.line(data, x="Year", y="CO2 emissions (in Mtonnes)", color='Entity_x', title="Annual CO2 Emissions")
        col1.plotly_chart(fig, use_container_width=True)

        data['Per Capita CO2 emissions'] = data['Annual CO2 emissions'] / data['Population']
        fig = px.line(data, x="Year", y="Per Capita CO2 emissions", color='Entity_x', title='Per Capita CO2 Emissions')
        col2.plotly_chart(fig, use_container_width=True)
