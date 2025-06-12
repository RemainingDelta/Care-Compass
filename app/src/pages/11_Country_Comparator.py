import logging
import decimal

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import numpy as np
import json
import plotly.express as px
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import plotly.graph_objects as go
from contextlib import contextmanager
from modules.style import style_sidebar


st.set_page_config(layout="wide")

from modules.style import style_sidebar, set_background
style_sidebar()


# Constants for feature configurations
FEATURES = {
    "live_births": {
        "code": "HFA_16",
        "title": "Live Births Over Time",
        "y_label": "Live Births per 1000 population"
    },
    "general_practitioners": {
        "code": "HLTHRES_67",
        "title": "General Practitioners Over Time",
        "y_label": "General Practitioners per 10,000 population"
    },
    "health_expenditure": {
        "code": "HFA_570",
        "title": "Total Health Expenditure Over Time",
        "y_label": "Total Health Expenditure per Capita"
    }
}

@contextmanager
def get_session():
    """Create a fresh session for each request"""
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    try:
        yield session
    finally:
        session.close()

def fetch_countries(url):
    """Fetch country data from API"""
    with get_session() as session:
        logger.info(f"Attempting to connect to {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return [item["name"] for item in data], [item["code"] for item in data], [f"{item['name']}-{item['code']}" for item in data]

feature2 = []

def display_data(data_code, y_value, title, countries_exist, chosen_year):

    dataframe_list = []
    for chosen_country in countries_exist:
        api_url = f"http://web-api:4000/ml/ml/get_autoregressive/{chosen_country}/{data_code}/{chosen_year}"
        logger.info(f"Attempting to fetch data from: {api_url}")
        
        try:
            with get_session() as session:
                response = session.get(api_url, timeout=30, headers={'Accept': 'application/json'})
                logger.info(f"API response status code: {response.status_code}")
                
                if response.status_code != 200:
                    st.error(f"API returned status code {response.status_code}")
                    return
                
                data = response.json()
                if isinstance(data, str):
                    data = json.loads(data)
                
                df_country = pd.DataFrame(data)
                df_graph = df_country #[(df_country['country'] == chosen_country)]
                df_graph['COUNTRY'] = chosen_country
                dataframe_list.append(df_graph)
            
                
        except Exception as e:
            logger.error(f"Error fetching/processing data: {str(e)}")
            st.error(f"Failed to process data: {str(e)}")
    df_graph = pd.concat(dataframe_list, ignore_index=True)
    df_graph['YEAR'] = df_graph['YEAR'].astype(float)
            
    st.plotly_chart(px.line(df_graph, x='YEAR', y='VALUE', labels={
                "x": "Time in Years",
                "y": y_value}, color = 'COUNTRY', title = title))


# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("COUNTRY COMPARATOR")
st.write("")
st.write("")



country3_list = ["N/A"]

# Fetch Countries
try:
    country_list, code_list, country_code_list = fetch_countries("http://web-api:4000/country/countries")
except Exception as e:
    logger.error(f"Failed to fetch countries: {str(e)}")
    st.error("Failed to load country data. Please try again later.")
    country_list, code_list, country_code_list = [], [], []

country3_list += country_code_list


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


if table:
    master_df = pd.DataFrame()

    for country in countries:
        try:
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
    if feature == live_births:
        feature2 = FEATURES["live_births"]
        st.subheader("Here are the projected live birth numbers for your compared countries up to 2035:")
        #display_data("HFA_16", "Live Births per 1000 population", "Live Births Over Time", countries_exist)

    if feature == gen_practitioners: 
        feature2 = FEATURES["general_practitioners"]
        st.subheader("Here are the projected general practitioner numbers for your compared countries up to 2035:")
        #display_data("HLTHRES_67", "General Practitoners per 10,000 population", "General Practitioners Over Time", countries_exist)  

    if feature == health_expend:
        feature2 = FEATURES["health_expenditure"]
        st.subheader("Here are the projected expenditures for your compared countries up to 2035:")
        #display_data("HFA_570", "Total Health Expenditure per Capita", "Total Health Expenditure Over Time", countries_exist)  
    if len(feature2) != 0:
        display_data(feature2["code"], feature2["y_label"], feature2["title"], 
                        countries_exist, 2035)
    #results = requests.get(f"http://web-api:4000/ml/predict/{feature}/{country1}") # need to do more for the other countries
    #json_results = results.json()
    #st.dataframe(json_results)


    