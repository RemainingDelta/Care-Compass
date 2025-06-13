import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from urllib.error import URLError
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import random
import json

from modules.style import style_sidebar, set_background
style_sidebar()

SideBarLinks()


st.title("FAVORITE HEALTHCARE ARTICLES")

 # Healthcare Articles 
def get_random_thumbnail():
    names = [
        "Book-Blue.png", "Book-Green.png", "Book-Orange.png", "Book-Purple.png", "Book-Red.png",
        "ClipBoard-Blue.png", "ClipBoard-Green.png", "ClipBoard-Orange.png", "ClipBoard-Purple.png", "ClipBoard-Red.png",
        "MagnifyingGlass-Blue.png", "MagnifyingGlass-Green.png", "MagnifyingGlass-Orange.png", "MagnifyingGlass-Purple.png", "MagnifyingGlass-Red.png"
    ]
    # Assuming you are running streamlit from the `app/` root and images are in `app/src/assets/`
    return f"assets/{random.choice(names)}"

userID = st.session_state["id"]
# fav_articles_URL = f"http://host.docker.internal:4000/country/articles/favorite"
fav_articles_URL = f"http://host.docker.internal:4000/country/articles/favorite?userID={userID}"

# Confirm the structure
st.write("userID from session:", st.session_state["id"])

try:
    # Fetch Articles details
    response = requests.get(fav_articles_URL)

    if response.status_code == 200:
        favorites = response.json()

        cols = st.columns(3)

        for i, article in enumerate(favorites):
            col = cols[i % 3]
            with col:
                st.container(border=True)
                st.image(get_random_thumbnail())
                st.markdown(f"**{article['article_title']}**")
                col_a, col_b = st.columns([0.85,0.15],gap="small")
                with col_a:
                    st.markdown(f"*{article['source']}*")
                    st.markdown(f"[Read more]({article['article_link']})", unsafe_allow_html=True)

        

    elif response.status_code == 404:
        st.error("Favorite Articles not found")
    else:
        st.error(
            f"Error fetching Favorite Article data: {response.json().get('error', 'Unknown error')}"
        )

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running")

