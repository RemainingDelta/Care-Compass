import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Student, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Compare Countries', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Country_Comparator.py')

if st.button('View Country Strength & Weakness Profiles', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Strength_Weakness.py')
