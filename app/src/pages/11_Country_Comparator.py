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
from modules.style import style_sidebar, set_background

st.set_page_config(layout="wide")
style_sidebar()

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# Custom CSS for modern styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #fafafa;
    }
    
    /* Header styling - clean and simple */
    .page-header {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 1rem 0;
        padding: 0;
        line-height: 1.2;
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.95;
        line-height: 1.5;
        margin: 0;
        padding: 0;
    }
    
    /* Welcome section */
    .welcome-box {
        background: rgba(255, 255, 255, 0.6);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #097969;
    }
    
    .welcome-name {
        font-size: 1.5rem;
        font-weight: 600;
        color: #097969;
        margin-bottom: 0.5rem;
    }
    
    /* Instructions card */
    .instructions-card {
        background: rgba(232, 245, 240, 0.8);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid rgba(9, 121, 105, 0.2);
    }
    
    /* Expander styling */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(224, 224, 224, 0.5);
        margin-bottom: 1.5rem;
        overflow: hidden;
    }
    
    div[data-testid="stExpander"] > details > summary {
        background: linear-gradient(135deg, #f0fdf4 0%, #e8f5f0 100%);
        color: #097969;
        font-weight: 600;
        border: none;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
    }
    
    div[data-testid="stExpander"] > details > summary:hover {
        background: linear-gradient(135deg, #e8f5f0 0%, #d8f3dc 100%);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        margin-top: 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Country selector card */
    .selector-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(224, 224, 224, 0.5);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 1.05rem;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #097969;
    }
    
    /* Submit button */
    .stButton > button {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3);
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(9, 121, 105, 0.4);
    }
    
    /* Results section */
    .results-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(224, 224, 224, 0.7);
    }
    
    .results-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #097969;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Feature tracking section */
    .feature-tracking-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid rgba(224, 224, 224, 0.5);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Data table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Plot button specific styling */
    .plot-button-container .stButton > button {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        padding: 0.5rem 2rem;
        font-size: 1rem;
    }
    
    /* Info badges */
    .info-badge {
        background: rgba(9, 121, 105, 0.1);
        color: #097969;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid rgba(224, 224, 224, 0.3);
    }
    
    /* Country selection labels */
    .country-label {
        font-weight: 600;
        color: #2c3e50;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .country-number {
        background: #097969;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: 700;
    }
    
    /* Feature list styling */
    .feature-list {
        background: rgba(232, 245, 240, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .feature-item {
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(9, 121, 105, 0.1);
        font-size: 0.95rem;
        color: #2c3e50;
    }
    
    .feature-item:last-child {
        border-bottom: none;
    }
    
    /* Status messages */
    .status-message {
        background: rgba(255, 193, 7, 0.1);
        border: 1px solid rgba(255, 193, 7, 0.3);
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #2c3e50;
        color: white;
        text-align: center;
        padding: 8px 12px;
        border-radius: 6px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.85rem;
        white-space: nowrap;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    </style>
""", unsafe_allow_html=True)

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

def display_data(data_code, y_value, title, countries_exist, chosen_year):
    dataframe_list = []
    for chosen_country in countries_exist:
        api_url = f"http://web-api:4000/ml/get_autoregressive/{chosen_country}/{data_code}/{chosen_year}"
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
                df_graph = df_country
                df_graph['COUNTRY'] = chosen_country
                dataframe_list.append(df_graph)
                
        except Exception as e:
            logger.error(f"Error fetching/processing data: {str(e)}")
            st.error(f"Failed to process data: {str(e)}")
    
    df_graph = pd.concat(dataframe_list, ignore_index=True)
    df_graph['YEAR'] = df_graph['YEAR'].astype(float)
    
    # Create a more styled chart
    fig = px.line(df_graph, x='YEAR', y='VALUE', 
                  labels={"YEAR": "Year", "VALUE": y_value}, 
                  color='COUNTRY', 
                  title=title)
    
    # Update layout for better appearance
    fig.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font=dict(size=18, color='#097969'),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            zerolinecolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            zerolinecolor='rgba(128,128,128,0.2)'
        ),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(224,224,224,0.8)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Header
st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🌍 Country Healthcare Comparator</h1>
        <div class="page-subtitle">Compare healthcare systems across multiple countries with data-driven insights</div>
    </div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown(f"""
    <div class="welcome-box">
        <div class="welcome-name">Welcome back, {st.session_state.get('name', 'Guest')}! 👋</div>
        <div>Explore and compare healthcare metrics across different countries to gain valuable insights.</div>
    </div>
""", unsafe_allow_html=True)

# Quick Start Guide
st.markdown("""
    <div class="instructions-card">
        <strong>🎯 Quick Start Guide:</strong>
        <ol style="margin: 0.5rem 0 0 1rem; padding-left: 1rem;">
            <li>Choose up to 3 countries from the dropdown menus below</li>
            <li>Click "Submit" to generate a detailed comparison table</li>
            <li>Use the feature tracking section to visualize trends over time</li>
            <li>Explore projected values up to 2035 using our forecasting models</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# How it works expander
with st.expander("📚 Learn How This Tool Works"):
    st.markdown("""
    ### 🔍 Understanding Country Comparison
    
    This tool provides comprehensive healthcare system comparisons using data from trusted global sources.
    
    ---
    
    ### 📊 Key Healthcare Metrics
    
    **Life Expectancy** 📈  
    Average years a person is expected to live in each country
    
    **Infant Mortality Rate** 👶  
    Deaths per 1,000 live births (lower is better)
    
    **Healthcare Workforce** 👨‍⚕️  
    Number of general practitioners per 10,000 population
    
    **Health Expenditure** 💰  
    Total healthcare spending per capita in USD
    
    **Financial Protection** 🛡️  
    Percentage of households impoverished by healthcare costs
    
    **Birth Rate Indicators** 📊  
    Live births per 1,000 population
    
    ---
    
    ### 🤖 Forecasting Technology
    
    Our **autoregressive models** analyze historical patterns to project future trends:
    - Based on WHO and GHSI historical data
    - Accounts for country-specific trends
    - Provides estimates up to 2035
    - Helps identify emerging healthcare challenges
    
    ---
    
    ### 📈 Data Sources
    - **Global Health Security Index (GHSI)**
    - **World Health Organization (WHO)**
    - **Updated regularly** to ensure accuracy
    """)

# Fetch Countries
feature2 = []
country3_list = ["N/A"]

try:
    country_list, code_list, country_code_list = fetch_countries("http://web-api:4000/country/countries")
    country3_list += country_code_list
except Exception as e:
    logger.error(f"Failed to fetch countries: {str(e)}")
    st.error("Failed to load country data. Please try again later.")
    country_list, code_list, country_code_list = [], [], []

# Country Selection Section
st.markdown('<div class="section-header">🌐 Step 1: Select Countries for Comparison</div>', unsafe_allow_html=True)

features = []
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="country-label"><span class="country-number">1</span> First Country</div>', unsafe_allow_html=True)
    country1 = st.selectbox(
        "Select your primary country",
        country_code_list,
        index=None,
        placeholder="Choose a country...",
        help="This will be your baseline for comparison"
    )

with col2:
    st.markdown('<div class="country-label"><span class="country-number">2</span> Second Country</div>', unsafe_allow_html=True)
    country2 = st.selectbox(
        "Select a country to compare",
        country_code_list,
        index=None,
        placeholder="Choose a country...",
        help="Compare against your primary selection"
    )

with col3:
    st.markdown('<div class="country-label"><span class="country-number">3</span> Third Country (Optional)</div>', unsafe_allow_html=True)
    country3 = st.selectbox(
        "Add another country",
        country3_list,
        index=None,
        placeholder="Choose a country...",
        help="Optional third country for comparison"
    )
    if country3 == "N/A":
        country3_status = False
    else:
        country3_status = True

# Submit button
table = st.button("🔍 Generate Comparison", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Handle country code extraction
if country1:
    start_index = (str(country1)).index('-') + 1
    country1 = country1[start_index:]
else:
    st.info("👆 Please select at least one country to begin your comparison")

if country2:
    start_index = (str(country2)).index('-') + 1
    country2 = country2[start_index:]

if country3 and country3_status:
    start_index = (str(country3)).index('-') + 1
    country3 = country3[start_index:]

# Process comparison
countries_exist = list(filter(None, [country1, country2] + ([country3] if country3_status else [])))


# Define features
life_expectancy = "Life Expectancy (years)"
inf_mortality = "Infant Mortality Rate (%)"
live_births = "Live Births per 1000 Population"
gen_practitioners = "General Practitioners per 10,000 Population"
health_expend = "Total Health Expenditure per Capita"
impov_house = "Impoverished Households due to out-of-pocket healthcare payments"

features = [live_births, gen_practitioners, health_expend]

# Display results
if table:
    if len(set(countries_exist)) != len(countries_exist):
        st.error("🚫 You've selected the same country multiple times. Please choose different countries for comparison.")
    else:
        with st.spinner('🔄 Fetching healthcare data from global databases...'):
            master_df = pd.DataFrame()

            for country in countries_exist:
                if country:
                    try:
                        countryurl = f"http://host.docker.internal:4000/country/features/{country}"
                        response = requests.get(countryurl)

                        if response.status_code == 200:
                            data_dict = response.json()

                            # Flatten dictionary row
                            flat_row = {"Country": country}
                            for feature_name, feature_values in data_dict.items():
                                for k, v in feature_values.items():
                                    flat_row[f"{feature_name}"] = v
                            
                            if any(v not in [None, "", 0.0] for k, v in flat_row.items() if k != "Country"):
                                df = pd.DataFrame([flat_row])
                                master_df = pd.concat([master_df, df], ignore_index=True)

                        else:
                            if country3_status == True:
                                st.error(f"Failed to fetch data for country: {country}")

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

            # Display results
            if not master_df.empty:
                st.markdown('<div class="results-header">📊 Healthcare Comparison Results</div>', unsafe_allow_html=True)
                
                st.dataframe(
                    master_df,
                    hide_index=True,
                    use_container_width=True,
                )
                
                # Add footnotes with better styling
                st.markdown("""
                    <div style="margin-top: 1rem; padding: 1rem; background: rgba(9, 121, 105, 0.05); border-radius: 10px;">
                        <p style="font-size: 0.85rem; color: #6c757d; margin: 0.25rem 0;">
                            <strong>*</strong> General Practitioners per 10,000 Population<br>
                            <strong>**</strong> Total Health Expenditure per Capita (USD)<br>
                            <strong>+</strong> Percentage of households impoverished by healthcare payments<br>
                            <strong>++</strong> Live births per 1,000 population
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# Feature Tracking Section
st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📈 Step 2: Track Healthcare Trends Over Time</div>', unsafe_allow_html=True)

col7, col3 = st.columns([3, 1], gap="large")

with col7:
    feature = st.selectbox(
        "Select a healthcare metric to visualize:",
        features,
        index=None,
        placeholder="Choose a metric...",
        help="View historical data and future projections"
    )

with col3:
    st.markdown('<div class="plot-button-container" style="margin-top: 1.75rem;">', unsafe_allow_html=True)
    plot = st.button("📊 Generate Chart", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if plot and feature and countries_exist:
    with st.spinner('📊 Generating visualization with projections to 2035...'):
        if feature == live_births:
            feature2 = FEATURES["live_births"]
            st.markdown("""
                <div style="margin-top: 2rem;">
                    <h3 style="color: #097969;">📊 Projected Live Birth Rates Through 2035</h3>
                    <p style="color: #6c757d;">Comparing birth rate trends and projections across selected countries</p>
                </div>
            """, unsafe_allow_html=True)

        elif feature == gen_practitioners:
            feature2 = FEATURES["general_practitioners"]
            st.markdown("""
                <div style="margin-top: 2rem;">
                    <h3 style="color: #097969;">👨‍⚕️ Healthcare Workforce Projections Through 2035</h3>
                    <p style="color: #6c757d;">Tracking general practitioner availability per 10,000 population</p>
                </div>
            """, unsafe_allow_html=True)

        elif feature == health_expend:
            feature2 = FEATURES["health_expenditure"]
            st.markdown("""
                <div style="margin-top: 2rem;">
                    <h3 style="color: #097969;">💰 Healthcare Expenditure Projections Through 2035</h3>
                    <p style="color: #6c757d;">Analyzing healthcare spending trends per capita</p>
                </div>
            """, unsafe_allow_html=True)

        if len(feature2) != 0:
            display_data(feature2["code"], feature2["y_label"], feature2["title"], 
                        countries_exist, 2035)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <small>💡 Tip: Hover over chart lines to see exact values for each year</small>
    </div>
""", unsafe_allow_html=True)