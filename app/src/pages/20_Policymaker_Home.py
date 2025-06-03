import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Policymaker, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('See Features Over Time', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Regression.py')

if st.button('Set and Monitor Scores', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Target_Scores.py')


  
import logging
logger = logging.getLogger(__name__)

