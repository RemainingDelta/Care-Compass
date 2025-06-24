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
from modules.style import style_sidebar, set_background_color

import time
from datetime import datetime, date

# Constants for feature configurations
FEATURES = {
    "live_births": {
        "code": "HFA_16",
        "title": "Live Births Over Time",
        "y_label": "Live Births per 1000 population",
        "table": "LiveBirths"
    },
    "general_practitioners": {
        "code": "HLTHRES_67",
        "title": "General Practitioners Over Time",
        "y_label": "General Practitioners per 10,000 population",
        "table": "GenPractitioners"
    },
    "health_expenditure": {
        "code": "HFA_570",
        "title": "Total Health Expenditure Over Time",
        "y_label": "Total Health Expenditure per Capita",
        "table": "HealthExpend"
    }
}

# Cache for predictions to avoid repeated API calls
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_prediction(country, data_code, year, user_id=1):
    """Cache predictions to improve performance"""
    return fetch_prediction_data(country, data_code, year, user_id)

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

def fetch_historical_data(country, data_code):
    """Fetch only historical data for a country/indicator"""
    # You might want to create an endpoint for this, or query the database directly
    # For now, we'll extract it from the full autoregression response
    pass

def fetch_prediction_data(country, data_code, year, user_id=1):
    """Fetch prediction data with smart fallback"""
    start_time = time.time()
    
    # First, try the fast prediction endpoint
    fast_url = f"http://web-api:4000/ml/predict_autoreg_fast/{country}/{data_code}/{year}/{user_id}"
    
    try:
        with get_session() as session:
            logger.info(f"Trying fast prediction: {fast_url}")
            response = session.get(fast_url, timeout=5)
            
            if response.status_code == 200:
                fast_data = response.json()
                elapsed = time.time() - start_time
                logger.info(f"Fast prediction successful in {elapsed:.2f}s")
                
                # We need to combine this with historical data
                # For now, fall through to full calculation
                # In production, you'd fetch historical data separately
                raise Exception("Need historical data too")
                
    except Exception as e:
        logger.info(f"Fast prediction failed: {str(e)}, falling back to full calculation")
    
    # Fallback to full autoregression calculation
    full_url = f"http://web-api:4000/ml/get_autoregressive/{country}/{data_code}/{year}"
    
    try:
        with get_session() as session:
            response = session.get(full_url, timeout=30)
            response.raise_for_status()
            
            elapsed = time.time() - start_time
            logger.info(f"Full calculation completed in {elapsed:.2f}s")
            
            data = response.json()
            if isinstance(data, str):
                data = json.loads(data)
            
            return data, elapsed
            
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise

def process_and_plot_data(df_country, title, y_value, calculation_time=None):
    """Process dataframe and create plot with enhanced features"""
    df_graph = df_country.copy()
    df_graph['YEAR'] = df_graph['YEAR'].astype(float)
    df_graph['VALUE'] = df_graph['VALUE'].astype(float)
    
    # Find transition from historical to predicted data
    last_historical_year = 2021  # You might want to make this dynamic
    
    # Mark predicted vs actual data
    df_graph['IsPred'] = df_graph['YEAR'] > last_historical_year
    
    # Split the data
    df_actual = df_graph[~df_graph['IsPred']]
    df_pred = df_graph[df_graph['IsPred']]
    
    # Create plot with explicit sizing
    fig = go.Figure()
    
    # Add actual data
    fig.add_trace(go.Scatter(
        x=df_actual['YEAR'],
        y=df_actual['VALUE'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='blue', width=3),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Value: %{y:.2f}<br>Type: Historical<extra></extra>'
    ))
    
    # Add predicted data with smooth transition
    if not df_actual.empty and not df_pred.empty:
        # Create smooth transition by including last historical point
        last_actual = df_actual.iloc[-1]
        
        fig.add_trace(go.Scatter(
            x=[last_actual['YEAR']] + df_pred['YEAR'].tolist(),
            y=[last_actual['VALUE']] + df_pred['VALUE'].tolist(),
            mode='lines+markers',
            name='Predicted',
            line=dict(color='red', width=3, dash='dash'),
            marker=dict(size=8, symbol='diamond'),
            hovertemplate='Year: %{x}<br>Value: %{y:.2f}<br>Type: Predicted<extra></extra>'
        ))
    
    # Add vertical line at prediction start
    fig.add_vline(
        x=last_historical_year, 
        line_dash="dot", 
        line_color="gray",
        annotation_text="Prediction starts",
        annotation_position="top"
    )
    
    # Calculate and display trend
    trend_text = ""
    if len(df_graph) > 1:
        try:
            from scipy import stats
            slope, intercept, r_value, _, _ = stats.linregress(df_graph['YEAR'], df_graph['VALUE'])
            trend_text = f"Trend: {'↑' if slope > 0 else '↓'} {abs(slope):.2f} per year (R²={r_value**2:.3f})"
        except:
            pass
    
    # Update layout with better styling and explicit sizing
    fig.update_layout(
        title={
            'text': f"{title}<br><sub>{trend_text}</sub>",
            'y':0.95,  # Lower this slightly from 0.98
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20}
        },
        xaxis_title='Year',
        yaxis_title=y_value,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        # Adjust margins - increase top margin
        height=600,
        margin=dict(
            l=80,      # left margin
            r=80,      # right margin
            t=120,     # top margin - INCREASED from 100 to 120
            b=80,      # bottom margin
            pad=10     # padding between title and plot
        ),
        # Make plot responsive
        autosize=True,
        # Grid styling
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            tickmode='linear',
            tick0=1970,
            dtick=10
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    # Add calculation time annotation if available
    if calculation_time:
        fig.add_annotation(
            text=f"Calculated in {calculation_time:.2f}s",
            xref="paper", yref="paper",
            x=0.02, y=-0.1,
            showarrow=False,
            font=dict(size=10, color="gray"),
            xanchor="left"
        )
    
    return fig

def display_data_with_loading(data_code, y_value, title, chosen_country, chosen_year):
    """Fetch and display feature data with loading states"""
    
    # Use full width container
    with st.container():
        # Create placeholder for loading message
        status_placeholder = st.empty()
        
        try:
            # Show loading message
            with status_placeholder:
                with st.spinner(f'Calculating predictions for {chosen_country} up to {chosen_year}...'):
                    # Use cached function
                    data, calculation_time = get_cached_prediction(chosen_country, data_code, chosen_year)
            
            # Clear loading message
            status_placeholder.empty()
            
            # Process and display data
            df_country = pd.DataFrame(data)
            
            # Create the plot FIRST (before metrics) for better layout
            fig = process_and_plot_data(df_country, title, y_value, calculation_time)
            
            # Display the chart using full width
            st.plotly_chart(fig, use_container_width=True)
            
            # Show statistics below the chart in a horizontal layout
            st.write("---")  # Divider
            
            # Use more columns for horizontal display
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
            
            with col1:
                st.metric("📊 Data Points", len(df_country))
            
            with col2:
                historical_count = len(df_country[df_country['YEAR'] <= 2021])
                st.metric("📈 Historical", historical_count)
            
            with col3:
                predicted_count = len(df_country[df_country['YEAR'] > 2021])
                st.metric("🔮 Predicted", predicted_count)
            
            with col4:
                # Add calculation time as a metric
                st.metric("⏱️ Time", f"{calculation_time:.2f}s")
            
            with col5:
                # Add download button aligned to the right
                csv = df_country.to_csv(index=False)
                st.download_button(
                    label="📥 Download data as CSV",
                    data=csv,
                    file_name=f"{chosen_country}_{data_code}_{chosen_year}.csv",
                    mime="text/csv"
                )
            
        except Exception as e:
            status_placeholder.empty()
            st.error(f"Failed to fetch predictions: {str(e)}")
            logger.error(f"Error in display_data_with_loading: {str(e)}")

# Page Configuration - Ensure wide layout
st.set_page_config(
    layout='wide', 
    page_title="Healthcare Features Over Time",
    page_icon="📈"
)
style_sidebar()
set_background_color() 
SideBarLinks()

# Custom CSS for modern styling - combining existing styles with new header styles
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
        background: white;
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
        background: #f1f8e9;
        color: #2c3e50 !important;
        padding: 1.8rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 2px solid #097969;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.15);
        position: relative;
        overflow: hidden;
    }

    /* Text colors for instructions card */
    .instructions-card * {
        color: #2c3e50 !important;
    }

    .instructions-card strong {
        color: #097969 !important;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        display: block;
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
        background: #f1f8e9;
        color: #097969;
        font-weight: 600;
        border: 2px solid #097969;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 12px 12px 0 0;
    }

    div[data-testid="stExpander"] > details:not([open]) > summary {
        border-radius: 12px;  /* Rounds all corners when closed */
    }

    div[data-testid="stExpander"] > details > summary:hover {
        background: linear-gradient(135deg, #c8e6c9 0%, #b2dfdb 100%);
    }
    
    /* Force main container to use almost full width */
    .main .block-container {
        max-width: 98% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Force plotly container to expand */
    .stPlotlyChart {
        width: 100% !important;
    }

    /* Ensure the plotly div itself is full width */
    .js-plotly-plot, .plotly {
        width: 100% !important;
    }

    /* Remove any constraining divs */
    .element-container {
        width: 100% !important;
    }

    /* Make sure the chart's parent divs don't constrain it */
    div[data-testid="stHorizontalBlock"] > div:has(.js-plotly-plot) {
        width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 16px;
        font-weight: 500;
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        border-radius: 30px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(9, 121, 105, 0.4);
    }

    /* Metrics in row */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
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
    
    /* Date input styling */
    .stDateInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 1.05rem;
        transition: all 0.3s ease;
    }
    
    .stDateInput > div > div > input:hover {
        border-color: #097969;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="page-header">
        <h1 class="page-title">📈 Healthcare Trends Over Time</h1>
        <div class="page-subtitle">Visualize historical data and future projections for key healthcare indicators</div>
    </div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown(f"""
    <div class="welcome-box">
        <div class="welcome-name">Welcome back, {st.session_state.get('name', 'Guest')}! 👋</div>
        <div>Explore how healthcare metrics have evolved and where they're heading in the future.</div>
    </div>
""", unsafe_allow_html=True)

# Quick Start Guide
st.markdown("""
    <div class="instructions-card">
        <strong>🎯 Quick Start Guide:</strong>
        <ol style="margin: 0.5rem 0 0 1rem; padding-left: 1rem;">
            <li>Select a country from the dropdown menu</li>
            <li>Choose your target year for projections (up to 2100)</li>
            <li>Click on any healthcare indicator button to see its trend</li>
            <li>Download the data as CSV for further analysis</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# How it works expander
with st.expander("📚 Learn How This Tool Works"):
    st.markdown("""
    ### 🔍 Understanding Healthcare Trend Analysis
    
    This tool uses advanced statistical modeling to analyze and predict healthcare trends.
    
    ---
    
    ### 📊 Available Healthcare Indicators
    
    **Live Births per 1,000 Population** 👶  
    Track population growth trends and birth rate changes over time
    
    **General Practitioners per 10,000 People** 👨‍⚕️  
    Monitor the availability of primary healthcare providers
    
    **Total Health Expenditure per Capita** 💰  
    Analyze healthcare spending patterns and future budget needs
    
    ---
    
    ### 🤖 Our Forecasting Technology
    
    **Autoregressive Models**  
    - Uses historical patterns to predict future values
    - Accounts for trends, seasonality, and country-specific factors
    - Provides reliable estimates based on WHO and GHSI data
    
    **Smart Performance Features**  
    - **Intelligent Caching**: Predictions stored for 1 hour
    - **Fast Mode**: Pre-calculated models when available
    - **Automatic Fallback**: Recalculates if needed
    
    ---
    
    ### 📈 How to Read the Charts
    
    - **Blue Line with Markers**: Historical data (actual measurements)
    - **Red Dashed Line**: Predicted future values
    - **Vertical Gray Line**: Shows where predictions begin
    - **Trend Indicator**: Shows if values are increasing (↑) or decreasing (↓)
    
    ---
    
    ### 💡 Pro Tips
    - Hover over data points to see exact values
    - Look for the R² value to assess prediction reliability
    - Download data for custom analysis in Excel or other tools
    """)

# Use full width for main content
main_container = st.container()

with main_container:
    # Fetch Countries
    try:
        country_list, code_list, country_code_list = fetch_countries("http://web-api:4000/country/countries")
    except Exception as e:
        logger.error(f"Failed to fetch countries: {str(e)}")
        st.error("Failed to load country data. Please try again later.")
        country_list, code_list, country_code_list = [], [], []

    # User Input Section
    st.markdown('<div class="section-header">🌐 Step 1: Select Country and Target Year</div>', unsafe_allow_html=True)
    
    input_container = st.container()
    with input_container:
        col1, col2 = st.columns(2)
        with col1:
            chosen_country2 = st.selectbox(
                "🌍 Select Country:",
                country_code_list,
                index=None,
                placeholder="Choose a country...",
                help="Select the country you want to analyze"
            )

        with col2:
            end_date = st.date_input(
                "📅 Target Year for Projections:", 
                value=date.today(),
                min_value=pd.to_datetime("2024-01-01"),
                max_value=pd.to_datetime("2100-01-01"),
                help="How far into the future do you want to project?"
            )

    # Process Inputs
    chosen_year = end_date.year if end_date else None
    
    if chosen_country2:
        chosen_country = chosen_country2[chosen_country2.index('-')+1:]
        
        st.write("")
        st.markdown('<div class="section-header">📊 Step 2: Select Healthcare Indicator to Analyze</div>', unsafe_allow_html=True)
        
        # Feature Selection buttons - these stay in columns
        col3, col4, col5 = st.columns(3)
        
        selected_feature = None
        
        with col3:
            if st.button("👶 Live Births", help="Track population growth trends", use_container_width=True):
                selected_feature = "live_births"
        
        with col4:
            if st.button("👨‍⚕️ General Practitioners", help="Monitor healthcare workforce", use_container_width=True):
                selected_feature = "general_practitioners"
        
        with col5:
            if st.button("💰 Health Expenditure", help="Analyze healthcare spending", use_container_width=True):
                selected_feature = "health_expenditure"
        
        # IMPORTANT: Display the chart OUTSIDE of any columns
        if selected_feature:
            feature = FEATURES[selected_feature]
            
            # Use the FULL WIDTH of the page - no columns here!
            st.success(f"✅ Loading {feature['title'].replace(' Over Time', '')} data for analysis...")
            
            # Call the display function directly, not inside any column
            display_data_with_loading(
                feature["code"], 
                feature["y_label"], 
                feature["title"], 
                chosen_country, 
                chosen_year
            )    
    else:
        st.info("👆 Please select a country to begin exploring healthcare trends")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <small>💡 Tip: Use the download button to export data for custom analysis in Excel or other tools</small>
    </div>
""", unsafe_allow_html=True)