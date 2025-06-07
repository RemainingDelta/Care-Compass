import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

st.set_page_config(layout = 'wide')

from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")

SideBarLinks()

st.title('FEATURES OVER TIME')
st.write("Choose a region and your target country to view how including features changes scores over time.")
st.write("")


headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Your backend endpoint URL
API_URL = "http://host.docker.internal:4000/country/countries"  

country_list = []

try:
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    country_list = [item["name"] for item in data]
    print("Countries:", country_list)


except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)



col1,col2 = st.columns(2)
regions = []
time = []

with col1: 
    
    country = st.selectbox(
        "Country:",
        country_list,
        index=None,
        placeholder="Select Country ..."
    )
    
    
with col2:

    end_date = st.date_input(
        "End Date:", 
        "today")

st.write("")
st.write("")

st.subheader("SELECT FEATURES TO CONSIDER")
col3,col4 = st.columns(2)

data_code = ""

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
            response_text = requests.get(api_url, headers=headers, timeout=10).text

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
            response_text = requests.get(api_url, headers=headers, timeout=10).text

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
            response_text = requests.get(api_url, headers=headers, timeout=10).text

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
            response_text = requests.get(api_url, headers=headers, timeout=10).text

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
            response_text = requests.get(api_url, headers=headers, timeout=10).text

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
            response_text = requests.get(api_url, headers=headers, timeout=10).text

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

# EX DATA 

#graph_button = st.button("Display Graph")
#if graph_button:
get_graph = f"http://host.docker.internal:4000/ml/ml/get_graph_data/{data_code}"
headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
    }
all_countries = requests.get(get_graph, headers=headers, timeout=10)
all_country = requests.get(get_graph, headers=headers, timeout=10).text
if all_countries.status_code == 200:
    data_dict = json.loads(all_country)

    #data_series = pd.Series(all_countries)
    #print(all_countries)
    df_country = pd.DataFrame(data_dict)
    #df_graph = pd.concat([df_graph, data_dict.to_frame().T], ignore_index=True)
    #print(df_graph)
    df_graph = df_country[(df_country['country'] == chosen_country)]
    df_graph['year'] = df_graph['year'].astype(float)
    X = np.array(df_graph['year'])
    y = np.array(df_graph['value']) 
    predict_dict = json.loads(response_text)
    slope = predict_dict['slope']
    intercept = predict_dict['intercept']
    def show_fit(X, y, slope, intercept):
        plt.figure()
        
        # in case this wasn't done before, transform the input data into numpy arrays and flatten them
        x = np.array(X).ravel()
        y = np.array(y).ravel()

        
        # plot the actual data
        plt.scatter(x, y, label='data')
        
        # compute linear predictions 
        # x is a numpy array so each element gets multiplied by slope and intercept is added
        y_pred = slope * x + intercept
        
        # plot the linear fit
        plt.plot(x, y_pred, color='black',
            ls=':',
            label='linear fit')
        
        plt.legend()
        
        plt.xlabel('x')
        plt.ylabel('y')
        
        # print the mean squared error
        y_pred = slope * x + intercept

    st.pyplot(show_fit(X, y, slope, intercept))


else:
    st.error(f"Error: {all_countries.status_code}")
    st.write(all_countries.text)


