import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from modules.style import style_sidebar, set_background_color


# Page config
st.set_page_config(layout='wide', page_title="About - Care Compass", page_icon="🧭")
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
    
    /* Mission section */
    .mission-container {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border-left: 4px solid #097969;
    }
    
    .mission-title {
        font-size: 2rem;
        font-weight: 700;
        color: #097969;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .mission-text {
        font-size: 1.1rem;
        color: #2c3e50;
        line-height: 1.8;
    }
    
    /* Feature cards */
    .factor-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        height: 100%;
        border: 1px solid rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .factor-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 20px rgba(9, 121, 105, 0.1);
        background: rgba(232, 245, 240, 0.3);
    }
    
    .factor-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .factor-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.3rem;
    }
    
    .factor-description {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* About section */
    .about-section {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(9, 121, 105, 0.2);
    }
    
    .about-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #097969;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Stats section */
    .stat-item {
        padding: 1rem;
        text-align: center;
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
    
    /* Team section */
    .team-section {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    }
    
    .team-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #097969;
        margin-bottom: 1rem;
        text-align: center;
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
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(9, 121, 105, 0.4);
        background: linear-gradient(135deg, #0a9d7a 0%, #097969 100%);
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
    
    .highlight-green {
        color: #097969;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title" style="color: white !important;">Get to Know Care Compass 🧭</h1>
        <p class="hero-subtitle" style="color: white !important;">Navigating global healthcare with data-driven insights</p>
    </div>
""", unsafe_allow_html=True)

# Mission Section
st.markdown("""
    <div class="mission-container">
        <h2 class="mission-title">
            <span>🌍</span>
            <span>Our Mission</span>
        </h2>
        <p class="mission-text">
            Hi, we're <span class="highlight-green">Team Care Compass</span>! We use real health data and machine learning to 
            help users compare and understand global healthcare systems. Our platform lets you explore country profiles, 
            visualize key trends, and get personalized recommendations based on your healthcare priorities.
        </p>
    </div>
""", unsafe_allow_html=True)

# Problem & Solution
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="about-section" style="height: 100%;">
            <h3 style="font-size: 1.5rem; color: #097969; margin-bottom: 1rem;">
                <span style="font-size: 1.8rem;">🎯</span> The Challenge
            </h3>
            <p style="color: #2c3e50; line-height: 1.8;">
                With an expansive network of public health knowledge at our fingertips, evaluating 
                and comparing healthcare systems across countries can be a complex and overwhelming 
                process. Making sense of vast amounts of healthcare data requires expertise and time 
                that most people don't have.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="about-section" style="height: 100%;">
            <h3 style="font-size: 1.5rem; color: #097969; margin-bottom: 1rem;">
                <span style="font-size: 1.8rem;">💡</span> Our Solution
            </h3>
            <p style="color: #2c3e50; line-height: 1.8;">
                Care Compass simplifies this by evaluating complex public health data and providing 
                users access to succinct, intuitive insights. We make healthcare information more 
                easily accessible and understandable to a broader audience, from individuals to 
                policymakers.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Six Core Factors
st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="font-size: 2rem; font-weight: 700; color: #097969; text-align: center; margin-bottom: 2rem;">
            Six Core Healthcare Factors We Analyze
        </h2>
    </div>
""", unsafe_allow_html=True)

# Factor cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="factor-card">
            <span class="factor-icon">🛡️</span>
            <h4 class="factor-title">Prevention</h4>
            <p class="factor-description">
                Measures to prevent disease emergence and spread
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="factor-card" style="margin-top: 1rem;">
            <span class="factor-icon">🔬</span>
            <h4 class="factor-title">Detection & Reporting</h4>
            <p class="factor-description">
                Early detection and transparent reporting capabilities
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="factor-card">
            <span class="factor-icon">⚡</span>
            <h4 class="factor-title">Rapid Response</h4>
            <p class="factor-description">
                Speed and effectiveness of emergency response
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="factor-card" style="margin-top: 1rem;">
            <span class="factor-icon">🏥</span>
            <h4 class="factor-title">Health System</h4>
            <p class="factor-description">
                Quality and accessibility of healthcare infrastructure
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="factor-card">
            <span class="factor-icon">🌐</span>
            <h4 class="factor-title">International Norms</h4>
            <p class="factor-description">
                Compliance with global health regulations
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="factor-card" style="margin-top: 1rem;">
            <span class="factor-icon">⚠️</span>
            <h4 class="factor-title">Risk Environment</h4>
            <p class="factor-description">
                Environmental and societal vulnerability factors
            </p>
        </div>
    """, unsafe_allow_html=True)

# Impact Stats
st.markdown("---")
st.markdown("""
    <h2 style="font-size: 1.8rem; font-weight: 700; color: #097969; text-align: center; margin: 2rem 0;">
        Our Impact by the Numbers
    </h2>
""", unsafe_allow_html=True)

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
            <div class="stat-number">6</div>
            <div class="stat-label">Core Health Factors</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">1000+</div>
            <div class="stat-label">Data Points</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">3</div>
            <div class="stat-label">User Types Served</div>
        </div>
    """, unsafe_allow_html=True)

# Our Approach
st.markdown("""
    <div class="mission-container" style="margin-top: 2rem;">
        <h2 class="mission-title">
            <span>🚀</span>
            <span>Our Approach</span>
        </h2>
        <p class="mission-text">
            Care Compass converts raw public healthcare data into actionable insights to drive equitable 
            improvements and create informed populations regarding healthcare around the world. We leverage 
            the Global Health Security Index data combined with advanced analytics and machine learning to 
            provide personalized recommendations that matter to you.
        </p>
    </div>
""", unsafe_allow_html=True)

# CTA Section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h3 style="color: #097969; margin-bottom: 1rem;">Ready to explore global healthcare insights?</h3>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🏠 Return to Home", type="primary", use_container_width=True):
        st.switch_page("Home.py")