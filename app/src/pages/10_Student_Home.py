import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

from modules.style import style_sidebar, set_background
style_sidebar()

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Student, {st.session_state['name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')
st.write("")

if st.button('Compare Countries', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Country_Comparator.py')

if st.button('View Country Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Country_Profile.py')

if st.button('See Favorite Healthcare Articles', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/12_Favorite_Articles.py')






















