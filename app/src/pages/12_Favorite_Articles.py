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

st.write("Session keys:", list(st.session_state.keys()))
st.write("Session values:", dict(st.session_state))

if not st.session_state.get("authenticated"):
    st.warning("You must be logged in to access this page.")
    st.stop()

# Try multiple fallback keys to get the user ID
userID = (
    st.session_state.get("user_id")
    or st.session_state.get("id")
    or st.session_state.get("user", {}).get("id")
)

if not userID:
    st.warning("You must be logged in to view your favorite articles.")
    st.stop()

# fav_articles_URL = f"http://host.docker.internal:4000/country/articles/favorite"
fav_articles_URL = f"http://host.docker.internal:4000/country/articles/favorite?userID={userID}"

# Confirm the structure
userID = st.session_state.get("user_id")
st.write("userID from session:", userID)



try:
    # Fetch Articles details
    response = requests.get(fav_articles_URL)
    
    if response.status_code == 200:
        st.write("Raw response text:", response.text)
        try:
            favorites = response.json()
        except Exception as e:
            st.error("Could not parse JSON. Here's the raw response:")
            st.code(response.text)
            st.stop()


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

