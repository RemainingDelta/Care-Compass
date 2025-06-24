import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
from modules.style import style_sidebar, set_background_color


# Page config
st.set_page_config(layout='wide', page_title="Student Home - Healthcare Education Journey", page_icon="🎓")
style_sidebar()
set_background_color() 
SideBarLinks()

# Custom CSS for modern styling
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
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        height: 100%;
        border: 1px solid rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(9, 121, 105, 0.15);
        background: rgba(232, 245, 240, 0.3);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #097969 0%, #0a9d7a 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #666;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        text-align: center;
        width: 100%;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        color: white !important;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(9, 121, 105, 0.3);
        width: 100%;
        margin-top: auto;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(9, 121, 105, 0.4);
        background: linear-gradient(135deg, #0a9d7a 0%, #097969 100%);
    }
    
    /* Stats section */
    .stats-container {
        background: #f8f9fa;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
    }
    
    .stat-item {
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #097969 0%, #0a9d7a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #666;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
    }
    
    /* Custom alert styling to match green theme */
    .stInfo {
        background: rgba(232, 245, 240, 0.8);
        color: #097969;
        border: 1px solid rgba(9, 121, 105, 0.3);
        border-radius: 10px;
    }
    
    .stSuccess {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
    <div class="hero-container">
        <h1 class="hero-title" style="color: white !important;">Welcome, {st.session_state.get('name', 'Student')}! 🎓</h1>
        <p class="hero-subtitle" style="color: white !important;">Explore global healthcare education opportunities and find your perfect study destination</p>
    </div>
""", unsafe_allow_html=True)

# Feature Cards Section
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <h3 class="feature-title">Compare Countries</h3>
            <p class="feature-description">
                Evaluate multiple countries side-by-side. Compare key metrics, living conditions, and opportunities to find the best destination for your studies.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button('Start Comparing', key='compare', use_container_width=True):
        st.switch_page('pages/11_Country_Comparator.py')

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3 class="feature-title">Country Profiles</h3>
            <p class="feature-description">
                Deep dive into comprehensive country profiles. Explore education systems, healthcare quality, visa requirements, and student life in your destination.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button('Explore Countries', key='profiles', use_container_width=True):
        st.switch_page('pages/02_Country_Profile.py')

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⭐</div>
            <h3 class="feature-title">Saved Articles</h3>
            <p class="feature-description">
                Access your personalized collection of study abroad guides and resources. Save important information for easy reference during your education journey.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button('View Favorites', key='favorites', use_container_width=True):
        st.switch_page('pages/12_Favorite_Articles.py')



# Stats Section
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">195+</div>
            <div class="stat-label">Countries Analyzed</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">1000+</div>
            <div class="stat-label">Health Metrics</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">6</div>
            <div class="stat-label">Core Health Factors</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Resource Access</div>
        </div>
    """, unsafe_allow_html=True)

# Quick Tips Section
with st.container():
    st.markdown("### 💡 Student Success Tips")
    tip_col1, tip_col2 = st.columns(2)
    
    with tip_col1:
        st.info("**📖 New to studying abroad?** Start by comparing 3-4 countries that interest you to understand the differences in healthcare education systems and requirements.")
    
    with tip_col2:
        st.success("**🎯 Pro tip:** Save articles about healthcare education programs and international study requirements to build your personal resource library!")
