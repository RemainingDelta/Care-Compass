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
        <div class="company-name">CARE COMPASS</div>
    </div>
""", unsafe_allow_html=True)


def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

#Sample Example
text = "We use real health data and machine learning to help users compare and understand global healthcare systems. Our platform lets you explore country profiles, visualize key trends, and get personalized recommendations based on your healthcare priorities."
speed = 30
typewriter(text=text, speed=speed)


# Add space or content that appears lower on scroll
st.write("")
st.markdown("---")
st.header('Welcome!')
st.write('\n')
st.write('#### Login as a ...')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

col1, col2, col3 = st.columns(3)

with col1 :

    if st.button("Relocating Resident", 
                type = 'primary', 
                use_container_width=True):
        # when user clicks the button, they are now considered authenticated
        st.session_state['authenticated'] = True
        # we set the role of the current user
        st.session_state['role'] = 'resident'
        # we add the first name of the user (so it can be displayed on 
        # subsequent pages). 
        st.session_state['name'] = 'Archibald'
        # finally, we ask streamlit to switch to another page, in this case, the 
        # landing page for this particular user type
        logger.info("Logging in as Resident Persona")
        st.switch_page('pages/00_Resident_Login.py')

with col2 :
    if st.button('Global Health Student', 
                type = 'primary', 
                use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'student'
        st.session_state['name'] = 'Gale'
        logger.info("Logging in as Student Persona")
        st.switch_page('pages/10_Student_Login.py')

with col3 : 
    if st.button('Policymaker', 
                type = 'primary', 
                use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'policymaker'
        st.session_state['name'] = 'Nancy'
        logger.info("Logging in as Policymaker Persona")
        st.switch_page('pages/20_Policymaker_Login.py')



