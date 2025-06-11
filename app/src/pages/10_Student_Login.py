import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.session_state['authenticated'] = False

st.set_page_config(layout = 'wide')

from modules.style import style_sidebar, set_background
style_sidebar()

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks(show_home=True)


headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}


# API endpoint
API_URL = "http://host.docker.internal:4000/users/users"  


# Get unique values for filters from the API
try:
    response = requests.get(API_URL, headers=headers, timeout=10)
    response.raise_for_status()

    users = response.json()
    users_list = [item["first_name"] for item in users]

    # Extract unique values for filters
    role = sorted(list(set(Users["roleID"] for Users in users)))
    
    # Create ROLE ID FILTER
    selected_role = 1
    
    # Build query parameters
    params = {"roleID": selected_role}
  
    # Get filtered data
    filtered_response = requests.get(API_URL, params=params, headers=headers, timeout=10)
    #filtered_response.raise_for_status()
    
    filtered_users = filtered_response.json()
    user_email_list = [item['first_name'] + ' ' + item['last_name'] + ' - ' + item['email'] for item in filtered_users]

    filtered_response = requests.get(API_URL, params=params, headers=headers, timeout=10)

except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)


# UI
col1, col2 = st.columns([0.7,0.3],vertical_alignment="bottom")

with col1 :
  user = st.selectbox(
      "Login:",
      user_email_list,
      index=None
  )
  
if user:
    name, _ = user.split(" - ", 1)
    selected_name = name
    st.write("You are logging in as:", selected_name)

with col2 :
  if st.button("Submit", type="primary",use_container_width=False) :
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student'
    st.session_state['name'] = selected_name
    logger.info("Logging in as Student Persona")
    st.switch_page('pages/10_Student_Home.py')



























