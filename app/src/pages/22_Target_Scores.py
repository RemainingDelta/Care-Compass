import logging
logger = logging.getLogger(__name__)
import streamlit as st

# PAGE CONFIG MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Healthcare Target Calculator",
    page_icon="🎯",
    layout="wide"
)

# Now import other modules
import requests
from modules.nav import SideBarLinks
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from modules.style import style_sidebar

def get_best_matching_key(target_key, data_dict):
    """Returns the best-matching key from data_dict for a given target_key by stripping symbols"""
    def normalize(s):
        return s.lower().replace("*", "").replace("+", "").replace("(", "").replace(")", "").strip()
    
    norm_target = normalize(target_key)
    for actual_key in data_dict.keys():
        if normalize(actual_key) == norm_target:
            return actual_key
    return None


# Apply styling AFTER page config
style_sidebar()
SideBarLinks()

# Configuration
API_BASE_URL = "http://host.docker.internal:4000"  # Fixed to match your setup
CURRENT_YEAR = datetime.now().year

# Feature configurations - keys should NOT include asterisks (those are just for footnotes)
FEATURES_CONFIG = {
    "life_expectancy": {
        "name": "Life Expectancy",
        "code": "H2020_17",
        "unit": "years",
        "icon": "🏥",
        "improvement": "increase",
        "display_key": "Life Expectancy (years)"
    },
    "infant_mortality": {
        "name": "Infant Mortality Rate",
        "code": "H2020_19",
        "unit": "per 1,000 live births",
        "icon": "👶",
        "improvement": "decrease",
        "display_key": "Infant Mortality Rate (%)"
    },
    "live_births": {
        "name": "Live Births",
        "code": "HFA_16",
        "unit": "per 1,000 population",
        "icon": "🍼",
        "improvement": "stable",
        "display_key": "Live Births++"
    },
    "practitioners": {
        "name": "General Practitioners",
        "code": "HLTHRES_67",
        "unit": "per 10,000 population",
        "icon": "👨‍⚕️",
        "improvement": "increase",
        "display_key": "General Practitioners*"
    },
    "expenditure": {
        "name": "Health Expenditure",
        "code": "HFA_570",
        "unit": "per capita (USD)",
        "icon": "💰",
        "improvement": "increase",
        "display_key": "Health Expenditure**"
    },
    "impoverished": {
        "name": "Impoverished Households",
        "code": "UHCFP_2",
        "unit": "% of households",
        "icon": "🏠",
        "improvement": "decrease",
        "display_key": "Impoverished Households"
    }
}

def try_float(val):
    try:
        return float(val)
    except:
        return None

@st.cache_data(ttl=3600)
def fetch_countries():
    """Fetch country list from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/country/countries", timeout=10)
        response.raise_for_status()
        data = response.json()
        return [f"{item['name']}-{item['code']}" for item in data]
    except Exception as e:
        st.error(f"Failed to fetch countries: {str(e)}")
        return []

def fetch_current_values(country_code):
    """Fetch current feature values for a country"""
    try:
        response = requests.get(f"{API_BASE_URL}/country/features/{country_code}")
        if response.status_code == 200:
            data_dict = response.json()
            
            # Flatten the nested response structure
            flat_data = {}
            for feature_name, feature_values in data_dict.items():
                if isinstance(feature_values, dict) and 'VALUE' in feature_values:
                    try:
                        flat_data[feature_name] = float(feature_values['VALUE'])
                    except:
                        flat_data[feature_name] = feature_values['VALUE']
                else:
                    try:
                        flat_data[feature_name] = float(feature_values)
                    except:
                        flat_data[feature_name] = feature_values
            
            return flat_data
        else:
            st.error(f"API returned status {response.status_code} for country features")
            return None
    except Exception as e:
        logger.error(f"Error fetching current values: {str(e)}")
        st.error(f"Error fetching current values: {str(e)}")
        return None

def get_regression_params(country_code, data_code):
    """Get regression parameters for a country and indicator"""
    try:
        api_url = f"{API_BASE_URL}/ml/get_regression/{country_code},{data_code}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"No regression data available for {data_code} in {country_code}")
            return None
    except Exception as e:
        logger.error(f"Error getting regression params: {str(e)}")
        st.error(f"Error getting regression params: {str(e)}")
        return None

def calculate_target_year(current_value, target_value, slope, intercept):
    """Calculate when target will be reached based on linear regression"""
    if slope == 0:
        return "No trend (flat line)"
    
    # Linear regression: value = slope * year + intercept
    # Solving for year: year = (value - intercept) / slope
    target_year = (target_value - intercept) / slope
    
    # Convert to integer year
    target_year = int(round(target_year))
    
    # Check if target is realistic
    if target_year < CURRENT_YEAR:
        return "Already achieved" if abs(current_value - target_value) > 0.01 else "Current level"
    elif target_year > CURRENT_YEAR + 100:
        return "Beyond 100 years"
    else:
        years_to_target = target_year - CURRENT_YEAR
        return f"{target_year} ({years_to_target} years)"

def create_projection_chart(feature_name, current_value, target_value, regression_data, years_ahead=30):
    """Create a chart showing projection to target"""
    slope = regression_data['slope']
    intercept = regression_data['intercept']
    
    # Generate projection years
    years = list(range(CURRENT_YEAR - 10, CURRENT_YEAR + years_ahead + 1))
    values = [slope * year + intercept for year in years]
    
    # Create figure
    fig = go.Figure()
    
    # Historical/Projection line
    fig.add_trace(go.Scatter(
        x=years,
        y=values,
        mode='lines',
        name='Trend',
        line=dict(color='blue', width=2)
    ))
    
    # Current value point
    if current_value:
        fig.add_trace(go.Scatter(
            x=[CURRENT_YEAR],
            y=[current_value],
            mode='markers',
            name='Current',
            marker=dict(size=12, color='green', symbol='star')
        ))
    
    # Target line
    fig.add_hline(
        y=target_value,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Target: {target_value:.1f}"
    )
    
    # Calculate intersection point
    if slope != 0:
        target_year = (target_value - intercept) / slope
        if CURRENT_YEAR <= target_year <= CURRENT_YEAR + years_ahead:
            fig.add_trace(go.Scatter(
                x=[target_year],
                y=[target_value],
                mode='markers',
                name='Target Reached',
                marker=dict(size=12, color='red', symbol='x')
            ))
    
    fig.update_layout(
        title=f"{feature_name} Projection",
        xaxis_title="Year",
        yaxis_title="Value",
        height=400,
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

# Title and Description
st.title("🎯 SET AND MONITOR TARGET VALUES")
st.write("Set healthcare goals and see when they might be achieved based on historical trends.")

# Custom CSS
# CSS to make this section wider and bigger
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
# How it works expander
with st.expander("ℹ️ How this tool works"):
    st.markdown("""
    ### 🎯 Purpose
    This tool helps you set long-term healthcare goals for a country and estimates when they might be achieved based on historical trends.

    ### 📊 How It Works
    1. **Linear Regression Analysis**: We analyze historical data for each healthcare indicator
    2. **Trend Projection**: We project future values based on the historical trend
    3. **Target Achievement**: We calculate when your target value will be reached if trends continue

    ### 🔍 Indicators Available
    - **Life Expectancy**: Average years of life expected at birth
    - **Infant Mortality**: Deaths under age 1 per 1,000 live births
    - **Live Births**: Birth rate per 1,000 population
    - **General Practitioners**: Healthcare workforce per 10,000 people
    - **Health Expenditure**: Total spending per capita
    - **Impoverished Households**: Percentage affected by healthcare costs

    ### ⚠️ Important Notes
    - Projections assume historical trends continue unchanged
    - Major policy changes or events can alter these trajectories
    - Use these as planning estimates, not guarantees
    """)

# Fetch countries
country_list = fetch_countries()

# Country selection
st.write("")
col1, col2 = st.columns([3, 1])

with col1:
    chosen_country = st.selectbox(
        "🌍 Select Country:",
        country_list,
        index=None,
        placeholder="Choose a country..."
    )

# Extract country code
country_code = None
current_values = None
if chosen_country:
    country_code = chosen_country.split('-')[-1]
    
    # Fetch current values
    with st.spinner("Loading current values..."):
        current_values = fetch_current_values(country_code)

# Show current values if available
if current_values:
    st.write("")
    st.subheader(f"📊 Current Healthcare Indicators for {chosen_country.split('-')[0]}")
    
    
    # Create metrics display
    st.write("### Displaying Metrics:")
    metric_cols = st.columns(3)
    
    # Add debugging for each metric
    debug_info = []
    
    for idx, (key, config) in enumerate(FEATURES_CONFIG.items()):
        col_idx = idx % 3
        
        # Get value from flattened data
        display_key = config['display_key']
        actual_key = get_best_matching_key(display_key, current_values)
        display_value = current_values.get(actual_key)

        
        # Debug info
        debug_info.append({
            'Feature': config['name'],
            'Key': key,
            'Display Key': display_key,
            'Value Found': display_value,
            'Type': type(display_value).__name__ if display_value is not None else 'None'
        })
        
        with metric_cols[col_idx]:
            # Add individual debug for this metric
            with st.container():
                
                if display_value is not None and display_value != 'N/A':
                    st.metric(
                        label=f"{config['icon']} {config['name']}",
                        value=f"{display_value:.2f}" if isinstance(display_value, (int, float)) else str(display_value),
                        help=f"Measured in {config['unit']}"
                    )
                else:
                    st.metric(
                        label=f"{config['icon']} {config['name']}",
                        value="No data",
                        help="Data not available for this country"
                    )
    
    
    # Add footnotes
    st.caption("*General Practitioners per 10,000 Population")
    st.caption("**Total Health Expenditure per Capita")
    st.caption("***Impoverished Households due to out-of-pocket healthcare payments")

# Target value inputs
if country_code:
    st.write("")
    st.write("")
    st.subheader("🎯 Set Your Target Values")
    
    # Create input columns
    input_cols = st.columns(3)
    target_values = {}
    
    for idx, (key, config) in enumerate(FEATURES_CONFIG.items()):
        col_idx = idx % 3
        with input_cols[col_idx]:
            # Get current value for reference
            current_val = current_values.get(config['display_key']) if current_values else None
            
            # Create number input with helpful placeholder
            if current_val is not None and isinstance(current_val, (int, float)):
                help_text = f"Current: {current_val:.1f} {config['unit']}"
            else:
                help_text = f"Enter target {config['unit']}"
            
            target_values[key] = st.number_input(
                f"{config['icon']} {config['name']}",
                min_value=0.0,
                value=None,
                help=help_text,
                key=f"target_{key}"
            )
    
    # Calculate button
    st.write("")
    col_calc, col_empty = st.columns([1, 4])
    
    with col_calc:
        if st.button("🔮 Calculate Projections", type="primary"):
            if any(target_values.values()):
                # Progress bar
                progress_bar = st.progress(0, text="Calculating projections...")
                results = {}
                errors = []
                
                # Calculate for each feature with a target
                total_targets = sum(1 for v in target_values.values() if v)
                current_idx = 0
                
                for key, target_value in target_values.items():
                    if target_value:
                        current_idx += 1
                        progress_bar.progress(current_idx / total_targets, text=f"Analyzing {FEATURES_CONFIG[key]['name']}...")
                        
                        # Get regression parameters
                        regression_data = get_regression_params(country_code, FEATURES_CONFIG[key]['code'])
                        
                        if regression_data:
                            # Get current value from flattened data
                            display_key = FEATURES_CONFIG[key]['display_key']
                            actual_key = get_best_matching_key(display_key, current_values)
                            current_val = current_values.get(actual_key) if current_values else None
                            
                            if current_val is not None and isinstance(current_val, (int, float)):
                                result = calculate_target_year(
                                    current_val,
                                    target_value,
                                    regression_data['slope'],
                                    regression_data['intercept']
                                )
                                
                                results[key] = {
                                    'target': target_value,
                                    'current': current_val,
                                    'projection': result,
                                    'regression': regression_data,
                                    'trend': 'increasing' if regression_data['slope'] > 0 else 'decreasing'
                                }
                            else:
                                errors.append(f"No current data for {FEATURES_CONFIG[key]['name']}")
                        else:
                            errors.append(f"No regression model available for {FEATURES_CONFIG[key]['name']}")
                
                progress_bar.empty()
                
                # Show errors if any
                if errors:
                    for error in errors:
                        st.warning(error)
                
                # Display results if we have any
# Display results if we have any
                if results:
                    st.write("")
                    st.write("---")
                    
                    # CSS to fix table width issues
                    st.markdown("""
                    <style>
                    /* Remove ALL width constraints for dataframe */
                    [data-testid="stDataFrame"] {
                        transform: none !important;
                        width: 100% !important;
                        max-width: none !important;  /* Remove max-width constraint */
                        margin: 0 !important;
                    }
                    
                    [data-testid="stDataFrame"] > div {
                        width: 100% !important;
                        max-width: none !important;
                    }
                    
                    /* Make table use full available width */
                    [data-testid="stDataFrame"] table {
                        font-size: 1.1rem !important;
                        width: 100% !important;
                        table-layout: fixed !important;  /* Force equal column widths */
                    }
                    
                    [data-testid="stDataFrame"] th {
                        padding: 10px 5px !important;
                        font-size: 1.1rem !important;
                        background-color: #e9ecef !important;
                        text-align: center !important;
                    }
                    
                    [data-testid="stDataFrame"] td {
                        padding: 10px 5px !important;
                        font-size: 1.1rem !important;
                        text-align: center !important;
                        white-space: normal !important;  /* Allow text wrapping */
                        word-wrap: break-word !important;
                    }
                    
                    /* Center tabs */
                    .stTabs [data-baseweb="tab-list"] {
                        justify-content: center !important;
                        gap: 3rem !important;
                    }
                    
                    .stTabs [data-baseweb="tab-list"] button {
                        font-size: 1.6rem !important;
                        padding: 15px 50px !important;
                        font-weight: bold !important;
                    }
                    
                    /* Center expanders in detailed view */
                    .stExpander {
                        max-width: 900px;
                        margin: 1rem auto !important;
                    }
                    
                    /* Center download button */
                    .stDownloadButton {
                        display: flex;
                        justify-content: center;
                        margin: 3rem auto;
                    }
                    
                    .stDownloadButton button {
                        font-size: 1.4rem !important;
                        padding: 15px 40px !important;
                    }
                    
                    /* Metrics row styling */
                    .metrics-row {
                        text-align: center;
                        margin: 2rem 0;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Big centered title
                    st.markdown("""
                    <h1 style="font-size: 3.5rem; font-weight: 900; text-align: center; margin: 2rem auto; color: #1f2937;">
                        📈 Projection Results
                    </h1>
                    """, unsafe_allow_html=True)
                    
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["📊 Summary", "📈 Detailed Analysis"])
                    
                    with tab1:
                        # Add some padding with columns
                        col1, col2, col3 = st.columns([0.5, 10, 0.5])
                        
                        with col2:
                            # Summary table with clear but concise column names
                            summary_data = []
                            
                            for key, result in results.items():
                                config = FEATURES_CONFIG[key]
                                
                                # Clear status text
                                if isinstance(result['projection'], str):
                                    if "Already achieved" in result['projection']:
                                        status = "✅ Achieved"
                                    elif "Beyond" in result['projection']:
                                        status = "⚠️ Long Term"
                                    elif "No trend" in result['projection']:
                                        status = "➖ No Trend"
                                    else:
                                        status = "📊 On Track"
                                else:
                                    status = "📊 Calculating"
                                
                                summary_data.append({
                                    'Indicator': f"{config['icon']} {config['name']}",
                                    'Current': f"{result['current']:.1f}",
                                    'Target': f"{result['target']:.1f}",
                                    'Trend': '📈' if result['trend'] == 'increasing' else '📉',
                                    'Projection': result['projection'],
                                    'Status': status
                                })
                            
                            df_summary = pd.DataFrame(summary_data)
                            
                            # Add custom styling for this specific dataframe
                            st.markdown("""
                            <style>
                            /* Make sure the table fits */
                            [data-testid="stDataFrame"]:has(table) {
                                width: 100% !important;
                            }
                            
                            /* Adjust column widths */
                            [data-testid="stDataFrame"] table {
                                width: 100% !important;
                            }
                            
                            /* Make specific columns narrower */
                            [data-testid="stDataFrame"] th:nth-child(2),
                            [data-testid="stDataFrame"] td:nth-child(2),
                            [data-testid="stDataFrame"] th:nth-child(3),
                            [data-testid="stDataFrame"] td:nth-child(3) {
                                width: 80px !important;  /* Current and Target columns */
                            }
                            
                            [data-testid="stDataFrame"] th:nth-child(4),
                            [data-testid="stDataFrame"] td:nth-child(4) {
                                width: 60px !important;  /* Trend column */
                            }
                            
                            /* Give more space to Indicator and Projection columns */
                            [data-testid="stDataFrame"] th:nth-child(1),
                            [data-testid="stDataFrame"] td:nth-child(1) {
                                width: 25% !important;  /* Indicator column */
                            }
                            
                            [data-testid="stDataFrame"] th:nth-child(5),
                            [data-testid="stDataFrame"] td:nth-child(5) {
                                width: 20% !important;  /* Projection column */
                            }
                            
                            [data-testid="stDataFrame"] th:nth-child(6),
                            [data-testid="stDataFrame"] td:nth-child(6) {
                                width: 15% !important;  /* Status column */
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            st.dataframe(df_summary, hide_index=True, use_container_width=True)
                    with tab2:
                        # Detailed charts for each indicator
                        for key, result in results.items():
                            config = FEATURES_CONFIG[key]
                            
                            with st.expander(f"{config['icon']} {config['name']} - Detailed Analysis", expanded=False):
                                # Create the chart
                                fig = create_projection_chart(
                                    config['name'],
                                    result['current'],
                                    result['target'],
                                    result['regression']
                                )
                                # Make chart bigger
                                fig.update_layout(
                                    height=500,
                                    font=dict(size=16),
                                    title_font_size=24
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Add metrics without using columns
                                st.markdown("### 📊 Regression Statistics")
                                
                                # Use HTML for side-by-side metrics instead of columns
                                st.markdown(f"""
                                <div class="metrics-row">
                                    <div style="display: inline-block; width: 30%; margin: 0 1.5%; text-align: center;">
                                        <h4>Slope</h4>
                                        <h2>{result['regression']['slope']:.4f}</h2>
                                    </div>
                                    <div style="display: inline-block; width: 30%; margin: 0 1.5%; text-align: center;">
                                        <h4>R² Score</h4>
                                        <h2>{result['regression']['r2']:.3f}</h2>
                                    </div>
                                    <div style="display: inline-block; width: 30%; margin: 0 1.5%; text-align: center;">
                                        <h4>Trend</h4>
                                        <h2>{'📈 Increasing' if result['trend'] == 'increasing' else '📉 Decreasing'}</h2>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Add interpretation
                                if result['regression']['r2'] > 0.7:
                                    st.success("Strong historical trend")
                                elif result['regression']['r2'] > 0.4:
                                    st.warning("Moderate historical trend")
                                else:
                                    st.error("Weak historical trend")
                    
                    # Download results - also centered
                    st.write("")
                    csv = pd.DataFrame(summary_data).to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"{country_code}_healthcare_targets_{CURRENT_YEAR}.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("No results could be calculated. Please check the data availability for this country.")
            else:
                st.warning("Please enter at least one target value.")
else:
    if country_code:
        st.info("👆 Enter target values and click 'Calculate Projections' to see when they might be achieved.")