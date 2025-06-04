import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("COUNTRY COMPARATOR")
st.write("")
st.write("")


# Your backend endpoint URL
url = "http://localhost:4000/country/countries"  

# Make GET request for countries
response = requests.get(url)

# Check response
if response.status_code == 200:
    data = response.json()
    country_list = data.get("countries", [])
    print("Countries:", country_list)
else:
    print("Error:", response.status_code)


features = []
col1, col2, col3 = st.columns(3)

with col1:
    country1 = st.selectbox(
            "Country 1:",
            country_list,
            index=None,
            placeholder="Select Country 1 ..."
        )

with col2: 
    country2 = st.selectbox(
            "Country 2:",
            country_list,
            index=None,
            placeholder="Select Country 2 ..."
    )

with col3: 
    country3 = st.selectbox(
            "Country 3:",
            country_list.insert(0, "N/A"),
            index=None,
            placeholder="Select Country 3 ..."
    )

#EX DATAFRAME
df = pd.DataFrame(
    np.random.randn(10, 5), columns=("col %d" % i for i in range(5))
)

st.table(df)

st.write("")
st.write("")
feature = st.selectbox(
            "Track a feature over time:",
            features,
            index=None,
            placeholder="Select Feature ..."
        )
st.write("Tracking %s over time" %feature)
st.write("")
plot = st.button("Plot", type="primary")

if plot:
    results = requests.get(f"http://web-api:4000/ml/predict/{feature}/{country1}") # need to do more for the other countries
    json_results = results.json()
    st.dataframe(json_results)