import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Get to Know Care Compass")

st.markdown(
    """
    Hi, we’re :blue[Team Care Compass]! We use real health data and machine learning to 
    help users compare and understand global healthcare systems. Our platform lets 
    you explore country profiles, visualize key trends, and get personalized 
    recommendations based on your healthcare priorities.

    
    With an expansive network of public health knowledge at our fingertips, evaluating 
    and comparing healthcare systems across countries can be a complex and overwhelming 
    process. Our project aims to simplify this by evaluating complex public health data 
    and providing users access to succinct, intuitive insights, making it more easily 
    accessible and understandable to a broader audience of users.

    
    We are building an application that helps users explore and evaluate the healthcare 
    systems of different countries based on six core factors from the Global Health 
    Security Index:
    - Prevention
    - Detection and Reporting
    - Rapid Response
    - Health System
    - Compliance with International Norms
    - Risk Environment

    
    We are utilizing the Global Health Security Index, which provides a standardized 
    scoring system across six core healthcare factors to generate a composite assessment 
    for each country. Rather than allowing users to customize weights directly, we leverage 
    the index to implement a machine learning model using k-nearest neighbors (k-NN). 
    This enables users to express their healthcare priorities through sliders, which are 
    transformed into a preference vector and compared against normalized country data to 
    identify the most similar healthcare systems. Additionally, users can optionally select 
    a country of origin. When enabled, recommendations blend similarity to that country with 
    the user’s stated preferences to deliver context-aware results.

    
    The resulting country matches are visualized through ranked comparisons, interactive heat 
    maps, and a side-by-side comparison tool for exploring differences in key health indicators. 
    In addition, users can track how selected indicators have changed over time and view 
    predictive forecasts for future performance, offering a forward-looking perspective based 
    on historical trends.

    
    The application converts raw public healthcare data to insights to drive equitable 
    improvements and informed populations regarding healthcare around the world.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
