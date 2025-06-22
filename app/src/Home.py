##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks
import time
import requests 

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide', page_title="Care Compass - Login", page_icon="⚕️")

# If a user is at this page, we assume they are not 
# authenticated. So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
SideBarLinks(show_home=True)

from modules.style import style_sidebar, set_background
style_sidebar()

# ***************************************************
#    Custom CSS for modern styling
# ***************************************************
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    /* Form container for centering selectbox and button */
    .login-card-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        padding: 1rem 0;
    }
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Ensure all content in login section is centered */
    .row-widget {
        justify-content: center !important;
    }
    
    /* Ensure proper vertical spacing and alignment */
    .login-section {
        min-height: 500px;
        display: flex;
        align-items: stretch;
    }
    
    /* Style the card container for better alignment */
    .card-wrapper {
        display: flex;
        flex-direction: column;
        height: 100%;
        align-items: center;
        justify-content: flex-start;
    }
    .login-card:hover .role-icon {
        animation: bounce 0.5s ease;
    }
    
    /* Override Streamlit's default alignment */
    .main .block-container {
        padding-top: 2rem;
    }
    
    div[data-testid="stHorizontalBlock"] > div {
        display: flex;
        align-items: stretch;
        justify-content: center;
    }
    
    /* Ensure columns have equal height */
    /* Make icons slightly bounce on card hover */
    .login-card:hover .role-icon {
        animation: bounce 0.5s ease;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Ensure emoji icons are perfectly centered */
    .login-card .role-icon {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 4rem;
    }
    
    /* Global heading styles for proper centering */
    h3 {
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 3rem 0 2rem 0;
        margin-bottom: 2rem;
    }
    
    .company-name {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .tagline {
        font-size: 1.3rem;
        color: #2c3e50;
        font-weight: 300;
        max-width: 800px;
        margin: 0 auto 3rem auto;
        line-height: 1.8;
    }
    
    /* Login cards styling */
    .login-card {
        background: white;
        border-radius: 20px;
        padding: 3rem 2.5rem 2.5rem 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(9, 121, 105, 0.1);
        height: 100%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        position: relative;
    }
    
    .login-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        border-color: rgba(9, 121, 105, 0.3);
    }
    
    .role-icon {
        font-size: 4rem;
        margin: 0 auto 1.5rem auto;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        width: 100%;
        height: 80px;
        line-height: 1;
    }
    
    .role-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #097969;
        margin: 0 0 0.5rem 0;
        text-align: center;
        width: 100%;
    }
    
    .role-description {
        color: #6c757d;
        font-size: 0.95rem;
        margin: 0 0 1.5rem 0;
        padding: 0 0.5rem;
        min-height: 3rem;
        text-align: center;
        width: 100%;
        line-height: 1.6;
    }
    
    /* Button styling */
    .stButton {
        width: 100%;
        display: flex;
        justify-content: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem auto 0 auto;
        display: block;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(9, 121, 105, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox {
        width: 100%;
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox > label {
        text-align: center;
        width: 100%;
        color: #2c3e50;
        font-weight: 500;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #097969;
    }
    
    /* Features section */
    .features-section {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 2rem;
        margin: 3rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }
    
    .feature-item {
        text-align: center;
        padding: 1rem;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: #097969;
        margin-bottom: 0.3rem;
    }
    
    .feature-text {
        color: #6c757d;
        font-size: 0.9rem;
    }
    
    /* Ensure Streamlit widgets are centered */
    [data-testid="stForm"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Center all content within columns */
    .element-container {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    [data-testid="column"] > div {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ***************************************************
#    Main content
# ***************************************************

logger.info("Loading the Home page of the app")

# Hero Section
st.markdown("""
    <div class="hero-section">
        <div class="company-name">Care Compass</div>
        <div class="tagline">
            Navigate the world of healthcare with confidence. We leverage real health data and 
            cutting-edge machine learning to help you compare, understand, and make informed 
            decisions about global healthcare systems.
        </div>
    </div>
""", unsafe_allow_html=True)

# API setup
headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

API_URL = "http://host.docker.internal:4000/users/users"

# Function to fetch users by role
def fetch_users_by_role(role_id):
    try:
        params = {"roleID": role_id}
        response = requests.get(API_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        users = response.json()
        return [f"{user['first_name']} {user['last_name']} - {user['email']}" for user in users]
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch users for role {role_id}: {e}")
        return []
    except (KeyError, TypeError) as e:
        logger.error(f"Unexpected response format for role {role_id}: {e}")
        return []

# Fetch users for each role
residents_list = fetch_users_by_role(0)
students_list = fetch_users_by_role(1)
policymakers_list = fetch_users_by_role(2)

# Check if we successfully fetched users
if not residents_list and not students_list and not policymakers_list:
    st.error("Unable to connect to the user database. Please check your connection and try again.")
    st.stop()

# Login Cards Section
st.markdown("### Choose Your Role")

col1, col2, col3 = st.columns(3, gap="large")

# Resident Card
with col1:
    st.markdown("""
        <div class="login-card">
            <div class="role-icon">🏠</div>
            <h3 class="role-title">Resident</h3>
            <p class="role-description">
                Access personalized healthcare recommendations and country comparisons
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if residents_list:
        resident = st.selectbox(
            "Select a resident account:",
            residents_list,
            index=None,
            placeholder="Choose a resident...",
            key="resident_select"
        )
    else:
        st.warning("No resident accounts available")
        resident = None
    
    if st.button("Login as Resident", key="resident_login", type="primary", use_container_width=True):
        if resident:
            name, email = resident.split(" - ", 1)
            first_name, last_name = name.split(" ", 1)
            
            # Get user ID first before setting session state
            try:
                userID_response = requests.get(f"http://host.docker.internal:4000/users/id/{email}", timeout=10)
                userID_response.raise_for_status()
                user_data = userID_response.json()
                
                # Check if 'id' exists in response
                if 'id' not in user_data:
                    raise ValueError("User ID not found in response")
                
                user_id = user_data["id"]
                
                # Set session state only after successful user ID retrieval
                st.session_state['authenticated'] = True
                st.session_state['role'] = 'resident'
                st.session_state['name'] = name
                st.session_state['last_name'] = last_name
                st.session_state['email'] = email
                st.session_state['user_id'] = user_id
                
                logger.info(f"Logging in as Resident Persona: {name}")
                st.switch_page('pages/00_Resident_Home.py')
            except requests.exceptions.RequestException as e:
                st.error("Failed to connect to user service")
                logger.error(f"API connection error: {e}")
            except (KeyError, ValueError) as e:
                st.error("Invalid user data received")
                logger.error(f"Data parsing error: {e}")
            except Exception as e:
                st.error("An unexpected error occurred during login")
                logger.error(f"Unexpected login error: {e}")
        else:
            st.error("Please select a resident account to login")

# Student Card
with col2:
    st.markdown("""
        <div class="login-card">
            <div class="role-icon">🎓</div>
            <h3 class="role-title">Student</h3>
            <p class="role-description">
                Explore healthcare data and trends for research and learning
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if students_list:
        student = st.selectbox(
            "Select a student account:",
            students_list,
            index=None,
            placeholder="Choose a student...",
            key="student_select"
        )
    else:
        st.warning("No student accounts available")
        student = None
    
    if st.button("Login as Student", key="student_login", type="primary", use_container_width=True):
        if student:
            name, email = student.split(" - ", 1)
            first_name, last_name = name.split(" ", 1)
            
            # Get user ID first before setting session state
            try:
                userID_response = requests.get(f"http://host.docker.internal:4000/users/id/{email}", timeout=10)
                userID_response.raise_for_status()
                user_data = userID_response.json()
                
                # Check if 'id' exists in response
                if 'id' not in user_data:
                    raise ValueError("User ID not found in response")
                
                user_id = user_data["id"]
                
                # Set session state only after successful user ID retrieval
                st.session_state['authenticated'] = True
                st.session_state['role'] = 'student'
                st.session_state['name'] = name
                st.session_state['last_name'] = last_name
                st.session_state['email'] = email
                st.session_state['user_id'] = user_id
                
                logger.info(f"Logging in as Student Persona: {name}")
                st.switch_page('pages/10_Student_Home.py')
            except requests.exceptions.RequestException as e:
                st.error("Failed to connect to user service")
                logger.error(f"API connection error: {e}")
            except (KeyError, ValueError) as e:
                st.error("Invalid user data received")
                logger.error(f"Data parsing error: {e}")
            except Exception as e:
                st.error("An unexpected error occurred during login")
                logger.error(f"Unexpected login error: {e}")
        else:
            st.error("Please select a student account to login")

# Policymaker Card
with col3:
    st.markdown("""
        <div class="login-card">
            <div class="role-icon">🏛️</div>
            <h3 class="role-title">Policymaker</h3>
            <p class="role-description">
                Analyze healthcare systems and access policy insights
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if policymakers_list:
        policymaker = st.selectbox(
            "Select a policymaker account:",
            policymakers_list,
            index=None,
            placeholder="Choose a policymaker...",
            key="policymaker_select"
        )
    else:
        st.warning("No policymaker accounts available")
        policymaker = None
    
    if st.button("Login as Policymaker", key="policymaker_login", type="primary", use_container_width=True):
        if policymaker:
            name, email = policymaker.split(" - ", 1)
            first_name, last_name = name.split(" ", 1)
            
            # Get user ID first before setting session state
            try:
                userID_response = requests.get(f"http://host.docker.internal:4000/users/id/{email}", timeout=10)
                userID_response.raise_for_status()
                user_data = userID_response.json()
                
                # Check if 'id' exists in response
                if 'id' not in user_data:
                    raise ValueError("User ID not found in response")
                
                user_id = user_data["id"]
                
                # Set session state only after successful user ID retrieval
                st.session_state['authenticated'] = True
                st.session_state['role'] = 'policymaker'
                st.session_state['name'] = name
                st.session_state['last_name'] = last_name
                st.session_state['email'] = email
                st.session_state['user_id'] = user_id
                
                logger.info(f"Logging in as Policymaker Persona: {name}")
                st.switch_page('pages/20_Policymaker_Home.py')
            except requests.exceptions.RequestException as e:
                st.error("Failed to connect to user service")
                logger.error(f"API connection error: {e}")
            except (KeyError, ValueError) as e:
                st.error("Invalid user data received")
                logger.error(f"Data parsing error: {e}")
            except Exception as e:
                st.error("An unexpected error occurred during login")
                logger.error(f"Unexpected login error: {e}")
        else:
            st.error("Please select a policymaker account to login")

# Features Section
st.markdown("""
    <div class="features-section">
        <h3 style="text-align: center; margin-bottom: 2rem; color: #2c3e50;">
            Why Choose Care Compass?
        </h3>
    </div>
""", unsafe_allow_html=True)

feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)

with feat_col1:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Real Data</div>
            <div class="feature-text">
                Access authentic healthcare data from trusted global sources
            </div>
        </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">ML Insights</div>
            <div class="feature-text">
                Powered by advanced machine learning algorithms
            </div>
        </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">🌍</div>
            <div class="feature-title">Global Coverage</div>
            <div class="feature-text">
                Compare healthcare systems across countries
            </div>
        </div>
    """, unsafe_allow_html=True)

with feat_col4:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Personalized</div>
            <div class="feature-text">
                Get recommendations based on your priorities
            </div>
        </div>
    """, unsafe_allow_html=True)