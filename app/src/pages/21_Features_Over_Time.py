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
    page_icon="🏥"
)
style_sidebar()
SideBarLinks()

# Use full width for main content
main_container = st.container()

with main_container:
    # Page Title and Description
    st.title('🏥 FEATURES OVER TIME')
    st.write("Explore historical trends and future projections for key healthcare indicators.")

    # Custom CSS for better styling and full width
    # Replace your CSS section with this more aggressive version:

    st.markdown("""
    <style>
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

    /* Style expander */
    div[data-testid="stExpander"] > details > summary {
        background-color: #d8f3dc;
        color: #1b4332;
        font-weight: 600;
        border: 1px solid #95d5b2;
        border-radius: 6px;
        padding: 8px;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 16px;
        font-weight: 500;
    }

    /* Metrics in row */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ How this tool works"):
        st.markdown("""
        ### 🎯 What It Does:
        This tool uses **autoregressive modeling** to predict future healthcare trends based on historical patterns.
        
        ### 📊 Available Indicators:
        - **Live Births per 1,000 Population** - Population growth trends
        - **General Practitioners per 10,000 People** - Healthcare workforce availability
        - **Total Health Expenditure per Capita** - Healthcare spending patterns
        
        ### 🚀 Performance Features:
        - **Smart Caching**: Predictions are cached for 1 hour to improve speed
        - **Fast Predictions**: Uses pre-calculated models when available
        - **Fallback Mode**: Automatically recalculates if no stored model exists
        
        ### 📈 How to Use:
        1. Select a country and target year
        2. Click on an indicator to view its trend
        3. Blue line = historical data, Red dashed line = predictions
        4. Download the data as CSV for further analysis
        """)

    # Spacer
    st.write("")

    # Fetch Countries
    try:
        country_list, code_list, country_code_list = fetch_countries("http://web-api:4000/country/countries")
    except Exception as e:
        logger.error(f"Failed to fetch countries: {str(e)}")
        st.error("Failed to load country data. Please try again later.")
        country_list, code_list, country_code_list = [], [], []

    # User Input Section - Keep in columns but ensure they don't constrain the chart
    input_container = st.container()
    with input_container:
        col1, col2 = st.columns(2)
        with col1:
            chosen_country2 = st.selectbox(
                "🌍 Select Country:",
                country_code_list,
                index=None,
                placeholder="Select Country ..."
            )

        with col2:
            end_date = st.date_input(
                "📅 Target Year:", 
                value=date.today(),
                min_value=pd.to_datetime("2024-01-01"),
                max_value=pd.to_datetime("2100-01-01")
            )

    # Process Inputs
    chosen_year = end_date.year if end_date else None
    
    # Replace your current button handling and display section with this:

    if chosen_country2:
        chosen_country = chosen_country2[chosen_country2.index('-')+1:]
        
        st.write("")
        st.subheader("📊 Select Healthcare Indicator to Analyze")
        
        # Feature Selection buttons - these stay in columns
        col3, col4, col5 = st.columns(3)
        
        selected_feature = None
        
        with col3:
            if st.button("👶 Live Births", help="Track population growth trends"):
                selected_feature = "live_births"
        
        with col4:
            if st.button("👨‍⚕️ General Practitioners", help="Monitor healthcare workforce"):
                selected_feature = "general_practitioners"
        
        with col5:
            if st.button("💰 Health Expenditure", help="Analyze healthcare spending"):
                selected_feature = "health_expenditure"
        
        # IMPORTANT: Display the chart OUTSIDE of any columns
        if selected_feature:
            feature = FEATURES[selected_feature]
            
            # Use the FULL WIDTH of the page - no columns here!
            st.success(f"Loading {feature['title'].replace(' Over Time', '')} data...")
            
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