import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

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


