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


# CHANGE FOLLOWING CODE 
st.write("Rank the factors in order of priority (1 being the highest and 6 the lowest)")

options = ["Prevention","Health System","Rapid Response","Detection & Reporting", 
           "International Norms Compliance","Risk Environment"]
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






# get the countries from the world bank data
with st.echo(code_location='above'):
    countries:pd.DataFrame = wb.get_countries()
   
    st.dataframe(countries)

# the with statment shows the code for this block above it 
with st.echo(code_location='above'):
    arr = np.random.normal(1, 1, size=100)
    test_plot, ax = plt.subplots()
    ax.hist(arr, bins=20)

    st.pyplot(test_plot)


with st.echo(code_location='above'):
    slim_countries = countries[countries['incomeLevel'] != 'Aggregates']
    data_crosstab = pd.crosstab(slim_countries['region'], 
                                slim_countries['incomeLevel'],  
                                margins = False) 
    st.table(data_crosstab)
