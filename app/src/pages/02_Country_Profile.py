import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

from modules.style import style_sidebar, set_background
style_sidebar()

SideBarLinks()


# add the logo
#add_logo("assets/logo.png", height=400)

# set up the page
st.title("<COUNTRY> PROFILE")

col1, col2 = st.columns([0.8,0.2],gap="large",vertical_alignment="top",border=True)

with col1 :
    st.subheader("General Information")
    st.divider()
    st.subheader("Healthcare Information")

with col2 : 
    st.markdown("Check out countries with similar scores.")

with st.container(height=393, border=True):
    cols_mr = st.columns([10.9, 0.2, 10.9])
    with cols_mr[0].container(height=350, border=False):
        st.write("Streamlit is an open-source Python framework for data scientists and AI/ML engineers to deliver dynamic data apps with only a few lines of code. Build and deploy powerful data apps in minutes. Let's get started!")
        st.image('https://docs.streamlit.io/images/app_model.png')
    with cols_mr[1]:
        st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 320px;
                        margin: auto;
                    }
                </style>
            '''
        )
    with cols_mr[2].container(height=350, border=False):
        st.write(
            '''
                Now that you know a little more about all the individual pieces, let's close the loop and review how it works together:
                - Streamlit apps are Python scripts that run from top to bottom.
                - Every time a user opens a browser tab pointing to your app, the script is executed and a new session starts.
                - As the script executes, Streamlit draws its output live in a browser.
                - Every time a user interacts with a widget, your script is re-executed and Streamlit redraws its output in the browser.
                - The output value of that widget matches the new value during that rerun.
                - Scripts use the Streamlit cache to avoid recomputing expensive functions, so updates happen very fast.
                - Session State lets you save information that persists between reruns when you need more than a simple widget.
                - Streamlit apps can contain multiple pages, which are defined in separate .py files in a pages folder.
            '''
        )

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.link_button("Supporting Article 1", "url", type="secondary", use_container_width=True)
    st.link_button("Supporting Artcile 4", "url", type="secondary", use_container_width=True)
with col_b:
    st.link_button("Supporting Article 2", "url", type="secondary", use_container_width=True)
    st.link_button("Supporting Artcile 5", "url", type="secondary", use_container_width=True)
with col_c:
    st.link_button("Supporting Article 3", "url", type="secondary", use_container_width=True)
    st.link_button("Supporting Artcile 6", "url", type="secondary", use_container_width=True)
