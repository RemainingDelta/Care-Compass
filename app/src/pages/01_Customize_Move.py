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
st.write(f"### Hi, {st.session_state['first_name']}. Rank the factors in order of priority -- 1 being the highest and 6 the lowest.")
st.write("")
st.write("")

options = ["Prevention","Health System","Rapid Response","Detection & Reporting", 
           "International Norms Compliance","Risk Environment"]

#EX DATAFRAME
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)

col1, col2 = st.columns(2)

with col1:
    col1a, col1b = st.columns(2)
    
    with col1a: 
        option1 = st.selectbox(
            "1:",
            options,
            index=None,
            placeholder="Select PRIORITY healthcare factor...",
        )
        st.write("\n")

    
        option2 = st.selectbox(
            "2:",
            options,
            index=None,
            placeholder="Select SECONDARY healthcare factor...",
        )
        st.write("\n")

        option3 = st.selectbox(
            "3:",
            options,
            index=None,
            placeholder="Select TERTIARY healthcare factor...",
        )
    

    with col1b:
        option4 = st.selectbox(
            "4:",
            options,
            index=None,
            placeholder="Select QUARTERNARY healthcare factor...",
        )
        st.write("\n")

        option5 = st.selectbox(
            "5:",
            options,
            index=None,
            placeholder="Select QUINARY healthcare factor...",
        )
        st.write("\n")

        option6 = st.selectbox(
            "6:",
            options,
            index=None,
            placeholder="Select SENARY healthcare factor...",
        )

with col2:
    on = st.toggle("Map / Bar Chart")

    if on:
        st.bar_chart(df)
    else: st.map(df)


st.write("")
st.write("")

st.write("#### Use the Sliders")

col1,col2 = st.columns(2)
with col1:  
    prevention = st.slider("Prevention Score: ", 0, 100, 25)
    healthsys = st.slider("Health System Score: ", 0, 100, 25)
    rapidresp = st.slider("Rapid Response Score: ", 0, 100, 25)

with col2:
    detectreport = st.slider("Detection & Reporting Score: ", 0, 100, 25)
    normscomp = st.slider("International Norms Compliance Score: ", 0, 100, 25)
    riskenv = st.slider("Risk Environment Score: ", 0, 100, 25)





