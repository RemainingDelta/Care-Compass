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
import plotly.express as px 
import plotly.graph_objects as go


from modules.style import style_sidebar, set_background
style_sidebar()

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
st.write(f"### Hi, {st.session_state['name']}.")
st.write("Choose a country, and rank the healthcare factors in order of YOUR priority -- 1 being the highest and 6 the lowest. Then, you may adjust the weights accordingly.")
st.write("")


options = ["Prevention","Health System","Rapid Response","Detection & Reporting", 
           "International Norms Compliance","Risk Environment"]


headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Fetch factor descriptions for tooltips
factor_descriptions = {}

try:
    response = requests.get("http://host.docker.internal:4000/country/factor_descriptions", headers=headers, timeout=10)
    if response.status_code == 200:
        
        data = response.json()
        for item in data:
            # Normalize key for matching
            key = item["name"].lower().replace(" ", "").replace("&", "and").strip()
            print("Storing description for:", key)
            factor_descriptions[key] = item["description"]
except Exception as e:
    print("Failed to fetch factor descriptions:", e)

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
#st.write("FRONTEND SELECTED COUNTRY", chosen_country)

st.write("Drag to reorder factors (top = 1, bottom = 6)")

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
st.session_state.dragged_factors = sort_items(
    st.session_state.dragged_factors,
    direction="vertical",
    key="drag_order"
)

# Set default weights per slot, not per factor
if "slot_weights" not in st.session_state:
    st.session_state.slot_weights = [100 - i * 20 for i in range(6)]

st.markdown("### Adjust the weight for each priority slot")

slider_range = (1, 10)


for i in range(6):
    factor = st.session_state.dragged_factors[i]
    
    # Set keys and defaults
    val_key = f"val_{i}"
    if val_key not in st.session_state:
        st.session_state[val_key] = 5  # Default slider/input value

    slider_val = st.session_state[val_key]

    # Normalize tooltip key
    tooltip_keys = {
        "prevention": "prevention",
        "healthsystem": "healthsystem",
        "rapidresponse": "rapidresponse",
        "detection&reporting": "detectionandreporting",
        "internationalnormscompliance": "compliancewithinternationalnorms",
        "riskenvironment": "riskenvironment"
    }
    lookup_key = tooltip_keys.get(factor.lower().replace(" ", "").strip(), "")
    desc = factor_descriptions.get(lookup_key, "")

    # Layout: label + ℹ️ on left, slider + input on right
    col_label, col_slider, col_input = st.columns([4, 5, 2])
    
    with col_label:
        row = st.columns([5, 1])  # 5 parts label, 1 part icon
        with row[0]:
            st.markdown(f"**{i+1}. {factor}**")
        with row[1]:
            st.button("ℹ️", key=f"info_button_{i}", help=desc)

    with col_slider:
        new_slider = st.slider(
            label="",
            min_value=0,
            max_value=10,
            value=slider_val,
            key=f"slider_{i}",
            label_visibility="collapsed"
        )
        
    with col_input:
        new_input = st.number_input(
            label="",
            min_value=0,
            max_value=10,
            value=slider_val,
            step=1,
            key=f"input_{i}",
            label_visibility="collapsed"
        )

    # Sync slider/input
    if new_input != st.session_state[val_key]:
        st.session_state[val_key] = new_input
    elif new_slider != st.session_state[val_key]:
        st.session_state[val_key] = new_slider

    # Calculate weighted priority
    if i == 0:
        true_weight = 90 + st.session_state[val_key]
    elif i == 5:
        true_weight = st.session_state[val_key]
    else:
        true_weight = 90 - 20 * i + 2 * st.session_state[val_key]

    st.session_state.slot_weights[i] = true_weight




if i == 0:
    true_weight = 90 + slider_val
elif i == 5:
    true_weight = slider_val
else:
    base = 90 - 20 * i
    true_weight = base + 2 * slider_val

st.session_state.slot_weights[i] = true_weight

weights_dict = {}
# Output
st.markdown("---")
st.markdown("### Final Rankings & Slot Weights")
for i in range(6):
    factor = st.session_state.dragged_factors[i]
    weight = st.session_state.slot_weights[i]
    st.write(f"{i+1}. {factor}: {weight}")
    weights_dict[factor] = float(weight/100)

#Put the weights in a table 


submit = st.button("Submit", type="primary")
on = st.toggle("Bar Chart / Gradient Map")
bar_chart_display = pd.DataFrame()
bar_chart_display['Country'] = []
bar_chart_display['the_country_cosine'] = []
bar_chart_display['the_country_dot_product'] = []
sorted_df_similar = pd.DataFrame()
sorted_df_similar['Country'] = []
sorted_df_similar['the_country_cosine'] = []
sorted_df_similar['the_country_dot_product'] = []
if submit:
    #GET THE WEIGHTS IN HERE 
    # Save the weights in both dict and JSON formats
    weights_dict_obj = weights_dict  # this is still a Python dict for saving to DB
    weights_dict = json.dumps(weights_dict)  # JSON string for similarity endpoint
    #Calculating Similarity 
    api_url = f"http://host.docker.internal:4000/ml/ml/cosine/{chosen_country}/{weights_dict}"
    response = requests.get(api_url, headers=headers, timeout=10)
    #print(response)

    if response.status_code == 200:
        # Save preferences to backend (if user is signed in)
        if 'user_id' in st.session_state:
            preferences_payload = {
                "preventionWeight": weights_dict_obj.get("Prevention", 1.0) * 100,
                "detectReportWeight": weights_dict_obj.get("Detection & Reporting", 1.0) * 100,
                "rapidRespWeight": weights_dict_obj.get("Rapid Response", 1.0) * 100,
                "healthSysWeight": weights_dict_obj.get("Health System", 1.0) * 100,
                "intlNormsWeight": weights_dict_obj.get("International Norms Compliance", 1.0) * 100,
                "riskEnvWeight": weights_dict_obj.get("Risk Environment", 1.0) * 100
            }

            try:
                save_url = f"http://host.docker.internal:4000/users/users/{st.session_state['user_id']}/preferences"
                save_response = requests.put(save_url, json=preferences_payload, headers=headers, timeout=10)
                if save_response.status_code == 200:
                    # st.success("Your preferences have been saved.")
                    pass
                else:
                    st.warning(f"Could not save preferences: {save_response.status_code}")
            except Exception as e:
                st.warning(f"Error saving preferences: {e}")
        data = response.text  
        #st.success("It worked!")
        data_dict = json.loads(data)
        df_similar = pd.DataFrame(data_dict)
        sorted_df_similar = df_similar.sort_values(by='the_country_cosine', ascending=False)
        #st.write(f"Here are the countries most similar to: {chosen_country}")
        #st.dataframe(sorted_df_similar.head(10)) 
        #st.write(f"Here are the countries least similar to: {chosen_country}")
        #st.dataframe(sorted_df_similar.tail(10)) 
        bar_chart_display = sorted_df_similar[1:6]
        st.session_state['similar_df'] = sorted_df_similar
    else:
        st.error(response.status_code)
        st.error("No data for the country available")
if on and chosen_country is not None:
    country_url = "http://host.docker.internal:4000/country/countries"  
    try:
        headers = {
        "User-Agent": "Python/requests",
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        response = requests.get(country_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        df_country_and_code = pd.DataFrame(data)
        #print(df_country_and_code)
        if 'similar_df' in st.session_state:
            sorted_df_similar = st.session_state['similar_df']

        add_names = []
        for index, row in df_country_and_code.iterrows():
            for index2, row2 in sorted_df_similar.iterrows():
                if row['code'] == row2['Country']:
                    add_names.append(row['name'])
        sorted_df_similar['name'] = add_names
        #print("THIS IS MY DATAFRAME INSIDE: ", sorted_df_similar)
        print("THIS IS MY DATAFRAME:", sorted_df_similar)
        fig1 = px.choropleth(
            sorted_df_similar,
            locations='Country',  # Column with country names/codes
            locationmode='ISO-3',  
            color='the_country_cosine',  # Column with similarity scores
            color_continuous_scale="Viridis",
            range_color=(-1, 1),  # Adjusted range to better show differences (since most scores are >0.95)
            scope='world',
            labels={'the_country_cosine': 'Similarity Score'},
            title='Country Similarity Scores (World)'
        )

        # Update layout for better display
        fig1.update_geos(showcountries=True, showcoastlines=True, showland=True)
        fig1.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

        st.plotly_chart(fig1, use_container_width=True)
    except requests.exceptions.RequestException as e:
        print("API request failed:", e)

elif not on and chosen_country is not None: 
    # Create the bar chart with individual bar colors
    fig = px.bar(bar_chart_display,
                    x='Country',
                    y='the_country_cosine',
                    color='Country',  
                    color_discrete_sequence=px.colors.qualitative.Set2 
                )

    fig.update_yaxes(range=[0.90, 1])
    # Customize axes labels and layout
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Similarity Score"
    )

    st.plotly_chart(fig, use_container_width=True)



