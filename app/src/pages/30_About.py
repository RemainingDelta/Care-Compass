import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# GET TO KNOW CARE COMPASS")

st.markdown(
    """
    Hi, we’re :green[Team Care Compass]! We use real health data and machine learning to 
    help users compare and understand global healthcare systems. Our platform lets 
    you explore country profiles, visualize key trends, and get personalized 
    recommendations based on your healthcare priorities.

    
    With an expansive network of public health knowledge at our fingertips, evaluating 
    and comparing healthcare systems across countries can be a complex and overwhelming 
    process. Our project aims to simplify this by evaluating complex public health data 
    and providing users access to succinct, intuitive insights, making it more easily 
    accessible and understandable to a broader audience of users.

    
    We are building an application that helps users explore and evaluate the healthcare 
    systems of different countries based on :green[six core factors] from the Global Health 
    Security Index:
    - Prevention
    - Detection and Reporting
    - Rapid Response
    - Health System
    - Compliance with International Norms
    - Risk Environment

    
    Our application converts raw public healthcare data to insights to drive equitable 
    improvements and informed populations regarding healthcare around the world.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
