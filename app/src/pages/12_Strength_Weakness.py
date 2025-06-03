import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Strengths vs. Weaknesses")

#data = {} 
#try:
 # data = requests.get('http://web-api:4000/data').json()
#except:
 # st.write("**Important**: Could not connect to sample api, so using dummy data.")
 # data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

#st.dataframe(data)

# create a 2 column layout
col1, col2 = st.columns(2)

# add one number input for variable 1 into column 1
with col1:
    var_01 = st.number_input("Variable 01:", step=1)

# add another number input for variable 2 into column 2
with col2:
    var_02 = st.number_input("Variable 02:", step=1)

logger.info(f"var_01 = {var_01}")
logger.info(f"var_02 = {var_02}")

# add a button to use the values entered into the number field to send to the
# prediction function via the REST API
if st.button("Calculate Prediction", type="primary", use_container_width=True):
    results = requests.get(f"http://web-api:4000/prediction/{var_01}/{var_02}")
    json_results = results.json()
    st.dataframe(json_results)
