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

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

from modules.style import style_sidebar, set_background
style_sidebar()

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")



st.markdown("""
    <style>
    .centered-title {
        height: 30vh; /* Full viewport height */
        display: flex;
        justify-content: top;
        align-items: top;
        flex-direction: column;
    }
    .company-name {
        font-size: 64px;
        font-weight: bold;
        color: 	#097969;
        text-align: center;
    }
    </style>
    <div class="centered-title">
        <div class="company-name">Care Compass</div>
    </div>
""", unsafe_allow_html=True)

text = "We use real health data and machine learning to help users compare and understand global healthcare systems. Our platform lets you explore country profiles, visualize key trends, and get personalized recommendations based on your healthcare priorities."
st.write(text)


# Add space or content that appears lower on scroll
st.write("")
st.markdown("---")
st.write('\n')
st.markdown('#### Login as a ...')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

# API endpoint
API_URL = "http://host.docker.internal:4000/users/users"  


# Get unique values for filters from the API
#For resident login 
try:
    response = requests.get(API_URL, headers=headers, timeout=10)
    response.raise_for_status()

    residents = response.json()
    residents_list = [item["first_name"] for item in residents]

    # Extract unique values for filters
    role = sorted(list(set(Users["roleID"] for Users in residents)))

    # Create ROLE ID FILTER
    selected_role = 0

    # Build query parameters
    params = {"roleID": selected_role}

    # Get filtered data
    filtered_response = requests.get(API_URL, params=params, headers=headers, timeout=10)
    #filtered_response.raise_for_status()

    filtered_residents = filtered_response.json()
    residents_email_list = [item['first_name'] + ' ' + item['last_name'] + ' - ' + item['email'] for item in filtered_residents]

    #filtered_response = requests.get(API_URL, params=params, headers=headers, timeout=10)

except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)

#For student login 
# API endpoint
API_URL = "http://host.docker.internal:4000/users/users"  


# Get unique values for filters from the API
try:
    response = requests.get(API_URL, headers=headers, timeout=10)
    response.raise_for_status()

    students = response.json()
    students_list = [item["first_name"] for item in students]

    # Extract unique values for filters
    role = sorted(list(set(Users["roleID"] for Users in students)))
    
    # Create ROLE ID FILTER
    selected_role = 1
    
    # Build query parameters
    params = {"roleID": selected_role}
  
    # Get filtered data
    filtered_response = requests.get(API_URL, params=params, headers=headers, timeout=10)
    #filtered_response.raise_for_status()
    
    filtered_students = filtered_response.json()
    students_email_list = [item['first_name'] + ' ' + item['last_name'] + ' - ' + item['email'] for item in filtered_students]

    #filtered_response = requests.get(API_URL, params=params, headers=headers, timeout=10)

except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)


#For policymaker login 
# API endpoint
API_URL = "http://host.docker.internal:4000/users/users"  


# Get unique values for filters from the API
try:
    response = requests.get(API_URL, headers=headers, timeout=10)
    response.raise_for_status()

    policy = response.json()
    policy_list = [item["first_name"] for item in policy]

    # Extract unique values for filters
    role = sorted(list(set(Users["roleID"] for Users in policy)))
    
    # Create ROLE ID FILTER
    selected_role = 2
    
    # Build query parameters
    params = {"roleID": selected_role}
  
    # Get filtered data
    filtered_response = requests.get(API_URL, params=params, headers=headers, timeout=10)
    #filtered_response.raise_for_status()
    
    filtered_policy = filtered_response.json()
    policy_email_list = [item['first_name'] + ' ' + item['last_name'] + ' - ' + item['email'] for item in filtered_policy]

    #filtered_response = requests.get(API_URL, params=params, headers=headers, timeout=10)

except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)


col1, col2 = st.columns([0.7,0.3],vertical_alignment="bottom")
col3, col4 = st.columns([0.7,0.3],vertical_alignment="bottom")
col5, col6 = st.columns([0.7,0.3],vertical_alignment="bottom")

# UI
with col1 :
  resident = st.selectbox(
      "Resident:",
      residents_email_list,
      index=None
  )

with col3:
  student = st.selectbox(
      "Student:",
      students_email_list,
      index=None
  )

with col5:
  policy = st.selectbox(
      "Policymaker:",
      policy_email_list,
      index=None
  )
  
if resident:
    name, email = resident.split(" - ", 1)
    selected_name = name
    selected_email = email
    first_name, last_name = name.split(" ", 1)
    #st.write("You are logging in as:", selected_name)

if student:
    name, email = student.split(" - ", 1)
    selected_name = name
    selected_email = email
    first_name, last_name = name.split(" ", 1)
    #st.write("You are logging in as:", selected_name)

if policy:
    name, email = policy.split(" - ", 1)
    selected_name = name
    selected_email = email
    first_name, last_name = name.split(" ", 1)
    #st.write("You are logging in as:", selected_name)




with col2 :
  if st.button("Login", key="resident",type="primary",use_container_width=False) :
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'resident'
    st.session_state['name'] = selected_name
    st.session_state['last_name'] = last_name
    st.session_state['email'] = selected_email
    email_API = st.session_state['email']

    userID_response = requests.get(f"http://host.docker.internal:4000/users/users/id/{email_API}")
    userID = userID_response.json()
    st.session_state['id'] = userID

    logger.info("Logging in as Resident Persona")
    st.switch_page('pages/00_Resident_Home.py')

with col4:
  if st.button("Login", key="student",type="primary",use_container_width=False) :
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student'
    st.session_state['name'] = selected_name
    st.session_state['last_name'] = last_name
    st.session_state['email'] = selected_email
    email_API = st.session_state['email']

    userID_response = requests.get(f"http://host.docker.internal:4000/users/users/id/{email_API}")
    userID = userID_response.json()
    st.session_state['id'] = userID
    
    logger.info("Logging in as Student Persona")
    st.switch_page('pages/10_Student_Home.py')

with col6:
  if st.button("Login", key="policymaker",type="primary",use_container_width=False) :
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'policymaker'
    st.session_state['name'] = selected_name
    st.session_state['last_name'] = last_name
    st.session_state['email'] = selected_email
    email_API = st.session_state['email']

    userID_response = requests.get(f"http://host.docker.internal:4000/users/users/id/{email_API}")
    userID = userID_response.json()
    st.session_state['id'] = userID
    
    logger.info("Logging in as Policymaker Persona")
    st.switch_page('pages/20_Policymaker_Home.py')


