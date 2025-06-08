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
from streamlit_sortables import sort_items


from modules.style import style_sidebar, set_background
style_sidebar()
set_background("assets/backdrop.jpg")

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.title('CUSTOMIZE YOUR MOVE!')

st.markdown("""
    <style>
    div[data-testid="sortable-item"] {
        font-family: inherit;
        font-weight: 500;
        font-size: 1rem;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)


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


st.subheader("Rank the healthcare factors (drag to reorder)")

factors = [
    "Prevention",
    "Health System",
    "Rapid Response",
    "Detection & Reporting",
    "International Norms Compliance",
    "Risk Environment"
]

# Persistent state
if "factor_weights" not in st.session_state:
    st.session_state.factor_weights = {factor: 100 - i * 20 for i, factor in enumerate(factors)}
if "dragged_factors" not in st.session_state:
    st.session_state.dragged_factors = factors.copy()

# Show rank guidance
st.markdown('<div style="text-align: center; font-weight: bold;">1</div>', unsafe_allow_html=True)
st.session_state.dragged_factors = sort_items(
    st.session_state.dragged_factors,
    direction="vertical",
    key="drag_order"
)
st.markdown('<div style="text-align: center; font-weight: bold;">6</div>', unsafe_allow_html=True)

# Set default weights per slot, not per factor
if "slot_weights" not in st.session_state:
    st.session_state.slot_weights = [100 - i * 20 for i in range(6)]

st.markdown("### Adjust weight for each priority slot")

ranges = [(90, 100), (70, 90), (50, 70), (30, 50), (10, 30), (0, 10)]

for i in range(6):
    factor = st.session_state.dragged_factors[i]
    min_val, max_val = ranges[i]

    # Clamp value into range
    cur_val = min(max(st.session_state.slot_weights[i], min_val), max_val)

    # Create row: number | factor | slider | input
    col_num, col_label, col_slider, col_input = st.columns([1, 3, 5, 2])
    with col_num:
        st.markdown(f"**{i+1}.**")
    with col_label:
        st.markdown(f"""
            <div style="padding-top: 8px; font-weight: 600;">
                {factor}
            </div>
        """, unsafe_allow_html=True)
    with col_slider:
        st.session_state.slot_weights[i] = st.slider(
            "", min_val, max_val, cur_val, key=f"slider_{i}"
        )
    with col_input:
        st.session_state.slot_weights[i] = st.number_input(
            "", min_value=min_val, max_value=max_val,
            value=st.session_state.slot_weights[i],
            step=1, key=f"input_{i}"
        )

# Output
st.markdown("---")
st.markdown("### Final Rankings & Slot Weights")
for i in range(6):
    factor = st.session_state.dragged_factors[i]
    weight = st.session_state.slot_weights[i]
    st.write(f"{i+1}. {factor}: {weight}")
