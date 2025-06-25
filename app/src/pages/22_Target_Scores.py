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
from modules.style import style_sidebar, set_background_color


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
set_background_color() 
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

def regression_params(country_code, data_code):
    """Get regression parameters for a country and indicator"""
    try:
        api_url = f"{API_BASE_URL}/ml/regression/{country_code},{data_code}"
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
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        text-align: center;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:hover {
        border-color: #097969;
    }
    
    /* Current values card */
    .current-values-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(224, 224, 224, 0.5);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Target input card */
    .target-input-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(224, 224, 224, 0.5);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Results section styling */
    .results-header {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin: 2rem auto;
        color: #1f2937;
    }
    
    /* Download button styling */
    .stDownloadButton {
        display: flex;
        justify-content: center;
        margin: 3rem auto;
    }
    
    .stDownloadButton button {
        font-size: 1.2rem !important;
        padding: 0.75rem 2rem !important;
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        border-radius: 30px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3);
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(9, 121, 105, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🎯 Healthcare Target Calculator</h1>
        <div class="page-subtitle">Set ambitious healthcare goals and track when they'll be achieved</div>
    </div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown(f"""
    <div class="welcome-box">
        <div class="welcome-name">Welcome back, {st.session_state.get('name', 'Guest')}! 👋</div>
        <div>Let's set healthcare targets and see when your country might achieve them based on current trends.</div>
    </div>
""", unsafe_allow_html=True)

# Quick Start Guide
st.markdown("""
    <div class="instructions-card">
        <strong>🎯 Quick Start Guide:</strong>
        <ol style="margin: 0.5rem 0 0 1rem; padding-left: 1rem;">
            <li>Select a country to analyze</li>
            <li>Review current healthcare indicators</li>
            <li>Set your target values for each metric</li>
            <li>Click "Calculate Projections" to see when targets will be reached</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# How it works expander
with st.expander("📚 Learn How This Tool Works"):
    st.markdown("""
    ### 🔍 Understanding Target Projections
    
    This tool helps you set long-term healthcare goals and estimates achievement timelines based on data-driven analysis.
    
    ---
    
    ### 📊 How Our Projections Work
    
    **Linear Regression Analysis** 📈  
    We analyze historical trends for each healthcare indicator using statistical modeling
    
    **Trend Projection** 📉  
    Future values are projected based on the historical rate of change
    
    **Target Achievement** 🎯  
    We calculate when your target value will be reached if current trends continue
    
    ---
    
    ### 🏥 Available Healthcare Indicators
    
    **Life Expectancy** - Average years of life expected at birth  
    **Infant Mortality** - Deaths under age 1 per 1,000 live births  
    **Live Births** - Birth rate per 1,000 population  
    **General Practitioners** - Healthcare workforce per 10,000 people  
    **Health Expenditure** - Total spending per capita in USD  
    **Impoverished Households** - Percentage affected by healthcare costs  
    
    ---
    
    ### ⚠️ Important Considerations
    
    - **Projections assume historical trends continue** unchanged
    - **Major policy changes** or events can alter these trajectories
    - **Use as planning estimates**, not guaranteed outcomes
    - **R² scores indicate** the reliability of historical trends
    
    ---
    
    ### 💡 Pro Tips
    
    - Set **ambitious but realistic** targets
    - Consider **regional benchmarks** when setting goals
    - Review projections **regularly** as new data becomes available
    - Use the **detailed analysis** tab for deeper insights
    """)

# Fetch countries
country_list = fetch_countries()

# Country selection
st.markdown('<div class="section-header">🌍 Step 1: Select Country to Analyze</div>', unsafe_allow_html=True)

chosen_country = st.selectbox(
    "Choose a country:",
    country_list,
    index=None,
    placeholder="Select a country...",
    help="Choose the country you want to set healthcare targets for"
)

# Extract country code
country_code = None
current_values = None
if chosen_country:
    country_code = chosen_country.split('-')[-1]
    
    # Fetch current values
    with st.spinner("Loading current healthcare indicators..."):
        current_values = fetch_current_values(country_code)

# Show current values if available
if current_values:
    st.markdown('<div class="section-header">📊 Step 2: Review Current Healthcare Status</div>', unsafe_allow_html=True)
    
    # Create metrics display
    metric_cols = st.columns(3)
    
    for idx, (key, config) in enumerate(FEATURES_CONFIG.items()):
        col_idx = idx % 3
        
        # Get value from flattened data
        display_key = config['display_key']
        actual_key = get_best_matching_key(display_key, current_values)
        display_value = current_values.get(actual_key)
        
        with metric_cols[col_idx]:
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
    st.caption("**Total Health Expenditure per Capita (USD)")
    st.caption("++Live births per 1,000 population")
    st.markdown('</div>', unsafe_allow_html=True)

# Target value inputs
if country_code:
    st.markdown('<div class="section-header">🎯 Step 3: Set Your Target Values</div>', unsafe_allow_html=True)
    
    # Create input columns
    input_cols = st.columns(3)
    target_values = {}
    
    for idx, (key, config) in enumerate(FEATURES_CONFIG.items()):
        col_idx = idx % 3
        with input_cols[col_idx]:
            # Get current value for reference
            display_key = config['display_key']
            actual_key = get_best_matching_key(display_key, current_values) if current_values else None
            current_val = current_values.get(actual_key) if current_values and actual_key else None
            
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate button
    st.write("")
    col_calc, col_empty = st.columns([1, 3])
    
    with col_calc:
        if st.button("🔮 Calculate Projections", type="primary", use_container_width=True):
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
                        regression_data = regression_params(country_code, FEATURES_CONFIG[key]['code'])
                        
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
                if results:
                    st.write("")
                    st.write("---")
                    
                    # Big centered title
                    st.markdown('<h1 class="results-header">📈 Projection Results</h1>', unsafe_allow_html=True)
                    
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["📊 Summary", "📈 Detailed Analysis"])
                    
                    with tab1:
                        # Summary table
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
                                
                                # Add metrics
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Slope", f"{result['regression']['slope']:.4f}")
                                
                                with col2:
                                    st.metric("R² Score", f"{result['regression']['r2']:.3f}")
                                
                                with col3:
                                    trend_emoji = '📈' if result['trend'] == 'increasing' else '📉'
                                    st.metric("Trend", f"{trend_emoji} {result['trend'].capitalize()}")
                                
                                # Add interpretation
                                if result['regression']['r2'] > 0.7:
                                    st.success("✅ Strong historical trend - High confidence in projection")
                                elif result['regression']['r2'] > 0.4:
                                    st.warning("⚠️ Moderate historical trend - Medium confidence in projection")
                                else:
                                    st.error("❌ Weak historical trend - Low confidence in projection")
                    
                    # Download results
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
                st.warning("⚠️ Please enter at least one target value.")
else:
    if chosen_country:
        st.info("👆 Enter target values and click 'Calculate Projections' to see when they might be achieved.")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <small>💡 Tip: Set ambitious but achievable targets based on regional benchmarks</small>
    </div>
""", unsafe_allow_html=True)