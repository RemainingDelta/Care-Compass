import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import requests
import random
from streamlit_extras.stateful_button import button
import json

from modules.style import style_sidebar, set_background_color
 
style_sidebar()
set_background_color()
SideBarLinks()

userID = st.session_state.get('user_id')

# Custom CSS for consistent styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #fafafa;
    }
    
    /* Header styling */
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
    
    /* Selector title */
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
    
    /* Info sections - more compact */
    .info-section {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(224, 224, 224, 0.5);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #097969;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
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
    
    /* Similar countries card */
    .similar-countries-card {
        background: linear-gradient(135deg, rgba(9, 121, 105, 0.05) 0%, rgba(10, 157, 122, 0.05) 100%);
        border: 1px solid rgba(9, 121, 105, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        height: fit-content;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .similar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #097969;
        margin-bottom: 1.5rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .country-score-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 0.5rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
        background: rgba(255, 255, 255, 0.5);
    }
    
    .country-score-item:hover {
        background: rgba(255, 255, 255, 0.8);
        transform: translateX(5px);
    }
    
    .country-score-item:last-child {
        margin-bottom: 0;
    }
    
    .country-rank {
        background: #097969;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        margin-right: 0.75rem;
        flex-shrink: 0;
    }
    
    .country-rank.gold {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #333;
    }
    
    .country-rank.silver {
        background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
        color: #333;
    }
    
    .country-rank.bronze {
        background: linear-gradient(135deg, #CD7F32 0%, #B87333 100%);
        color: white;
    }
    
    .country-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex: 1;
    }
    
    .country-flag {
        font-size: 1.5rem;
        line-height: 1;
    }
    
    .country-name {
        font-weight: 600;
        color: #2c3e50;
        font-size: 0.95rem;
    }
    
    .country-code {
        font-size: 0.75rem;
        color: #6c757d;
        margin-left: 0.25rem;
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    
    .country-score-item:hover .country-code {
        opacity: 1;
    }
    
    .score-badge {
        background: #097969;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Article cards */
    .article-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #097969;
        margin: 2rem 0 1.5rem 0;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
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
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 1.05rem;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #097969;
    }
    
    /* Article styling */
    div[data-testid="stContainer"] {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stContainer"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Aggressively hide empty containers */
    div[data-testid="stContainer"]:empty,
    div[data-testid="stContainer"]:not(:has(*)) {
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }
    
    /* Hide containers that only have borders but no content */
    div[data-testid="stContainer"][style*="border"]:not(:has(img)):not(:has(p)):not(:has(span)):not(:has(a)) {
        display: none !important;
    }
    
    /* Hide any element with border but no actual content */
    div[style*="border: 1px solid"]:empty {
        display: none !important;
    }
    
    /* Hide empty containers */
    div[data-testid="stContainer"]:empty {
        display: none !important;
    }
    
    /* Remove default streamlit padding on empty elements */
    .element-container:has(> div:empty) {
        display: none !important;
    }
    
    /* Hide any empty column containers */
    div[data-testid="column"]:empty {
        display: none !important;
    }
    
    /* Hide containers with only whitespace */
    div[data-testid="stContainer"]:has(> :only-child:empty) {
        display: none !important;
    }
    
    /* Reduce spacing between sections */
    .row-widget.stSelectbox {
        margin-bottom: 1rem !important;
    }
    
    /* Remove gap after selectbox */
    .stSelectbox + div {
        margin-top: 0 !important;
    }
    
    /* Remove extra spacing from empty blocks */
    .block-container > div:empty {
        display: none !important;
    }
    
    /* Hide horizontal blocks that contain only empty elements */
    .stHorizontalBlock:has(> div:empty):not(:has(> div:not(:empty))) {
        display: none !important;
    }
    
    /* Remove margins from elements following empty ones */
    div:empty + div {
        margin-top: 0 !important;
    }
    
    /* Global rule to hide ANY empty element with a border */
    *[style*="border"]:empty,
    *[style*="border"]:not(:has(*)) {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    /* Specifically target Streamlit's bordered containers */
    .element-container:has(> div[style*="border: 1px solid"]:empty) {
        display: none !important;
    }
    
    /* Remove any stray bordered divs */
    div[style*="border: 1px solid rgb(224, 224, 224)"]:empty {
        display: none !important;
    }
    
    /* Hide Streamlit's default container padding */
    .element-container:empty,
    .element-container:has(> :empty):not(:has(> :not(:empty))) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove empty write containers */
    .stMarkdown:empty {
        display: none !important;
    }
    
    /* Hide any container that only contains whitespace */
    .element-container:has(> .stMarkdown:empty) {
        display: none !important;
    }
    
    /* Remove padding from column containers when they start */
    div[data-testid="column"]:first-child {
        padding-top: 0 !important;
    }
    
    /* Hide info boxes that are empty */
    div[data-testid="stAlert"]:empty {
        display: none !important;
    }
    
    /* Remove top margin from first element in columns */
    div[data-testid="column"] > div:first-child {
        margin-top: 0 !important;
    }
    
    /* Ensure columns start flush with content */
    .stColumns {
        padding-top: 0 !important;
    }
    
    /* Remove any default spacing above section content */
    .info-section:first-child {
        margin-top: 0 !important;
    }
    
    .similar-countries-card {
        margin-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🌍 Country Healthcare Profiles</h1>
        <div class="page-subtitle">Explore comprehensive healthcare information and insights for countries worldwide</div>
    </div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown(f"""
    <div class="welcome-box">
        <div class="welcome-name">Welcome back, {st.session_state.get('name', 'Guest')}! 👋</div>
        <div>Let's explore healthcare systems from around the world.</div>
    </div>
""", unsafe_allow_html=True)

# Quick guide card
st.markdown("""
    <div class="instructions-card">
        <strong>🎯 Quick Start Guide:</strong>
        <ol style="margin: 0.5rem 0 0 1rem; padding-left: 1rem;">
            <li>Select a country from the dropdown below</li>
            <li>View comprehensive healthcare information</li>
            <li>Compare with similar healthcare systems</li>
            <li>Browse latest healthcare articles</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# Learn how it works expander
with st.expander("📚 Learn How This Tool Works"):
    st.markdown("""
    ### 🔍 Understanding Country Healthcare Profiles
    
    This tool provides comprehensive insights into healthcare systems worldwide:
    
    **📋 General Information**  
    Basic country demographics, economic indicators, and social context
    
    **🏥 Healthcare System Overview**  
    Detailed analysis of the country's healthcare infrastructure and services
    
    **🔗 Similar Healthcare Systems**  
    Countries with comparable healthcare characteristics based on 6 key factors
    
    **📰 Latest Healthcare Articles**  
    Current news and analysis about the country's healthcare system
    
    ---
    
    ### 📊 How We Calculate Similarity
    
    Countries are compared using the **Global Health Security Index** across:
    - Prevention capabilities
    - Health system quality
    - Rapid response readiness
    - Detection & reporting systems
    - International norms compliance
    - Risk environment factors
    
    The similarity scores help you discover countries with comparable healthcare strengths and challenges!
    """)

# Section title for country selection
st.markdown('<div class="selector-title">🌍 Select a Country to Explore</div>', unsafe_allow_html=True)

# Fetch countries
country_url = "http://host.docker.internal:4000/country/countries"  
country_list = []
country_code_list = []

try:
    response = requests.get(country_url)
    response.raise_for_status()
    data = response.json()
    
    country_list = [item["name"] for item in data]
    code_list = [item["code"] for item in data]
    country_code_list = [f"{item['name']} ({item['code']})" for item in data]
    
except requests.exceptions.RequestException as e:
    st.error("Failed to load countries. Please try again later.")
    logger.error(f"API request failed: {e}")

# Country selection
selected_country = st.selectbox(
    "Search or select a country:",
    country_code_list,
    index=None,
    placeholder="Choose a country...",
    help="Start typing to search"
)

# Once country is selected
if selected_country:
    # Extract country code
    start_index = selected_country.rfind('(') + 1
    end_index = selected_country.rfind(')')
    country_code = selected_country[start_index:end_index]
    country_name = selected_country[:start_index-2]
    
    # API endpoint
    API_URL = f"http://host.docker.internal:4000/country/{country_code}"
    
    try:
        # Fetch country details
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            country = response.json()
            
            # Main content area with two columns - direct layout, no spacing
            col1, col2 = st.columns([2.5, 1], gap="large")
            
            with col1:
                # General Information Section - direct rendering
                if country.get("info") and len(country["info"]) > 0 and country["info"][0].get("generalInfo"):
                    st.markdown(f"""
                        <div class="info-section">
                            <h2 class="section-title">📋 General Information</h2>
                            <p>{country["info"][0]["generalInfo"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Healthcare Information Section - direct rendering
                if country.get("info") and len(country["info"]) > 0 and country["info"][0].get("healthcareInfo"):
                    st.markdown(f"""
                        <div class="info-section">
                            <h2 class="section-title">🏥 Healthcare System Overview</h2>
                            <p>{country["info"][0]["healthcareInfo"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Similar Countries Sidebar
            with col2:
                            st.markdown('<div class="similar-title">🔗 Similar Healthcare Systems</div>', unsafe_allow_html=True)
                            st.markdown('<p style="text-align: center; font-size: 0.85rem; color: #6c757d; margin-bottom: 1rem;">Based on Global Health Security Index</p>', unsafe_allow_html=True)
                            
                            # Country flag mapping
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
                            
                            # Get country names mapping
                            country_names = {}
                            try:
                                # Use the already fetched country data
                                country_names = {item['code']: item['name'] for item in data}
                            except:
                                pass
                            
                            # Fetch similar countries
                            weights_dict = {
                                "Prevention": 0.95,
                                "Health System": 0.76,
                                "Rapid Response": 0.52,
                                "Detection & Reporting": 0.33,
                                "International Norms Compliance": 0.10,
                                "Risk Environment": 0.10
                            }
                            weights_json = json.dumps(weights_dict)
                            
                            similar_url = f"http://host.docker.internal:4000/ml/cosine/{country_code}/{weights_json}"
                            
                            try:
                                similar_response = requests.get(similar_url)
                                if similar_response.status_code == 200:
                                    similar_data = json.loads(similar_response.text)
                                    df_similar = pd.DataFrame(similar_data)
                                    sorted_similar = df_similar.sort_values(by='the_country_cosine', ascending=False)
                                    top_similar = sorted_similar[1:6]  # Exclude self
                                    
                                    for idx, (_, row) in enumerate(top_similar.iterrows(), 1):
                                        country_code_sim = row['Country']
                                        score_percent = f"{row['the_country_cosine'] * 100:.1f}%"
                                        flag = country_flags.get(country_code_sim, '🌍')
                                        country_name_sim = country_names.get(country_code_sim, country_code_sim)
                                        
                                        # Determine rank class
                                        rank_class = "gold" if idx == 1 else "silver" if idx == 2 else "bronze" if idx == 3 else ""
                                        
                                        st.markdown(f"""
                                            <div class="country-score-item">
                                                <div style="display: flex; align-items: center;">
                                                    <div class="country-rank {rank_class}">{idx}</div>
                                                    <div class="country-info">
                                                        <span class="country-flag">{flag}</span>
                                                        <span class="country-name">{country_name_sim}<span class="country-code">({country_code_sim})</span></span>
                                                    </div>
                                                </div>
                                                <span class="score-badge">{score_percent}</span>
                                            </div>
                                        """, unsafe_allow_html=True)
                                    
                                    # Add a subtle note at the bottom
                                    if len(top_similar) > 0:
                                        st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #6c757d; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(9, 121, 105, 0.1);">Higher percentages indicate more similar healthcare systems</p>', unsafe_allow_html=True)
                                else:
                                    st.info("Unable to load similar countries")
                            except Exception as e:
                                logger.error(f"Error fetching similar countries: {e}")
                                st.info("Similar countries data unavailable")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
            
            # Healthcare Articles Section
            # First, check if we should even attempt to show articles
            show_articles = False
            valid_articles = []
            
            try:
                articles_response = requests.get(f"http://host.docker.internal:4000/country/{country_code}/articles")
                if articles_response.status_code == 200:
                    articles_data = articles_response.json()
                    
                    # Thoroughly validate articles
                    if isinstance(articles_data, list):
                        for article in articles_data:
                            if (isinstance(article, dict) and 
                                article.get('title') and 
                                article.get('link') and
                                article.get('id') is not None):
                                valid_articles.append(article)
                        
                        show_articles = len(valid_articles) > 0
            except Exception as e:
                logger.error(f"Error fetching articles: {e}")
                show_articles = False
            
            # Only create UI elements if we have valid articles
            if show_articles:
                st.markdown(f'<h2 class="article-header">📰 Latest Healthcare Articles for {country_name}</h2>', unsafe_allow_html=True)
                
                # Create exactly the number of columns needed
                num_articles = len(valid_articles)
                if num_articles >= 3:
                    cols = st.columns(3, gap="medium")
                elif num_articles == 2:
                    cols = st.columns(2, gap="medium")
                else:
                    cols = [st.container()]  # Single article doesn't need columns
                
                for i, article in enumerate(valid_articles):
                    col_index = i % len(cols) if num_articles >= 3 else i
                    with cols[col_index]:
                        with st.container(border=True):
                            # Article image
                            if article.get('image_name'):
                                st.image(f"assets/{article['image_name']}", use_container_width=True)
                            
                            # Article title
                            st.markdown(f"**{article['title']}**")
                            
                            # Source and actions
                            col_a, col_b = st.columns([4, 1])
                            
                            with col_a:
                                st.caption(f"*{article.get('source', 'Unknown source')}*")
                                st.markdown(f"[Read more →]({article['link']})")
                            
                            with col_b:
                                if button("⭐", key=f"bookmark_{article['id']}", help="Save to favorites"):
                                    # Save favorite logic
                                    favorite_data = {
                                        "userID": userID,
                                        "articleID": article["id"]
                                    }
                                    favorite_url = "http://host.docker.internal:4000/country/articles/favorite"
                                    try:
                                        fav_response = requests.post(favorite_url, json=favorite_data)
                                        if fav_response.status_code == 201:
                                            st.success("Saved!")
                                        elif fav_response.status_code == 409:
                                            st.info("Already saved")
                                    except:
                                        pass
                
        elif response.status_code == 404:
            st.error("Country information not found")
        else:
            st.error("Unable to load country information. Please try again.")
            
    except requests.exceptions.RequestException as e:
        st.error("Connection error. Please check your internet and try again.")
        logger.error(f"API error: {e}")

else:
    # Show placeholder when no country is selected - more subtle
    st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #6c757d;">
            <p style="font-size: 1.1rem;">👆 Select a country above to view its healthcare profile</p>
        </div>
    """, unsafe_allow_html=True)