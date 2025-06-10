import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import numpy as np
import json

st.set_page_config(layout="wide")

from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")


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
    st.info("Please select countries to proceed.")

if country2 :
    start_index = (str(country2)).index('-') + 1
    country2 = country2[start_index:]

if country3 and country3_status :
    start_index = (str(country3)).index('-') + 1
    country3 = country3[start_index:]

table = st.button("Submit", type="primary")


# TABLE FOR THREE COUNTRIES 
countries = [country1, country2, country3]

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
if table:
    if country1 == country2 or country1 == country3 or country2 == country3:
        st.badge(f"You chose the same country for comparison. Please try again.", color='red')

    else:
        st.write("")
        st.dataframe(master_df)
        st.write("*General Practitioners per 10,000 Population")
        st.write("** Total Health Expenditure per Capita")
        st.write("+Impoverished Households due to out-of-pocket healthcare payments")
        st.write("++ Live Births per 1000 Population")


st.write("")
st.write("")

life_expectancy = "Life Expectancy (years)"
inf_mortality = "Infant Mortality Rate (%)"
live_births = "Live Births per 1000 Population"
gen_practitioners = "General Practitioners per 10,000 Population"
health_expend = "Total Health Expenditure per Capita"
impov_house = "Impoverished Households due to out-of-pocket healthcare payments"

features = [life_expectancy,inf_mortality,live_births,gen_practitioners,health_expend,impov_house]

# TRACK FEATURE OVER TIME
feature = st.selectbox(
            "Track a feature over time:",
            features,
            index=None,
            placeholder="Select Feature ..."
        )
st.write("Tracking %s over time" %feature)
st.write("")
plot = st.button("Plot", type="primary")

if plot:
    results = requests.get(f"http://web-api:4000/ml/predict/{feature}/{country1}") # need to do more for the other countries
    json_results = results.json()
    st.dataframe(json_results)