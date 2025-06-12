import decimal
import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import plotly.graph_objects as go
from contextlib import contextmanager
from modules.style import style_sidebar

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

def process_and_plot_data(df_country, title, y_value):
    """Process dataframe and create plot"""
    df_graph = df_country
    df_graph['YEAR'] = df_graph['YEAR'].astype(float)
    
    # Find last year of actual data
    last_year = 2020
    for _, row in df_country.iterrows():
        d = decimal.Decimal(str(row['VALUE']))
        if d.as_tuple().exponent <= -3:
            last_year = row['YEAR']
            break
    
    # Mark predicted vs actual data
    pred_list = [row['YEAR'] >= last_year for _, row in df_country.iterrows()]
    df_country['IsPred'] = pred_list
    
    # Split the data
    df_actual = df_country[~df_country['IsPred']]
    df_pred = df_country[df_country['IsPred']]
    
    # Create plot
    fig = go.Figure()
    
    # Add actual data
    fig.add_trace(go.Scatter(
        x=df_actual['YEAR'],
        y=df_actual['VALUE'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='blue')
    ))
    
    # Add predicted data with bridge point
    if not df_actual.empty and not df_pred.empty:
        last_actual = df_actual.iloc[-1]
        df_pred_with_bridge = pd.concat([
            pd.DataFrame({'YEAR': [last_actual['YEAR']], 'VALUE': [last_actual['VALUE']]}),
            df_pred[['YEAR', 'VALUE']]
        ], ignore_index=True)
        
        fig.add_trace(go.Scatter(
            x=df_pred_with_bridge['YEAR'],
            y=df_pred_with_bridge['VALUE'],
            mode='lines+markers',
            name='Predicted',
            line=dict(color='red')
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title=y_value
    )
    return fig

def display_data(data_code, y_value, title, chosen_country, chosen_year):
    """Fetch and display feature data"""
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
            fig = process_and_plot_data(df_country, title, y_value)
            st.plotly_chart(fig)
            
    except Exception as e:
        logger.error(f"Error fetching/processing data: {str(e)}")
        st.error(f"Failed to process data: {str(e)}")

# Page Configuration
st.set_page_config(layout='wide')
style_sidebar()
SideBarLinks()

# Page Title and Description
st.title('FEATURES OVER TIME')
st.write("Choose a region and your target country to view how including features changes scores over time.")
st.write("")

# Fetch Countries
try:
    country_list, code_list, country_code_list = fetch_countries("http://web-api:4000/country/countries")
except Exception as e:
    logger.error(f"Failed to fetch countries: {str(e)}")
    st.error("Failed to load country data. Please try again later.")
    country_list, code_list, country_code_list = [], [], []

# User Input Section
col1, col2 = st.columns(2)
with col1:
    chosen_country2 = st.selectbox(
        "Country:",
        country_code_list,
        index=None,
        placeholder="Select Country ..."
    )

with col2:
    end_date = st.date_input("End Date:", "today")

# Process Inputs
chosen_year = end_date.year if end_date else None
if chosen_country2:
    chosen_country = chosen_country2[chosen_country2.index('-')+1:]
    
    st.write("")
    st.write("")
    
    # Feature Selection Section
    st.subheader("Select Features to Consider")
    col3, col4 = st.columns(2)
    
    feature = []
    with col3:
        if st.button("Live Births per 1000 Population"):
            feature = FEATURES["live_births"]
            st.success("Hover over the graph below to see specific values")
    
    with col4:
        if st.button("General Practitioners per 10,000 Population"):
            feature = FEATURES["general_practitioners"]
            st.success("Hover over the graph below to see specific values")
        
        if st.button("Total Health Expenditure per Capita"):
            feature = FEATURES["health_expenditure"]
            st.success("Hover over the graph below to see specific values")
    if len(feature) != 0:
        display_data(feature["code"], feature["y_label"], feature["title"], 
                        chosen_country, chosen_year)
else:
    st.info("Please select a country to proceed")


