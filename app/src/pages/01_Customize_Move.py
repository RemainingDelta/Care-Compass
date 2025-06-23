import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import numpy as np
from modules.nav import SideBarLinks
import requests
import json
from streamlit_sortables import sort_items
import plotly.express as px 
import plotly.graph_objects as go

from modules.style import style_sidebar, set_background
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
    
    /* Section spacing */
    .section-spacing {
        margin-bottom: 1.5rem;
    }
    
    /* Country selector styling */
    .selector-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        margin-top: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Drag and drop section */
    .ranking-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
    }
    
    .ranking-subtitle {
        color: #6c757d;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    
    /* Sortable items styling */
    div[data-testid="sortable-item"] {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        cursor: move;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    div[data-testid="sortable-item"]:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3);
    }
    
    /* Weight adjustment section */
    .weights-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        margin-top: 1rem;
    }
    
    /* Individual weight item */
    .weight-item {
        background: rgba(255, 255, 255, 0.7);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid rgba(224, 224, 224, 0.7);
        transition: all 0.3s ease;
        position: relative;
        overflow: visible !important;
    }
    
    .weight-item:first-child {
        margin-top: 0.5rem;
        overflow: visible !important;
    }
    
    .weight-item:hover {
        background: rgba(255, 255, 255, 0.95);
        border-color: #097969;
        box-shadow: 0 2px 10px rgba(9, 121, 105, 0.1);
    }
    
    /* Add stacking context to ensure tooltips appear above other elements */
    .weight-label {
        font-weight: 600;
        color: #2c3e50;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        position: relative;
        z-index: 1;
        width: 100%;
    }
    
    .factor-name {
        position: relative;
        cursor: help;
        border-bottom: 1px dotted rgba(9, 121, 105, 0.5);
        display: inline-block;
        transition: all 0.2s ease;
        padding-bottom: 1px;
        font-weight: 600;
    }
    
    .factor-name::after {
        content: "ⓘ";
        font-size: 0.75rem;
        color: #097969;
        margin-left: 3px;
        opacity: 0.4;
        transition: opacity 0.3s ease;
        vertical-align: super;
        font-weight: normal;
    }
    
    .factor-name:hover {
        color: #097969;
        border-bottom-style: solid;
    }
    
    .factor-name:hover::after {
        opacity: 1;
    }
    
    /* Tooltip styling */
    .tooltip-container {
        position: relative;
        display: inline-flex;
        align-items: center;
    }
    
    /* Tooltip styling */
    .tooltip-container {
        position: relative;
        display: inline-block;
    }
    
    .tooltip-text {
        visibility: hidden;
        background-color: #2c3e50;
        color: white;
        text-align: left;
        padding: 12px 15px;
        border-radius: 8px;
        position: absolute;
        z-index: 1000;
        bottom: calc(100% + 10px);
        left: 0;
        min-width: 280px;
        max-width: 350px;
        font-size: 0.9rem;
        font-weight: 400;
        line-height: 1.5;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        opacity: 0;
        transition: opacity 0.2s, transform 0.2s;
        transform: translateY(5px);
        white-space: normal;
        pointer-events: none;
    }
    
    .tooltip-text::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 60px;
        border-width: 6px;
        border-style: solid;
        border-color: #2c3e50 transparent transparent transparent;
    }
    
    .tooltip-container:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
        transform: translateY(0);
        pointer-events: auto;
    }
    
    /* Adjust tooltip position for last 3 items to show below */
    .weight-item:nth-last-child(-n+3) .tooltip-text {
        bottom: auto;
        top: calc(100% + 10px);
    }
    
    .weight-item:nth-last-child(-n+3) .tooltip-text::after {
        top: auto;
        bottom: 100%;
        border-color: transparent transparent #2c3e50 transparent;
    }
    
    .rank-badge {
        background: #097969;
        color: white;
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        flex-shrink: 0;
        min-width: 28px;
        text-align: center;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #e8f5f0 0%, #097969 100%);
    }
    
    .stSlider > div > div > div > div > div {
        background: #097969;
        border: 3px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Results section */
    .results-section {
        padding: 2rem 0;
        margin-top: 2rem;
    }
    
    .results-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #097969;
        margin-bottom: 2rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .results-subtitle {
        font-size: 1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Match cards styling */
    .match-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(224, 224, 224, 0.7);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .match-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-color: #097969;
    }
    
    .match-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .match-rank {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .match-country {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
    }
    
    .match-score-container {
        text-align: right;
    }
    
    .match-score {
        font-size: 1.8rem;
        font-weight: 700;
        color: #097969;
    }
    
    .match-label {
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Top match special styling */
    .match-card:first-child {
        background: linear-gradient(135deg, rgba(9, 121, 105, 0.05) 0%, rgba(10, 157, 122, 0.05) 100%);
        border: 2px solid #097969;
    }
    
    .match-card:first-child .match-rank {
        background: gold;
        color: #2c3e50;
        font-size: 1.3rem;
    }
    
    /* Results summary box */
    .results-summary {
        background: linear-gradient(135deg, rgba(9, 121, 105, 0.05) 0%, rgba(10, 157, 122, 0.05) 100%);
        border: 1px solid rgba(9, 121, 105, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .summary-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #097969;
        margin-bottom: 0.5rem;
    }
    
    .summary-text {
        color: #2c3e50;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Visualization section */
    .viz-section {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid rgba(224, 224, 224, 0.5);
    }
    
    .viz-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Submit button */
    .stButton > button[type="primary"] {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem 3rem;
        border-radius: 30px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3);
        display: block;
        margin: 2rem auto;
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
    
    .stButton > button[type="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(9, 121, 105, 0.4);
    }
    
    /* Toggle switch styling */
    .stToggle > label {
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 1.05rem;
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
    }
    
    /* Success message */
    .stSuccess {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Add visual indicators for priority levels */
    .priority-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-left: auto;
        margin-right: 0.5rem;
        flex-shrink: 0;
    }
    
    /* Add country flag placeholder */
    .country-flag {
        width: 32px;
        height: 24px;
        background: #f0f0f0;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    
    /* Progress bar for match score */
    .match-progress {
        width: 100%;
        height: 6px;
        background: rgba(9, 121, 105, 0.1);
        border-radius: 3px;
        margin-top: 0.5rem;
        overflow: hidden;
    }
    
    .match-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #097969 0%, #0a9d7a 100%);
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    
    /* Ensure parent containers don't clip tooltips */
    .element-container {
        overflow: visible !important;
    }
    
    [data-testid="column"] {
        overflow: visible !important;
    }
    
    .stHorizontalBlock {
        overflow: visible !important;
    }
    
    .priority-high { background: #28a745; }
    .priority-medium { background: #ffc107; }
    .priority-low { background: #dc3545; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🏥 Customize Your Healthcare Journey</h1>
        <div class="page-subtitle">Design your ideal healthcare system by prioritizing what matters most to you</div>
    </div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown(f"""
    <div class="welcome-box">
        <div class="welcome-name">Welcome back, {st.session_state.get('name', 'Guest')}! 👋</div>
        <div>Let's find the perfect healthcare system that aligns with your priorities.</div>
    </div>
""", unsafe_allow_html=True)

# Instructions
st.markdown("""
    <div class="instructions-card">
        <strong>🎯 Quick Start Guide:</strong>
        <ol style="margin: 0.5rem 0 0 1rem; padding-left: 1rem;">
            <li>Select your current country from the dropdown</li>
            <li>Drag and drop the healthcare factors to rank them (1 = most important)</li>
            <li>Fine-tune the importance of each factor using the sliders</li>
            <li>Click Submit to see your personalized recommendations!</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# How it works expander
with st.expander("📚 Learn How This Tool Works"):
    st.markdown("""
    ### 🔍 Understanding the Healthcare Factors
    
    This tool analyzes **six core dimensions** from the Global Health Security Index:
    
    **1. 🛡️ Prevention**  
    Measures to prevent the emergence and spread of infectious diseases
    
    **2. 🔬 Detection & Reporting**  
    Capacity for early detection, testing, and transparent reporting
    
    **3. ⚡ Rapid Response**  
    Readiness and speed of response to health emergencies
    
    **4. 🏥 Health System**  
    Quality and accessibility of healthcare infrastructure
    
    **5. 🌍 International Norms Compliance**  
    Adherence to WHO and global health regulations
    
    **6. ⚠️ Risk Environment**  
    Social, political, and environmental vulnerability factors
    
    ---
    
    ### 📊 How We Calculate Your Matches
    
    Your rankings are converted into a **priority score system**:
    - **Rank 1** → 90-100 points (Highest priority)
    - **Rank 2** → 70-90 points
    - **Rank 3** → 50-70 points
    - **Rank 4** → 30-50 points
    - **Rank 5** → 10-30 points
    - **Rank 6** → 0-10 points (Lowest priority)
    
    We use **cosine similarity** to find countries whose healthcare profiles best match your priorities!
    """)

# Initialize session state
if "factor_weights" not in st.session_state:
    st.session_state.factor_weights = {}
if "dragged_factors" not in st.session_state:
    st.session_state.dragged_factors = [
        "Prevention",
        "Health System",
        "Rapid Response",
        "Detection & Reporting",
        "International Norms Compliance",
        "Risk Environment"
    ]
if "slot_weights" not in st.session_state:
    st.session_state.slot_weights = [100 - i * 20 for i in range(6)]

# API setup
headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Fetch countries
API_URL = "http://web-api:4000/country/countries"
country_list = []

try:
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()
    country_list = [item["name"] for item in data]
except requests.exceptions.RequestException as e:
    st.error("Failed to load countries. Please try again later.")
    logger.error(f"API request failed: {e}")

# Country selector section
st.markdown('<div class="selector-title">🌍 Step 1: Select Your Current Country</div>', unsafe_allow_html=True)

chosen_country = st.selectbox(
    "Where are you currently located?",
    country_list,
    index=None,
    placeholder="Choose a country...",
    help="This helps us provide more relevant recommendations"
)

# Add spacing
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

# Ranking section
st.markdown('<div class="ranking-title">📊 Step 2: Rank Healthcare Factors by Importance</div>', unsafe_allow_html=True)
st.markdown('<div class="ranking-subtitle">Drag to reorder - your top priority should be at the top!</div>', unsafe_allow_html=True)

# Drag and drop interface
st.session_state.dragged_factors = sort_items(
    st.session_state.dragged_factors,
    direction="vertical",
    key="drag_order"
)

# Add spacing
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

# Weight adjustment section
st.markdown('<div class="weights-title">⚖️ Step 3: Fine-tune Your Priorities</div>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">💡 Hover over factor names to see detailed descriptions</p>', unsafe_allow_html=True)

# Fetch factor descriptions
factor_descriptions = {}
try:
    response = requests.get("http://host.docker.internal:4000/country/factor_descriptions", headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            # Map factor names to their descriptions
            key = item["name"].lower().replace(" ", "").replace("&", "and").strip()
            factor_descriptions[key] = item["description"]
            logger.info(f"Loaded description for: {key}")
except Exception as e:
    logger.error(f"Failed to fetch factor descriptions: {e}")

# Load saved preferences if available
if 'user_id' in st.session_state:
    def fetch_user_preferences(user_id):
        try:
            url = f"http://host.docker.internal:4000/users/{user_id}/preferences"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Exception while fetching preferences: {e}")
            return None
    
    prefs = fetch_user_preferences(st.session_state['user_id'])
    if prefs:
        weights_from_backend = {
            "Prevention": prefs["preventionWeight"] / 100,
            "Detection & Reporting": prefs["detectReportWeight"] / 100,
            "Rapid Response": prefs["rapidRespWeight"] / 100,
            "Health System": prefs["healthSysWeight"] / 100,
            "International Norms Compliance": prefs["intlNormsWeight"] / 100,
            "Risk Environment": prefs["riskEnvWeight"] / 100
        }
        st.session_state["initial_preferences"] = weights_from_backend

# Weight adjustment interface
for i in range(6):
    factor = st.session_state.dragged_factors[i]
    
    # Create weight item container
    st.markdown(f'<div class="weight-item">', unsafe_allow_html=True)
    
    # Set keys and defaults
    val_key = f"val_{i}"
    initial_weight = st.session_state.get("initial_preferences", {}).get(factor, None)
    
    if val_key not in st.session_state:
        st.session_state[val_key] = int(initial_weight * 10) if initial_weight is not None else 5
    
    slider_val = st.session_state[val_key]
    
    # Get tooltip
    tooltip_keys = {
        "prevention": "prevention",
        "healthsystem": "healthsystem",
        "rapidresponse": "rapidresponse",
        "detection&reporting": "detectionandreporting",
        "internationalnormscompliance": "compliancewithinternationalnorms",
        "riskenvironment": "riskenvironment"
    }
    lookup_key = tooltip_keys.get(factor.lower().replace(" ", "").strip(), "")
    desc = factor_descriptions.get(lookup_key, "")
    
    # Fallback descriptions if API doesn't provide them
    if not desc:
        fallback_descriptions = {
            "Prevention": "Measures and policies to prevent the emergence and spread of infectious diseases",
            "Health System": "The quality, accessibility, and robustness of healthcare infrastructure and services",
            "Rapid Response": "The readiness and speed of response to health emergencies and outbreaks",
            "Detection & Reporting": "Capacity for early detection, testing, and transparent reporting of health threats",
            "International Norms Compliance": "Adherence to WHO regulations and global health standards",
            "Risk Environment": "Social, political, and environmental factors that affect health vulnerability"
        }
        desc = fallback_descriptions.get(factor, f"Priority ranking for {factor}")
    
    # Layout - adjusted for better spacing
    col_label, col_slider, col_input = st.columns([4.5, 5.5, 2])
    
    with col_label:
        priority_class = "priority-high" if i < 2 else "priority-medium" if i < 4 else "priority-low"
        # Create tooltip HTML - factor name stays visible, description in tooltip
        tooltip_desc = desc if desc else f"Configure priority for {factor} in the healthcare system"
        tooltip_html = f"""
            <div class="weight-label">
                <span class="rank-badge">{i+1}</span>
                <div class="tooltip-container">
                    <span class="factor-name">{factor}</span>
                    <span class="tooltip-text">{tooltip_desc}</span>
                </div>
                <span class="priority-indicator {priority_class}"></span>
            </div>
        """
        st.markdown(tooltip_html, unsafe_allow_html=True)
    
    with col_slider:
        new_slider = st.slider(
            label="Importance",
            min_value=0,
            max_value=10,
            value=slider_val,
            key=f"slider_{i}",
            help=f"Adjust the importance of {factor}"
        )
    
    with col_input:
        new_input = st.number_input(
            label="Value",
            min_value=0,
            max_value=10,
            value=slider_val,
            step=1,
            key=f"input_{i}"
        )
    
    # Sync slider/input
    if new_input != st.session_state[val_key]:
        st.session_state[val_key] = new_input
    elif new_slider != st.session_state[val_key]:
        st.session_state[val_key] = new_slider
    
    # Calculate weighted priority
    if i == 0:
        true_weight = 90 + st.session_state[val_key]
    elif i == 5:
        true_weight = st.session_state[val_key]
    else:
        true_weight = 90 - 20 * i + 2 * st.session_state[val_key]
    
    st.session_state.slot_weights[i] = true_weight
    st.markdown('</div>', unsafe_allow_html=True)

# Build weights dictionary
weights_dict = {}
for i in range(6):
    factor = st.session_state.dragged_factors[i]
    weight = st.session_state.slot_weights[i]
    weights_dict[factor] = float(weight/100)

# Add spacing before submit button
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

# Submit button and visualization toggle
col1, col2 = st.columns([1, 2])
with col1:
    submit = st.button("🚀 Find My Matches", type="primary", use_container_width=True)
with col2:
    on = st.toggle("Switch View: Bar Chart / World Map", help="Toggle between different visualization styles")

# Results processing
if submit and chosen_country:
    with st.spinner('🔍 Analyzing healthcare systems worldwide...'):
        # Prepare weights
        weights_dict_obj = weights_dict
        weights_dict_json = json.dumps(weights_dict)
        
        # Call similarity API
        api_url = f"http://host.docker.internal:4000/ml/cosine/{chosen_country}/{weights_dict_json}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Save preferences if user is logged in
                if 'user_id' in st.session_state:
                    preferences_payload = {
                        "preventionWeight": weights_dict_obj.get("Prevention", 1.0) * 100,
                        "detectReportWeight": weights_dict_obj.get("Detection & Reporting", 1.0) * 100,
                        "rapidRespWeight": weights_dict_obj.get("Rapid Response", 1.0) * 100,
                        "healthSysWeight": weights_dict_obj.get("Health System", 1.0) * 100,
                        "intlNormsWeight": weights_dict_obj.get("International Norms Compliance", 1.0) * 100,
                        "riskEnvWeight": weights_dict_obj.get("Risk Environment", 1.0) * 100
                    }
                    
                    try:
                        save_url = f"http://host.docker.internal:4000/users/{st.session_state['user_id']}/preferences"
                        save_response = requests.put(save_url, json=preferences_payload, headers=headers, timeout=10)
                        if save_response.status_code == 200:
                            st.success("✅ Your preferences have been saved!")
                    except Exception as e:
                        logger.warning(f"Error saving preferences: {e}")
                
                # Process results
                data = response.text
                data_dict = json.loads(data)
                df_similar = pd.DataFrame(data_dict)
                sorted_df_similar = df_similar.sort_values(by='the_country_cosine', ascending=False)
                st.session_state['similar_df'] = sorted_df_similar
                
                # Get country names mapping
                country_names = {}
                try:
                    country_response = requests.get("http://host.docker.internal:4000/country/countries", headers=headers, timeout=10)
                    if country_response.status_code == 200:
                        countries_data = country_response.json()
                        country_names = {item['code']: item['name'] for item in countries_data}
                except Exception as e:
                    logger.error(f"Failed to fetch country names: {e}")
                
                # Country flag emoji mapping (common countries)
                country_flags = {
                    'USA': '🇺🇸', 'GBR': '🇬🇧', 'CAN': '🇨🇦', 'AUS': '🇦🇺', 'DEU': '🇩🇪',
                    'FRA': '🇫🇷', 'JPN': '🇯🇵', 'KOR': '🇰🇷', 'CHN': '🇨🇳', 'IND': '🇮🇳',
                    'BRA': '🇧🇷', 'MEX': '🇲🇽', 'ITA': '🇮🇹', 'ESP': '🇪🇸', 'NLD': '🇳🇱',
                    'BEL': '🇧🇪', 'CHE': '🇨🇭', 'SWE': '🇸🇪', 'NOR': '🇳🇴', 'DNK': '🇩🇰',
                    'FIN': '🇫🇮', 'AUT': '🇦🇹', 'POL': '🇵🇱', 'PRT': '🇵🇹', 'GRC': '🇬🇷',
                    'TUR': '🇹🇷', 'ISR': '🇮🇱', 'SGP': '🇸🇬', 'NZL': '🇳🇿', 'IRL': '🇮🇪',
                    'LUX': '🇱🇺', 'ISL': '🇮🇸', 'CZE': '🇨🇿', 'SVK': '🇸🇰', 'HUN': '🇭🇺',
                    'ROU': '🇷🇴', 'BGR': '🇧🇬', 'HRV': '🇭🇷', 'SVN': '🇸🇮', 'LTU': '🇱🇹',
                    'LVA': '🇱🇻', 'EST': '🇪🇪', 'CYP': '🇨🇾', 'MLT': '🇲🇹', 'ZAF': '🇿🇦',
                    'ARG': '🇦🇷', 'CHL': '🇨🇱', 'COL': '🇨🇴', 'PER': '🇵🇪', 'VEN': '🇻🇪',
                    'EGY': '🇪🇬', 'MAR': '🇲🇦', 'NGA': '🇳🇬', 'KEN': '🇰🇪', 'GHA': '🇬🇭',
                    'ETH': '🇪🇹', 'TZA': '🇹🇿', 'UGA': '🇺🇬', 'DZA': '🇩🇿', 'SDN': '🇸🇩',
                    'AGO': '🇦🇴', 'MOZ': '🇲🇿', 'MDG': '🇲🇬', 'CMR': '🇨🇲', 'CIV': '🇨🇮',
                    'NER': '🇳🇪', 'BFA': '🇧🇫', 'MLI': '🇲🇱', 'MWI': '🇲🇼', 'ZMB': '🇿🇲',
                    'SEN': '🇸🇳', 'ZWE': '🇿🇼', 'RWA': '🇷🇼', 'TUN': '🇹🇳', 'LBY': '🇱🇾',
                    'MUS': '🇲🇺', 'BWA': '🇧🇼', 'NAM': '🇳🇦', 'GAB': '🇬🇦', 'TGO': '🇹🇬',
                    'BEN': '🇧🇯', 'GNB': '🇬🇼', 'SLE': '🇸🇱', 'LBR': '🇱🇷', 'MRT': '🇲🇷',
                    'GMB': '🇬🇲', 'GNQ': '🇬🇶', 'SWZ': '🇸🇿', 'DJI': '🇩🇯', 'COM': '🇰🇲',
                    'CPV': '🇨🇻', 'STP': '🇸🇹', 'SYC': '🇸🇨', 'ARE': '🇦🇪', 'SAU': '🇸🇦',
                    'QAT': '🇶🇦', 'KWT': '🇰🇼', 'BHR': '🇧🇭', 'OMN': '🇴🇲', 'JOR': '🇯🇴',
                    'LBN': '🇱🇧', 'YEM': '🇾🇪', 'IRQ': '🇮🇶', 'SYR': '🇸🇾', 'IRN': '🇮🇷',
                    'PAK': '🇵🇰', 'AFG': '🇦🇫', 'BGD': '🇧🇩', 'LKA': '🇱🇰', 'MMR': '🇲🇲',
                    'THA': '🇹🇭', 'VNM': '🇻🇳', 'KHM': '🇰🇭', 'LAO': '🇱🇦', 'MYS': '🇲🇾',
                    'IDN': '🇮🇩', 'PHL': '🇵🇭', 'BRN': '🇧🇳', 'TLS': '🇹🇱', 'MNG': '🇲🇳',
                    'KAZ': '🇰🇿', 'UZB': '🇺🇿', 'TKM': '🇹🇲', 'KGZ': '🇰🇬', 'TJK': '🇹🇯',
                    'RUS': '🇷🇺', 'UKR': '🇺🇦', 'BLR': '🇧🇾', 'MDA': '🇲🇩', 'ARM': '🇦🇲',
                    'GEO': '🇬🇪', 'AZE': '🇦🇿', 'ALB': '🇦🇱', 'MKD': '🇲🇰', 'SRB': '🇷🇸',
                    'MNE': '🇲🇪', 'BIH': '🇧🇦', 'AND': '🇦🇩', 'MCO': '🇲🇨', 'LIE': '🇱🇮',
                    'SMR': '🇸🇲', 'VAT': '🇻🇦', 'PNG': '🇵🇬', 'FJI': '🇫🇯', 'SLB': '🇸🇧',
                    'VUT': '🇻🇺', 'NCL': '🇳🇨', 'PYF': '🇵🇫', 'WSM': '🇼🇸', 'KIR': '🇰🇮',
                    'TON': '🇹🇴', 'FSM': '🇫🇲', 'PLW': '🇵🇼', 'MHL': '🇲🇭', 'NRU': '🇳🇷',
                    'TUV': '🇹🇻', 'COK': '🇨🇰', 'NIU': '🇳🇺', 'TKL': '🇹🇰', 'GUM': '🇬🇺',
                    'ASM': '🇦🇸', 'MNP': '🇲🇵', 'PRY': '🇵🇾', 'URY': '🇺🇾', 'ECU': '🇪🇨',
                    'BOL': '🇧🇴', 'GUY': '🇬🇾', 'SUR': '🇸🇷', 'GUF': '🇬🇫', 'HTI': '🇭🇹',
                    'DOM': '🇩🇴', 'CUB': '🇨🇺', 'JAM': '🇯🇲', 'TTO': '🇹🇹', 'BRB': '🇧🇧',
                    'DMA': '🇩🇲', 'GRD': '🇬🇩', 'VCT': '🇻🇨', 'LCA': '🇱🇨', 'ATG': '🇦🇬',
                    'KNA': '🇰🇳', 'BHS': '🇧🇸', 'BLZ': '🇧🇿', 'CRI': '🇨🇷', 'SLV': '🇸🇻',
                    'GTM': '🇬🇹', 'HND': '🇭🇳', 'NIC': '🇳🇮', 'PAN': '🇵🇦'
                }
                
                # Display results
                st.markdown('<div class="results-section">', unsafe_allow_html=True)
                st.markdown("""
                    <div class="results-title">
                        <span>🎯</span>
                        <span>Your Top Healthcare Matches</span>
                    </div>
                    <div class="results-subtitle">
                        Based on your priorities, these countries offer healthcare systems that best align with your preferences
                    </div>
                """, unsafe_allow_html=True)
                
                # Show top 5 matches
                top_matches = sorted_df_similar[1:6]  # Exclude the selected country itself
                
                for idx, (_, row) in enumerate(top_matches.iterrows(), 1):
                    match_score = row['the_country_cosine']
                    match_percentage = f"{match_score * 100:.1f}"
                    country_code = row['Country']
                    country_name = country_names.get(country_code, country_code)
                    
                    # Create match card
                    rank_emoji = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else str(idx)
                    
                    card_html = f"""
                        <div class="match-card">
                            <div class="match-info">
                                <div class="match-rank">{rank_emoji if idx <= 3 else idx}</div>
                                <div class="match-country">{country_name}</div>
                            </div>
                            <div class="match-score-container">
                                <div class="match-score">{match_percentage}%</div>
                                <div class="match-label">Match Score</div>
                            </div>
                        </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Visualization
                if on and 'similar_df' in st.session_state:
                    # World map visualization
                    st.markdown('<div class="viz-section">', unsafe_allow_html=True)
                    st.markdown('<div class="viz-title">🗺️ Healthcare System Compatibility Map</div>', unsafe_allow_html=True)
                    
                    country_url = "http://host.docker.internal:4000/country/countries"
                    try:
                        response = requests.get(country_url, headers=headers, timeout=10)
                        response.raise_for_status()
                        data = response.json()
                        
                        # Create a dictionary for efficient lookup
                        code_to_name = {item['code']: item['name'] for item in data}
                        
                        # Create a copy to avoid modifying the original
                        map_df = sorted_df_similar.copy()
                        
                        # Add country names using dictionary lookup
                        map_df['name'] = map_df['Country'].map(code_to_name)
                        
                        # Handle any missing country names
                        map_df['name'] = map_df['name'].fillna(map_df['Country'])
                        
                        # Create choropleth map
                        fig1 = px.choropleth(
                            map_df,
                            locations='Country',
                            locationmode='ISO-3',
                            color='the_country_cosine',
                            color_continuous_scale="Viridis",
                            range_color=(0.7, 1),
                            scope='world',
                            labels={'the_country_cosine': 'Similarity Score'},
                            hover_name='name',
                            hover_data={'the_country_cosine': ':.3f', 'Country': False}
                        )
                        
                        fig1.update_geos(
                            showcountries=True,
                            showcoastlines=True,
                            showland=True,
                            landcolor='lightgray',
                            coastlinecolor='white',
                            projection_type='natural earth'
                        )
                        
                        fig1.update_layout(
                            margin={"r":0,"t":0,"l":0,"b":0},
                            height=600,
                            geo=dict(
                                showframe=False,
                                showcoastlines=True,
                                bgcolor='rgba(0,0,0,0)'
                            ),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        
                        # Fixed colorbar configuration - removed titleside
                        fig1.update_coloraxes(
                            colorbar=dict(
                                title="Match Score",
                                tickmode="linear",
                                tick0=0.7,
                                dtick=0.05,
                                tickformat=".0%"
                            )
                        )
                        
                        st.plotly_chart(fig1, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        logger.error(f"Map visualization error: {e}")
                        st.error(f"Unable to load the world map visualization. Error: {str(e)}")
                        # Show debug info if needed
                        if st.checkbox("Show debug info"):
                            st.write("Similar countries data shape:", sorted_df_similar.shape)
                            st.write("Sample data:", sorted_df_similar.head())
                            st.write("Columns:", sorted_df_similar.columns.tolist())
                else:
                    # Bar chart visualization
                    st.markdown('<div class="viz-section">', unsafe_allow_html=True)
                    st.markdown('<div class="viz-title">📊 Top Healthcare Matches Comparison</div>', unsafe_allow_html=True)
                    
                    bar_chart_display = sorted_df_similar[1:6].copy()
                    
                    # Add country names to bar chart
                    bar_chart_countries = []
                    for _, row in bar_chart_display.iterrows():
                        country_code = row['Country']
                        country_name = country_names.get(country_code, country_code)
                        bar_chart_countries.append(country_name)
                    
                    bar_chart_display['Country_Name'] = bar_chart_countries
                    
                    fig = px.bar(
                        bar_chart_display,
                        x='Country_Name',
                        y='the_country_cosine',
                        color='the_country_cosine',
                        color_continuous_scale="Viridis",
                        labels={'the_country_cosine': 'Similarity Score', 'Country_Name': 'Country'},
                        hover_data={'the_country_cosine': ':.3f'}
                    )
                    
                    fig.update_yaxes(range=[0.85, 1], tickformat=".0%")
                    fig.update_layout(
                        xaxis_title="Country",
                        yaxis_title="Match Score",
                        showlegend=False,
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(
                            gridcolor='rgba(128,128,128,0.2)',
                            zerolinecolor='rgba(128,128,128,0.2)'
                        )
                    )
                    
                    # Add value labels on bars
                    fig.update_traces(
                        texttemplate='%{y:.1%}',
                        textposition='outside',
                        textfont_size=12
                    )
                    
                    fig.update_coloraxes(showscale=False)
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                st.error("😔 Unable to process your request. Please try again.")
                
        except Exception as e:
            st.error("🚫 Connection error. Please check your internet and try again.")
            logger.error(f"API error: {e}")

elif submit and not chosen_country:
    st.warning("⚠️ Please select your current country before submitting!")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <small>💡 Tip: Your preferences are automatically saved when you submit!</small>
    </div>
""", unsafe_allow_html=True)