import decimal
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

# Your backend endpoint URL - for getting all countries for the drop down 
get_country_url = "http://host.docker.internal:4000/country/countries"  

country_list = []

#to display country dropdown
try:
    response = requests.get(get_country_url)
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
    #country selection 
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

st.subheader("Select Features to Consider")
col3,col4 = st.columns(2)

#displays all graphical data through getting the regression values and using plotly to graph
def display_data(data_code, y_value, title):
    get_graph = f"http://web-api:4000/ml/ml/get_autoregressive/{chosen_country}/{data_code}/{chosen_year}"
    all_countries = requests.get(get_graph)
    all_country = all_countries.text
    if all_countries.status_code == 200:
        data_dict = json.loads(all_country)
        data_dict = json.loads(data_dict)
        df_country = pd.DataFrame(data_dict)
        df_graph = df_country 
        df_graph['YEAR'] = df_graph['YEAR'].astype(float)
        X = np.array(df_graph['YEAR'])
        y = np.array(df_graph['VALUE']) 

        last_year = 2020
        print("THIS IS DF COUNTRY:", df_country)
        for index, row in df_country.iterrows():
            d = decimal.Decimal(str(row['VALUE']))
            #st.write("THIS IS D:", d)
            if d.as_tuple().exponent <= -3:
                last_year = row['YEAR']
                break

        x = np.array(X).ravel()
        y = np.array(y).ravel()
        
        pred_list = []
        print("THE LAST YEAR:", last_year)
        #st.write("The last year:", last_year)
        for index, row in df_country.iterrows():
            if row['YEAR'] >= last_year:
                pred_list.append(True)
            else:
                pred_list.append(False)
        df_country['IsPred'] = pred_list

        # Split the data
        df_actual = df_country[df_country['IsPred'] == False]
        df_pred = df_country[df_country['IsPred'] == True]

        # Create figure with both lines
        fig = go.Figure()

        # Get last point of historical data to connect to predicted data 
        if not df_actual.empty and not df_pred.empty:
            last_actual_year = df_actual.iloc[-1]['YEAR']
            last_actual_value = df_actual.iloc[-1]['VALUE']

            # add the last historical point to front of predicted values 
            df_pred_with_bridge = pd.concat([
                pd.DataFrame({'YEAR': [last_actual_year], 'VALUE': [last_actual_value]}),
                df_pred[['YEAR', 'VALUE']]
            ], ignore_index=True)
        else:
            df_pred_with_bridge = df_pred
        
        # Actual line (historical data)
        fig.add_trace(go.Scatter(
            x=df_actual['YEAR'],
            y=df_actual['VALUE'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='blue')
        ))

        # Predicted line 
        fig.add_trace(go.Scatter(
            x=df_pred_with_bridge['YEAR'],
            y=df_pred_with_bridge['VALUE'],
            mode='lines+markers',
            name='Predicted',
            line=dict(color='red')
        ))


        # Final layout
        fig.update_layout(
            title=title,
            xaxis_title='Year',
            yaxis_title=y_value
        )

        st.plotly_chart(fig)
    else:
        st.error(f"Error: {all_countries.status_code}")
        st.write(all_countries.text)

#creates booleans and empty values when deciding what to display
expenditure_bool = False
gen_prac_bool = False
live_birth_bool = False

data_code = ""
y_value = ""
title = ""

#each button when pressed calls the correct route to get regression values 
with col3:   

    live_birth = st.button("Live Births per 1000 Population")
    if live_birth:
        data_code = "HFA_16"
        y_value = "Live Births per 1000 population"
        title = "Live Births Over Time"
        #st.write("Country Code", chosen_country) 
        api_url = f"http://web-api:4000/ml/ml/get_autoregressive/{chosen_country}/{data_code}/{chosen_year}"

        try:

            response = requests.get(api_url, timeout=10)
            response_text = requests.get(api_url, timeout=10).text

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
        title = "General Practitioners Over Time"
        api_url = f"http://web-api:4000/ml/ml/get_autoregressive/{chosen_country}/{data_code}/{chosen_year}"

        try:
            response = requests.get(api_url)
            response_text = requests.get(api_url, timeout=10).text

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
        api_url = f"http://web-api:4000/ml/ml/get_autoregressive/{chosen_country}/{data_code}/{chosen_year}"

        try:

            response = requests.get(api_url, timeout=10)
            response_text = requests.get(api_url, timeout=10).text

            if response.status_code == 200:
                data = response.json()  
                expenditure_bool = True
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"No total health expenditure data for: {chosen_country}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write(f"URL that worked : {api_url}")

# Displaying relevant information if a button is pressed 
if expenditure_bool or live_birth_bool or gen_prac_bool:
    st.success("Hover over the graph below to see specific values")
    display_data(data_code, y_value, title)

