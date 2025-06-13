import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import requests
import random
from streamlit_extras.stateful_button import button
import json

from modules.style import style_sidebar, set_background
style_sidebar()

SideBarLinks()


userID = st.session_state['id']

#getting all the countries 
country_url = "http://host.docker.internal:4000/country/countries"  

country_list = []
country_code_list = []

try:
    response = requests.get(country_url)
    response.raise_for_status()
    data = response.json()

    country_list = [item["name"] for item in data]
    code_list = [item["code"] for item in data]
    country_code_list = [item['name'] + '-' + item['code'] for item in data]

    print("Countries:", country_list)


except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)


# CHOOSE COUNTRIES
selected_country = st.selectbox(
    "Select Country:",
    country_code_list,
    index=None
)

#once the country is selected start getting the information 
if selected_country :
    start_index = (str(selected_country)).index('-') + 1
    country_code = selected_country[start_index:]
        
    # API endpoint
    API_URL = f"http://host.docker.internal:4000/country/countries/{country_code}"  

    try:
        # Fetch Country details
        response = requests.get(API_URL)

        if response.status_code == 200:
            country = response.json()

            # Display basic information
            st.title(country["name"] + " Profile")
            
            col1, col2 = st.columns([0.8,0.2],gap="medium",vertical_alignment="top",border=True)

            with col1:
                if country.get("info"):
                    st.subheader("General Information")
                    for info in country["info"]:
                        st.write(f'{info["generalInfo"]}')
                else:
                    st.info("No information found for this Country")
                
                st.divider()
                st.subheader("Healthcare Information")
                for info in country["info"]:
                    st.write(f'{info["healthcareInfo"]}')
                    st.write("")
            #display countries with similarity scores close to the given country 
            with col2 : 
                st.markdown("Countries with similar scores:")
                factors = [
                    "Prevention",
                    "Health System",
                    "Rapid Response",
                    "Detection & Reporting",
                    "International Norms Compliance",
                    "Risk Environment"
                ]
                weights = [95, 76, 52, 33, 10, 10]
                weights_dict ={}
                for i in range(6):
                    weights_dict[factors[i]] = float(weights[i]/100)
                weights_dict = json.dumps(weights_dict)
                API_URL_2 = f"http://host.docker.internal:4000/ml/ml/cosine//{country_code}/{weights_dict}" 
                response = requests.get(API_URL_2) 
                
                if response.status_code == 200:
                    data = response.text  
                    data_dict = json.loads(data)
                    df_similar = pd.DataFrame(data_dict)
                    sorted_df_similar = df_similar.sort_values(by='the_country_cosine', ascending=False)
                    display = sorted_df_similar[1:6]
                    st.session_state['similar_df'] = sorted_df_similar
                    for index, row in display.iterrows():
                        st.write(row['Country'], ":", round(row['the_country_cosine'], 4))
                else:
                    st.error(response.status_code)
                
                    st.error("No data for the country available")
                    st.error(response.text)

        elif response.status_code == 404:
            st.error("Country not found")
        else:
            st.error(
                f"Error fetching Country data: {response.json().get('error', 'Unknown error')}"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running")


    # Healthcare Articles 
    def get_random_thumbnail():
        names = [
            "Book-Blue.png", "Book-Green.png", "Book-Orange.png", "Book-Purple.png", "Book-Red.png",
            "ClipBoard-Blue.png", "ClipBoard-Green.png", "ClipBoard-Orange.png", "ClipBoard-Purple.png", "ClipBoard-Red.png",
            "MagnifyingGlass-Blue.png", "MagnifyingGlass-Green.png", "MagnifyingGlass-Orange.png", "MagnifyingGlass-Purple.png", "MagnifyingGlass-Red.png"
        ]
        # Assuming you are running streamlit from the `app/` root and images are in `app/src/assets/`
        return f"assets/{random.choice(names)}"


    st.header(f"Healthcare Articles for {country_code}")

    res = requests.get(f"http://host.docker.internal:4000/country/countries/{country_code}/articles")

    articles = res.json()


    # 3 columns
    cols = st.columns(3)

    for i, article in enumerate(articles):
        col = cols[i % 3]
        with col:
            st.container(border=True)
            st.image(get_random_thumbnail())
            st.markdown(f"**{article['title']}**")

            col_a, col_b = st.columns([0.85,0.15],gap="small")

            with col_a:
                st.markdown(f"*{article['source']}*")
                st.markdown(f"[Read more]({article['link']})", unsafe_allow_html=True)

            with col_b:
                favorite_icon = "⭐️"

                if button(favorite_icon, key=f"{article['id']}bookmark_button") : 
                    favorite_data = {
                        "userID": userID["id"], 
                        "articleID": article["id"]
                    }
                    #st.write("favorite_data =", favorite_data)

                    favorite_url = "http://host.docker.internal:4000/country/articles/favorite"
                    
                    response = requests.post(favorite_url, json=favorite_data)

                    # try:
                    #     # Send POST request to API
                    #     response = requests.post(favorite_url, json=favorite_data)

                    #     if response.status_code == 201:
                    #         st.success("Article added successfully!")
                    #     elif response.status_code == 409:
                    #         st.warning("This article is already in your favorites.")
                    #     else:
                    #         try:
                    #             error_message = response.json().get("error", "Unknown error")
                    #         except ValueError:
                    #             error_message = f"Non-JSON response: {response.text}"
                            
                    #         st.error(f"Failed to add Article: {error_message}")

                    # except requests.exceptions.RequestException as e:
                    #     st.error(f"Error connecting to the API: {str(e)}")
                        # st.info("Please ensure the API server is running")

              