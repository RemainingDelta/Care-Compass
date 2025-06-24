import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import json
from modules.style import style_sidebar, set_background_color


# Page config
st.set_page_config(layout='wide', page_title="Team - Care Compass", page_icon="🧭")
style_sidebar()
set_background_color() 
SideBarLinks()

# Custom CSS for modern styling (matching About page)
st.markdown("""
<style>
    /* Global styles */
    .main {
        padding-top: 0rem;
        background-color: #fafafa;
    }
    
    /* Hero section styling */
    .hero-container {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container * {
        color: white !important;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(0.8); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 0.8; }
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: white !important;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: white !important;
        opacity: 0.95;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* Team member cards */
    .team-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .team-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(9, 121, 105, 0.15);
        border-color: rgba(9, 121, 105, 0.2);
    }
    
    .team-header {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .team-avatar {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: white;
        font-weight: 600;
        flex-shrink: 0;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3);
    }
    
    .team-info {
        flex-grow: 1;
    }
    
    .team-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.3rem;
    }
    
    .team-bio {
        color: #666;
        line-height: 1.8;
        font-size: 1rem;
        margin-top: 1rem;
    }
    
    /* Blog button section */
    .blog-section {
        background: linear-gradient(135deg, rgba(9, 121, 105, 0.05) 0%, rgba(10, 157, 122, 0.05) 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 1rem;
        text-align: center;
        border: 1px solid rgba(9, 121, 105, 0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 150px;
    }
    
    .blog-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #097969;
        margin-bottom: 0.7rem;
    }
    
    .blog-description {
        font-size: 1rem;
        color: #2c3e50;
        margin-bottom: 0;
        line-height: 1.7;
        max-width: 700px;
    }
    
    /* Custom button styling - applies to all buttons including link buttons */
    .stButton > button, [data-testid="stLinkButton"] > a {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3);
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    
    .stButton > button:hover, [data-testid="stLinkButton"] > a:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(9, 121, 105, 0.4);
        background: linear-gradient(135deg, #0a9d7a 0%, #097969 100%) !important;
        color: white !important;
    }
    
    /* Ensure link buttons get the gradient */
    div[data-testid="column"] a[kind="primary"] {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%) !important;
        color: white !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3) !important;
    }
    
    /* Additional selector for streamlit link buttons */
    .stLinkButton a {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        text-decoration: none !important;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Email button special styling */
    .email-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(9, 121, 105, 0.1);
        color: #097969;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid rgba(9, 121, 105, 0.2);
    }
    
    .email-button:hover {
        background: rgba(9, 121, 105, 0.2);
        transform: translateY(-1px);
        box-shadow: 0 2px 10px rgba(9, 121, 105, 0.2);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
        .team-header {
            flex-direction: column;
            text-align: center;
        }
    }
    
    .highlight-green {
        color: #097969;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title" style="color: white !important;">Meet Our Team 👋</h1>
        <p class="hero-subtitle" style="color: white !important;">The passionate minds behind Care Compass</p>
    </div>
""", unsafe_allow_html=True)

# Blog Link Section
st.markdown("""
    <div class="blog-section">
        <h3 class="blog-title">📖 Explore Our Research & Insights</h3>
        <p class="blog-description">
            Discover in-depth analysis of global healthcare systems through our data-driven research. 
            Read country spotlights, methodology deep-dives, policy trend analysis, and follow our team's 
            journey in making complex health data accessible and actionable for everyone.
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.link_button("🌐 Visit Care Compass Blog", 'https://arthur-t-huang.github.io/Care-Compass-Blog/', type="primary", use_container_width=True)

st.write("")

# Team members data
team_members = [
    {
        "name": "Anoushka Abroal",
        "email": "abroal.a@northeastern.edu",
        "initials": "AA",
        "bio": "Passionate and highly motivated Northeastern honors college student interested in research opportunities to collaborate on real world challenges using AI, machine learning, and data science. Experienced at working on individual research projects as well as team based initiatives. Detail-oriented and project management-focused about completing my projects on time. Self-driven person who enjoys solving technically challenging problems and researching new approaches to traditional solutions. Eager to take on new challenges and enjoys collaborating with others. Focused on how technology can be leveraged for better healthcare research outcomes. Held leadership roles in school and external clubs. Volunteered with technical teams at the American Diabetes Association. Strong communication and task prioritization skills."
    },
    {
        "name": "Arthur Huang",
        "email": "huang.arth@northeastern.edu",
        "initials": "AH",
        "bio": "Arthur Huang is a 18 year old male computer science major with an electrical engineering minor at Northeastern University. He is a very adventurous and team oriented individual who is eager to embark on new projects and opportunites regarding software development and artificial intelligence. In his free time, he enjoys golfing, skiing, and cooking."
    },
    {
        "name": "Katherine Ahn",
        "email": "ahn.ka@northeastern.edu",
        "initials": "KA",
        "bio": "Katherine Ahn is a rising fourth year Biology and Math major with minors in Data Science and Global Health at Northeastern University. An aspiring Bioinformatician, Katherine is pursuing a Masters in the field following graduation. Katherine has always been greatly interested in the healthcare sector, and her education at Northeastern has provided her with the tools to look at it from a lens she never considered – through a data filled lens."
    },
    {
        "name": "Shiven Ajwaliya",
        "email": "ajwaliya.s@northeastern.edu",
        "initials": "SA",
        "bio": "Hi, my name is Shiven Ajwaliya, a CS student at Northeastern University who loves learning new things and traveling. I'm passionate about building meaningful tech products, exploring different cultures, and discovering new places through local food and history."
    }
]

# Display team members
for member in team_members:
    st.markdown(f"""
        <div class="team-card">
            <div class="team-header">
                <div class="team-avatar">{member['initials']}</div>
                <div class="team-info">
                    <h3 class="team-name">{member['name']}</h3>
                    <a href="mailto:{member['email']}" class="email-button">
                        📧 {member['email']}
                    </a>
                </div>
            </div>
            <p class="team-bio">{member['bio']}</p>
        </div>
    """, unsafe_allow_html=True)

# Add some spacing before the return button
st.write("")

# Return to home button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🏠 Return to Home", type="primary", use_container_width=True):
        st.switch_page("Home.py")