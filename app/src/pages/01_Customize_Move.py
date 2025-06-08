import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
#import matplotlib.pyplot as plt
import numpy as np
#import plotly.express as px
from modules.nav import SideBarLinks
import requests
import json

from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.title('CUSTOMIZE YOUR MOVE!')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}. Rank the healthcare factors in order of priority -- 1 being the highest and 6 the lowest.")
st.write("")
st.write("")

options = ["Prevention","Health System","Rapid Response","Detection & Reporting", 
           "International Norms Compliance","Risk Environment"]

#EX DATAFRAME
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["countries","features"],
)


headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

st.title("Please input the country to get similarity scores:")

API_URL = "http://web-api:4000/country/countries"

country_list = []

try:
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Response is a list of country dicts
    country_list = [item["name"] for item in data]

    print("Countries:", country_list)

except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)

# Select Country Dropdown
chosen_country = st.selectbox("Select Country:", 
                                country_list,
                                index=None)

# Submit button
if st.button("Submit"):
    
    #Hard coding similarity for now: 
    api_url = f"http://host.docker.internal:4000/ml/ml/get_cosine_similar/{chosen_country}"
    response = requests.get(api_url, headers=headers, timeout=10)
    #print(response)

    if response.status_code == 200:
         data = response.text  
         #st.success("It worked!")
         data_dict = json.loads(data)
         df_similar = pd.DataFrame(data_dict)
         sorted_df_similar = df_similar.sort_values(by='the_country_cosine', ascending=False)
         st.write(f"Here are the countries most similar to: {chosen_country}")
         st.dataframe(sorted_df_similar.head(10)) 
         st.write(f"Here are the countries least similar to: {chosen_country}")
         st.dataframe(sorted_df_similar.tail(10)) 


col1, col2 = st.columns(2)

with col1:
    col1a, col1b = st.columns(2)
    
    with col1a: 
        option1 = st.selectbox(
            "1:",
            options,
            index=None,
            placeholder="Select PRIORITY factor...",
        )
        st.write("\n")

    
        option2 = st.selectbox(
            "2:",
            options,
            index=None,
            placeholder="Select SECONDARY factor...",
        )
        st.write("\n")

        option3 = st.selectbox(
            "3:",
            options,
            index=None,
            placeholder="Select TERTIARY factor...",
        )

        st.write("")
        st.button("Submit", type="primary")
    

    with col1b:
        option4 = st.selectbox(
            "4:",
            options,
            index=None,
            placeholder="Select QUARTERNARY factor...",
        )
        st.write("\n")

        option5 = st.selectbox(
            "5:",
            options,
            index=None,
            placeholder="Select QUINARY factor...",
        )
        st.write("\n")

        option6 = st.selectbox(
            "6:",
            options,
            index=None,
            placeholder="Select SENARY factor...",
        )

with col2:
    on = st.toggle("Bar Chart / Map")

    if on:
        st.map(df)
    else: st.bar_chart(df)


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





