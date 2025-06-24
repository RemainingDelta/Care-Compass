import streamlit as st
import base64

def style_sidebar():
    st.markdown(
    """
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #c2ddd9; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def set_background_color():
    st.markdown(
        """
        <style>
        /* Main app background - light green gradient */
        .stApp {
            background: linear-gradient(135deg, #e6f7f5 0%, #d1f2eb 100%);
        }
        
        /* Also target the main content area */
        .main {
            background: transparent;
        }
        
        /* Target the block container */
        .block-container {
            background: transparent;
        }
        
        /* Make sure sections don't have white backgrounds */
        section[data-testid="stSidebar"] > div {
            background: transparent;
        }
        
        /* Target the main view container */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #e6f7f5 0%, #d1f2eb 100%);

        }
        
        /* Target header if needed */
        [data-testid="stHeader"] {
            background: transparent;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
