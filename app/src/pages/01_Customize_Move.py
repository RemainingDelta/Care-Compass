import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Customize Your Move!')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

col1, col2, col3 = st.columns(3)
options = ["Prevention","Health System","Rapid Response","Detection & Reporting", 
           "International Norms Compliance","Risk Environment"]

col1.subheader("Rank the factors in order of priority (1 being the highest and 6 the lowest)")
with col1:
    option1 = st.selectbox(
        "1:",
        options,
        index=None,
        placeholder="Select PRIORITY healthcare factor...",
    )
    option2 = st.selectbox(
        "2:",
        options,
        index=None,
        placeholder="Select SECONDARY healthcare factor...",
    )
    option3 = st.selectbox(
        "3:",
        options,
        index=None,
        placeholder="Select TERTIARY healthcare factor...",
    )
    

with col2:
    option4 = st.selectbox(
        "4:",
        options,
        index=None,
        placeholder="Select QUARTERNARY healthcare factor...",
    )
    option5 = st.selectbox(
        "5:",
        options,
        index=None,
        placeholder="Select QUINARY healthcare factor...",
    )
    option6 = st.selectbox(
        "6:",
        options,
        index=None,
        placeholder="Select SENARY healthcare factor...",
    )

with col3:
    on = st.toggle("Map / Bar Chart")

    if on:
        st.write("Feature activated!")
    



prevention = st.slider("Prevention Score: ", 0, 100, 25)
healthsys = st.slider("Health System Score: ", 0, 100, 25)
rapidresp = st.slider("Rapid Response Score: ", 0, 100, 25)
detectreport = st.slider("Detection & Reporting Score: ", 0, 100, 25)
normscomp = st.slider("International Norms Compliance Score: ", 0, 100, 25)
riskenv = st.slider("Risk Environment Score: ", 0, 100, 25)





