import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import plotly.express as px
import plotly.graph_objects as go 

st.set_page_config(layout = 'wide')

from modules.style import style_sidebar, set_background
style_sidebar()

SideBarLinks()

#Creates title and description of the page
st.title('FEATURES OVER TIME')
st.write("Choose a region and your target country to view how including features changes scores over time.")
st.write("")

#headers to bypass requests 
headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Your backend endpoint URL - for getting all countries for the drop down 
get_country_url = "http://host.docker.internal:4000/country/countries"  

country_list = []

try:
    response = requests.get(get_country_url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()


    country_list = [item["name"] for item in data]
    code_list = [item["code"] for item in data]
    country_code_list = [item['name'] + '-' + item['code'] for item in data]
    print("Countries:", country_list)


except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)


#creates necessary columns for user inputs 
col1,col2 = st.columns(2)
regions = []
time = []

with col1: 
    
    chosen_country2 = st.selectbox(
        "Country:",
        country_code_list,
        index=None,
        placeholder="Select Country ..."
    )
    
    
with col2:

    end_date = st.date_input(
        "End Date:", 
        "today")

#handles considering the end date:
if end_date:
    chosen_year = end_date.year 


st.write("")
st.write("")

#handles getting the country code needed for accessing each dataset 
if chosen_country2:
    start_index = (str(chosen_country2)).index('-') + 1
    chosen_country = chosen_country2[start_index:]
else:
    st.info("Please select a country to proceed")


st.write("")
st.write("")

st.subheader("SELECT FEATURES TO CONSIDER")
col3,col4 = st.columns(2)

#displays all graphical data through getting the regression values and using plotly to graph
def display_data(data_code, y_value, title):
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
            
            # in case this wasn't done before, transform the input data into numpy arrays and flatten them
            x = np.array(X).ravel()
            y = np.array(y).ravel()

            
            # plot the actual data
            figure1 = px.scatter(x=x, y=y, labels={
                "x": "Time in Years",
                "y": y_value
            }, title = title)
            
            # compute linear predictions 
            # x is a numpy array so each element gets multiplied by slope and intercept is added
            x = np.linspace(1970, 2040, 10)
            y_pred = slope * x + intercept
            
            #px.legend()
            figure2 = go.Figure(data=[go.Scatter(x=x, y=y_pred, mode='lines', name='line of best fit')])

            figure3 = go.Figure(data = figure1.data + figure2.data)
            figure3.update_layout(title=title, xaxis_title='Year', yaxis_title=y_value)

            return figure3

        st.plotly_chart(show_fit(X, y, slope, intercept))
    else:
        st.error(f"Error: {all_countries.status_code}")
        st.write(all_countries.text)

#creates booleans and empty values when deciding what to display
life_exp_bool = False
inf_mort_bool = False
impov_house_bool = False
expenditure_bool = False
gen_prac_bool = False
live_birth_bool = False

data_code = ""
y_value = ""
title = ""

#each button when pressed calls the correct route to get regression values 
with col3:
    life_exp = st.button("Life Expectancy (years)")
    if life_exp:
        data_code = "H2020_17"
        y_value = "Life Expectancy (years)"
        title = "Life Expectancy Over Time"
       # st.write("Country Code", chosen_country) 
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
                life_exp_bool = True
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"No life expectancy data for: {chosen_country}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")   

    inf_mort = st.button("Infant Mortality Rate")
    if inf_mort:
        data_code = "H2020_19"
        y_value = "Infant Mortality Rate (%)"
        title = "Infant Mortality Rate Over Time"
        #st.write("Country Code", chosen_country) 
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
                inf_mort_bool = True
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"No infant mortality data for: {chosen_country}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")

    live_birth = st.button("Live Births per 1000 Population")
    if live_birth:
        data_code = "HFA_16"
        y_value = "Live Births per 1000 population"
        title = "Live Births Over Time"
        #st.write("Country Code", chosen_country) 
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
                live_birth_bool = True 
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"No live births data for: {chosen_country}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")

with col4:
    gen_prac = st.button("General Practitioners per 10,000 Population")
    if gen_prac:
        data_code = "HLTHRES_67"
        y_value = "General Practitoners per 10,000 population"
        title = "Life Expectancy Over Time"
        #st.write("Country Code", chosen_country) 
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
                gen_prac_bool = True 
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"No general practioner data for: {chosen_country}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")
    
    health_expen = st.button("Total Health Expenditure per Capita")
    if health_expen:
        data_code = "HFA_570"
        y_value = "Total Health Expenditure per Capita"
        title = "Total Health Expenditure Over Time"
        #st.write("Country Code", chosen_country) 
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
                expenditure_bool = True
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"No total health expenditure data for: {chosen_country}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")
    
    impov_house = st.button("Impoverished Households")
    if impov_house:
        data_code = "UHCFP_2"
        y_value = "Impoverished Households due to out-of-pocket healthcare payments"
        title = "Impoverished Households Over Time"
        #st.write("Country Code", chosen_country) 
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
                impov_house_bool = True 
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"No impoverished households data for: {chosen_country}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")

# Displaying relevant information if a button is pressed 
if inf_mort_bool or expenditure_bool or life_exp_bool or live_birth_bool or impov_house_bool or gen_prac_bool:
    st.success(f"""
                Here are the values for the line of best fit!  
                Slope: {round(data['slope'], 4)}  
                Intercept: {round(data['intercept'], 4)}
                """)
    st.badge(f"Mean Squared Error: {round(data['mse'], 4)}", color='violet')
    st.badge(f"Coefficient of Determination: {round(data['r2'], 4)}", color='violet')
    calculation = float(chosen_year)*data['slope'] + data['intercept']
    st.badge(f"The predicted value for your chosen date is: {round(calculation, 4)}", color='blue')
    #st.json(data)
    st.success("Hover over the graph below to see specific values")
    display_data(data_code, y_value, title)

