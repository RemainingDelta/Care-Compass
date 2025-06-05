import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import numpy as np

st.set_page_config(layout = 'wide')

from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")

SideBarLinks()

st.title('FEATURES OVER TIME')
st.write("Choose a region and your target country to view how including features changes scores over time.")
st.write("")


# EX DATA 
chart_data = pd.DataFrame(
    np.random.randn(20, 3), columns=["col1", "col2", "col3"]
)
chart_data["col4"] = np.random.choice(["A", "B", "C"], 20)

st.scatter_chart(
    chart_data,
    x="col1",
    y="col2",
    color="col4",
    size="col3",
)


col1,col2 = st.columns(2)
countries = []
regions = []
time = []

with col1: 
    region = st.selectbox(
        "Region:",
        regions,
        index=None,
        placeholder="Select Region ..."
    )
    
    country = st.selectbox(
        "Country:",
        countries,
        index=None,
        placeholder="Select Country ..."
    )
    
    
with col2:
    time = st.selectbox(
        "Time (years):",
        time,
        index=None,
        placeholder="Select Time ..."
    )

    end_date = st.date_input(
        "End Date:", 
        "today")

st.write("")
st.write("")
st.subheader("SELECT FEATURES TO CONSIDER")
col3,col4 = st.columns(2)

with col3:
    life_exp = st.checkbox("Life Expectancy (years)")
    if life_exp:
        st.write("Great!")
    
    inf_mort = st.checkbox("Infant Mortality Rate")
    if inf_mort:
        st.write("OK")

    live_birth = st.checkbox("Live Births per 1000 Population")
    if live_birth:
        st.write("YES")

with col4:
    gen_prac = st.checkbox("General Practitioners per 10,000 Population")
    if gen_prac:
        st.write("Yea")
    
    health_expen = st.checkbox("Total Health Expenditure per Capita")
    if health_expen:
        st.write("Money")
    
    impov_house = st.checkbox("Impoverished Households")
    if impov_house:
        st.write("NO")



