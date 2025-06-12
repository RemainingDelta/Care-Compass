import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import numpy as np
import json
import plotly.express as px

st.set_page_config(layout="wide")

from modules.style import style_sidebar, set_background
style_sidebar()


# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("COUNTRY COMPARATOR")
st.write("")
st.write("")

headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}


# Your backend endpoint URL
country_url = "http://host.docker.internal:4000/country/countries"  

country_list = []
country_code_list = []
country3_list = ["N/A"]

try:
    response = requests.get(country_url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    country_list = [item["name"] for item in data]
    code_list = [item["code"] for item in data]
    country_code_list = [item['name'] + '-' + item['code'] for item in data]

    country3_list += country_code_list

    print("Countries:", country_list)


except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)


# CHOOSE COUNTRIES
st.subheader("Select countries for comparison")
features = []
col1, col2, col3 = st.columns(3)

with col1:
    country1 = st.selectbox(
        "Country 1:",
        country_code_list,
        index=None,
        placeholder="Select Country 1 ..."
    )

with col2: 
    country2 = st.selectbox(
        "Country 2:",
        country_code_list,
        index=None,
        placeholder="Select Country 2 ..."
    )

with col3: 
    country3 = st.selectbox(
            "Country 3:",
            country3_list,
            index=None,
            placeholder="Select Country 3 ..."
    )
    if country3 == "N/A":
        country3_status = False
    else:
        country3_status = True

st.write("")
st.write("")

#handles getting the country code needed for accessing each dataset 
if country1 :
    start_index = (str(country1)).index('-') + 1
    country1 = country1[start_index:]
else:
    st.info("Please select a country to proceed")

if country2 :
    start_index = (str(country2)).index('-') + 1
    country2 = country2[start_index:]

if country3 and country3_status :
    start_index = (str(country3)).index('-') + 1
    country3 = country3[start_index:]

table = st.button("Submit", type="primary", use_container_width=True)


# TABLE FOR THREE COUNTRIES 
countries = [country1, country2, country3]
#st.write(countries)
countries_exist = []
for item in countries:
    if item:
        countries_exist.append(item)
#st.write(countries_exist)
#st.write(len(countries_exist))

if table:
    master_df = pd.DataFrame()

    for country in countries:
        try:
            headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            countryurl = f"http://host.docker.internal:4000/country/features/{country}"
            response = requests.get(countryurl)

            if response.status_code == 200:
                data_dict = response.json()

                # Debug step — see what the API returned
                # st.write(f"Raw API response for {country}:", data_dict)

                # flatten dictionary row
                flat_row = {}
                flat_row["Country"] = country

                for feature_name, feature_values in data_dict.items():
                    for k,v in feature_values.items():
                        flat_row[f"{feature_name}"] = v
          
                df = pd.DataFrame([flat_row])

                
                master_df = pd.concat([master_df, df], ignore_index=True)

            else:
                if country3_status == True:
                    st.error(f"Failed to fetch data for country: {country} (status code {response.status_code})")
                

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {countryurl}")



# TABLE

life_expectancy = "Life Expectancy (years)"
inf_mortality = "Infant Mortality Rate (%)"
live_births = "Live Births per 1000 Population"
gen_practitioners = "General Practitioners per 10,000 Population"
health_expend = "Total Health Expenditure per Capita"
impov_house = "Impoverished Households due to out-of-pocket healthcare payments"

features = [live_births,gen_practitioners,health_expend]

if table:
    if country1 == country2 or country1 == country3 or country2 == country3:
        st.badge(f"You chose the same country for comparison. Please try again.", color='red')

    else:
        st.write("")
        st.write("")
        st.write("")
        st.dataframe(master_df,hide_index=True)
        st.caption("*General Practitioners per 10,000 Population")
        st.caption("** Total Health Expenditure per Capita")
        st.caption("+Impoverished Households due to out-of-pocket healthcare payments")
        st.caption("++ Live Births per 1000 Population")


st.write("")
st.write("")



# TRACK FEATURE OVER TIME
st.subheader("Track a feature over time")
st.write("")

col7, col3 = st.columns([0.7,0.3], gap="large", vertical_alignment="bottom")


with col7:
    feature = st.selectbox(
                "Select Feature:",
                features,
                index=None
            )

with col3:
    plot = st.button("Plot", type="primary",use_container_width=False)

if plot:
    def display_data(data_code, y_value, title, countries_exist):
        dataframe_list = []
        for chosen_country in countries_exist:
            #st.write(countries_exist)
            get_graph = f"http://web-api:4000/ml/ml/get_autoregressive/{chosen_country}/{data_code}/2035"
            #headers = {
                #"User-Agent": "Python/requests",
                #"Accept": "application/json",
                #"Content-Type": "application/json"
                #}
            all_countries = requests.get(get_graph, timeout=10)
            #print(all_countries.type())
            all_country = requests.get(get_graph, timeout=10).text
            #st.write(all_country)
            if all_countries.status_code == 200:
                #all_countries = all_countries.json
                #all_countries = json.dumps(all_countries)
                data_dict = json.loads(all_country)
                data_dict = json.loads(data_dict)
                #print(type(data_dict))

                #data_series = pd.Series(all_countries)
                #print(all_countries)
                #st.write(type(data_dict))
                df_country = pd.DataFrame(data_dict)
                #df_graph = pd.concat([df_graph, data_dict.to_frame().T], ignore_index=True)
                #print(df_graph)
                df_graph = df_country #[(df_country['country'] == chosen_country)]
                df_graph['COUNTRY'] = chosen_country
                #print("individual dataframe length")
                #st.write(type(df_graph))
                dataframe_list.append(df_graph)
            else:
                st.error(f"Error: {all_countries.status_code}")
                st.write(all_countries.text)
        df_graph = pd.concat(dataframe_list, ignore_index=True)
        #print(df_graph)
        df_graph['YEAR'] = df_graph['YEAR'].astype(float)
        #X = np.array(df_graph['YEAR'])
        #y = np.array(df_graph['VALUE']) 
                #predict_dict = json.loads(response_text)
                #slope = predict_dict['slope']
                #intercept = predict_dict['intercept']
                
        #x = np.array(X).ravel()
        #y = np.array(y).ravel()
        #st.write(df_graph.dtypes)
        #st.write(df_graph)
        st.plotly_chart(px.line(df_graph, x='YEAR', y='VALUE', labels={
                "x": "Time in Years",
                "y": y_value}, color = 'COUNTRY', title = title))
    if feature == live_births:
        st.subheader("Here are the projected live birth numbers for your compared countries up to 2035:")
        display_data("HFA_16", "Live Births per 1000 population", "Live Births Over Time", countries_exist)

    if feature == gen_practitioners: 
        st.subheader("Here are the projected general practitioner numbers for your compared countries up to 2035:")
        display_data("HLTHRES_67", "General Practitoners per 10,000 population", "General Practitioners Over Time", countries_exist)  

    if feature == health_expend:
        st.subheader("Here are the projected expenditures for your compared countries up to 2035:")
        display_data("HFA_570", "Total Health Expenditure per Capita", "Total Health Expenditure Over Time", countries_exist)  

    #results = requests.get(f"http://web-api:4000/ml/predict/{feature}/{country1}") # need to do more for the other countries
    #json_results = results.json()
    #st.dataframe(json_results)


    