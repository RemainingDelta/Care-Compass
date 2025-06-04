import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import time

SideBarLinks()
st.title("SET AND MONITOR TARGET SCORES")
st.write("")

col1, col2 = st.columns(2)
countries = ["Afghanistan", "Cuba"]

with col1:
    country = st.selectbox(
            "Choose Country:",
            countries,
            index=None,
            placeholder="Select Country ..."
        )
    st.write("You selected ", country)
     #st.form_submit_button(
        #  label="Submit", 
         # help=None, 
         # on_click=None, 
         # args=None,  
       # )
    if st.button("Submit", type="primary"):
        col2.write("Scores")
        
col2.subheader("Current Scores for %s" %country)

st.write("")
st.write("")
st.subheader("INPUT TARGET SCORES")
cola,colb,colc = st.columns(3)
with cola:
    prevention = st.number_input("Prevention")
    rapresp = st.number_input("Rapid Response")

with colb:
    healthsys = st.number_input("Health System")
    detectreport = st.number_input("Detection & Reporting")

with colc:
    intlnorms = st.number_input("International Norms Compliance")
    riskenv = st.number_input("Risk Environment")

st.write("")
st.write("")
st.subheader("PROJECTED TIME")
progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

st.button("Rerun")

