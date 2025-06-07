import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import time

from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")

SideBarLinks()

headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Your backend endpoint URL
API_URL = "http://host.docker.internal:4000/country/countries"  

country_list = []

try:
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    country_list = [item["name"] for item in data]
    print("Countries:", country_list)


except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)


st.title("SET AND MONITOR TARGET SCORES")
st.write("")

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox(
            "Choose Country:",
            country_list,
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
    submit = st.button("Submit", type="primary")

if submit:
    col2.subheader("Current Scores for %s" %country)
    col2.write("Scores")

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
        calculate = st.button("Calculate", type="primary")

st.write("")
st.write("")
if calculate:
    st.subheader("PROJECTED TIME")
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    st.button("Rerun")








