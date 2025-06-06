import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import numpy as np
import requests

st.set_page_config(layout = 'wide')

from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")

SideBarLinks()

st.title('FEATURES OVER TIME')
st.write("Choose a region and your target country to view how including features changes scores over time.")
st.write("")


# EX DATA 
chart_data = pd.DataFrame(
    np.random.randn(20, 3), columns=["col1", "col2", "col3"]
)
chart_data["col4"] = np.random.choice(["A", "B", "C"], 20)

st.scatter_chart(
    chart_data,
    x="col1",
    y="col2",
    color="col4",
    size="col3",
)


col1,col2 = st.columns(2)
countries = []
regions = []
time = []

with col1: 
    region = st.selectbox(
        "Region:",
        regions,
        index=None,
        placeholder="Select Region ..."
    )
    
    country = st.selectbox(
        "Country:",
        countries,
        index=None,
        placeholder="Select Country ..."
    )
    
    
with col2:
    time = st.selectbox(
        "Time (years):",
        time,
        index=None,
        placeholder="Select Time ..."
    )

    end_date = st.date_input(
        "End Date:", 
        "today")

st.write("")
st.write("")
countries_get = f"http://host.docker.internal:4000/ml/ml/get_countries"
headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

all_countries = requests.get(countries_get, headers=headers, timeout=10)
if all_countries.status_code == 200:
    test_data = all_countries.json()
    st.write(test_data)
else:
    st.error(f"Error: {all_countries.status_code}")
    st.write(all_countries.text)
option = st.selectbox("Select A Country", tuple(all_countries))
chosen_country = st.text_input("Enter Country Here:")
st.subheader("SELECT FEATURES TO CONSIDER")
col3,col4 = st.columns(2)



with col3:
    life_exp = st.button("Life Expectancy (years)")
    if life_exp:
        data_code = "H2020_17"
        st.write("Country Code", chosen_country) 
        api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"

        try:
            headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()  
                st.success("Here are the values for the line of best fit!")
                st.json(data)
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")    
    inf_mort = st.button("Infant Mortality Rate")
    if inf_mort:
        data_code = "H2020_19"
        st.write("Country Code", chosen_country) 
        api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"

        try:
            headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()  
                st.success("Here are the values for the line of best fit!")
                st.json(data)
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")

    live_birth = st.button("Live Births per 1000 Population")
    if live_birth:
        data_code = "HFA_16"
        st.write("Country Code", chosen_country) 
        api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"

        try:
            headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()  
                st.success("Here are the values for the line of best fit!")
                st.json(data)
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")

with col4:
    gen_prac = st.button("General Practitioners per 10,000 Population")
    if gen_prac:
        data_code = "HLTHRES_67"
        st.write("Country Code", chosen_country) 
        api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"

        try:
            headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()  
                st.success("Here are the values for the line of best fit!")
                st.json(data)
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")
    
    health_expen = st.button("Total Health Expenditure per Capita")
    if health_expen:
        data_code = "HFA_570"
        st.write("Country Code", chosen_country) 
        api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"

        try:
            headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()  
                st.success("Here are the values for the line of best fit!")
                st.json(data)
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")
    
    impov_house = st.button("Impoverished Households")
    if impov_house:
        data_code = "UHCFP_2"
        st.write("Country Code", chosen_country) 
        api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"

        try:
            headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()  
                st.success("Here are the values for the line of best fit!")
                st.json(data)
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")



