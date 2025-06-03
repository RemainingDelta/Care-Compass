import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("COUNTRY COMPARATOR")
st.write("")
st.write("")

countries = []
features = []
col1, col2, col3 = st.columns(3)

with col1:
    country1 = st.selectbox(
            "Country 1:",
            countries,
            index=None,
            placeholder="Select Country 1 ..."
        )

with col2: 
    country2 = st.selectbox(
            "Country 2:",
            countries,
            index=None,
            placeholder="Select Country 2 ..."
    )

with col3: 
    country3 = st.selectbox(
            "Country 3:",
            countries.insert(0, "N/A"),
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
trackfeat = st.selectbox(
            "Track a feature over time:",
            features,
            index=None,
            placeholder="Select Feature ..."
        )

st.line_chart(df)