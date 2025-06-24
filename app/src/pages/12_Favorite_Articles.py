import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from modules.style import style_sidebar, set_background_color


style_sidebar()
set_background_color() 
SideBarLinks()

# Custom CSS matching Country Healthcare Profiles page exactly
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #fafafa;
    }
    
    /* Header styling - matching Country page exactly */
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
    
    /* Style the expander */
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
    
    /* Articles count message */
    .articles-count {
        background-color: #f0f4f8;
        border: 1px solid #4a90e2;
        color: #2c5282;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.05rem;
    }
    
    /* Articles container */
    .articles-empty {
        background: #e6f3ff;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        border: 1px solid #b3d9ff;
        margin-bottom: 2rem;
    }
    
    /* Success message styling */
    div[data-testid="stAlert"] {
        background-color: #f0f4f8 !important;
        border: 1px solid #4a90e2 !important;
        color: #2c5282 !important;
        margin-bottom: 1.5rem;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Override default success alert colors */
    div[data-testid="stAlert"][data-baseweb="notification"] {
        background-color: #f0f4f8 !important;
    }
    
    .st-emotion-cache-1kyxreq {
        background-color: #f0f4f8 !important;
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
    
    /* Reduce spacing between sections */
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header - matching Country page exactly
st.markdown("""
    <div class="page-header">
        <h1 class="page-title">📰 Your Healthcare Article Collection</h1>
        <div class="page-subtitle">Save and organize articles that matter most to your healthcare journey</div>
    </div>
""", unsafe_allow_html=True)

# Authentication check
if not st.session_state.get("authenticated"):
    st.warning("You must be logged in to access this page.")
    st.stop()

# Get user ID and username
userID = st.session_state.get("user_id")
username = st.session_state.get("name", "User")  # Use 'name' from session state like Country page

if not userID:
    st.error("Could not find user ID in session. Please log in again.")
    st.stop()

# Welcome message - matching Country page style
st.markdown(f"""
    <div class="welcome-box">
        <div class="welcome-name">Welcome back, {username}! 👋</div>
        <div>Build your personal library of healthcare insights by favoriting articles from different countries.</div>
    </div>
""", unsafe_allow_html=True)

# Quick guide card - matching Country page exactly
st.markdown("""
    <div class="instructions-card">
        <strong>🎯 Quick Start Guide:</strong>
        <ol style="margin: 0.5rem 0 0 1rem; padding-left: 1rem;">
            <li>Navigate to any country page using the sidebar</li>
            <li>Browse through healthcare articles and reports</li>
            <li>Click the star icon to favorite articles you want to save</li>
            <li>Return here to access all your favorited content in one place</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# Learn How This Tool Works - Expandable Section
with st.expander("📚 Learn How This Tool Works"):
    st.markdown("""
    ### 🔍 Building Your Healthcare Knowledge Base
    
    This tool helps you create a personalized collection of healthcare articles and insights from around the world:
    
    **📋 How to Find Articles**  
    Navigate to any country page to discover healthcare articles, reports, and analysis specific to that nation
    
    **⭐ Save Your Favorites**  
    Click the star icon on any article to add it to your personal collection
    
    **📚 Organize Your Research**  
    All your favorited articles appear here in one convenient location for easy reference
    
    **🔄 Manage Your Collection**  
    Remove articles you no longer need with the "Remove from Favorites" button
    
    ---
    
    ### 📊 Why Build a Collection?
    
    Creating your own library of healthcare articles helps you:
    - Track important healthcare trends across different countries
    - Compare healthcare systems and policies globally  
    - Save time by having quick access to relevant information
    - Build expertise in specific healthcare topics of interest
    - Share insights with colleagues and stakeholders
    
    Start exploring country pages to build your personalized healthcare knowledge base!
    """)

# API endpoint
fav_articles_URL = f"http://host.docker.internal:4000/country/articles/favorite?userID={userID}"

try:
    # Fetch Articles details
    response = requests.get(fav_articles_URL, timeout=10)
    
    if response.status_code == 200:
        favorites = response.json()
        
        if not favorites:
            # Empty state with styled container
            st.markdown("""
            <div class="articles-empty">
                <p style="color: #2c7a7b; font-size: 1.2rem; margin-bottom: 1rem; font-weight: 500;">
                    You haven't favorited any articles yet.
                </p>
                <p style="color: #555; font-size: 1rem;">
                    Browse the country pages to find and favorite articles!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Article count message with custom styling
            st.markdown(f"""
            <div class="articles-count">
                <strong>You have {len(favorites)} favorite article{'s' if len(favorites) != 1 else ''}:</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Display articles in a 3-column grid
            for idx in range(0, len(favorites), 3):
                cols = st.columns(3, gap="medium")
                
                for col_idx in range(3):
                    if idx + col_idx < len(favorites):
                        article = favorites[idx + col_idx]
                        
                        with cols[col_idx]:
                            # Create a container for each article
                            with st.container(border=True):
                                # Display thumbnail from database
                                image_name = article.get('image_name', 'Book-Blue.png')
                                st.image(f"assets/{image_name}", use_container_width=True)
                                
                                # Article title
                                st.markdown(f"**{article.get('article_title', 'No Title')}**")
                                
                                # Source
                                st.markdown(f"*{article.get('source', 'Unknown Source')}*")
                                
                                # Country code
                                if article.get('country_code'):
                                    st.caption(f"Country: {article['country_code']}")
                                
                                # Read more link
                                if article.get('article_link'):
                                    st.markdown(f"[Read article →]({article['article_link']})")
                                
                                # Unfavorite button
                                if st.button(
                                    "Remove from Favorites", 
                                    key=f"remove_{article['id']}_{idx + col_idx}",
                                    type="secondary",
                                    use_container_width=True
                                ):
                                    # Call unfavorite API
                                    unfav_url = f"http://host.docker.internal:4000/country/articles/favorite/{article['id']}?userID={userID}"
                                    unfav_response = requests.delete(unfav_url)
                                    
                                    if unfav_response.status_code == 200:
                                        st.info("Article removed from favorites!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to remove article from favorites")
                                
    else:
        st.error(f"Error fetching favorites: Status {response.status_code}")
        
except Exception as e:
    st.error(f"Error connecting to the API: {str(e)}")

# Footer spacing
st.write("")
st.write("")